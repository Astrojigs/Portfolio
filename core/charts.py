import colorsys
import json
import os
import re
from matplotlib import cm, colors as mcolors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from functools import lru_cache
import requests
import seaborn as sns
import plotly.express as px
import streamlit as st
from typing import Literal, List, Optional, Union, Sequence, Callable, Dict, Set, Any
import geopandas as gpd
from matplotlib.pyplot import title
from scipy.stats import gaussian_kde
from streamlit_echarts import st_echarts, JsCode, Map


@st.cache_data(show_spinner=False)
def load_geojson(source: str, source_type: str = "file") -> dict:
    """
    Load a GeoJSON dict from either:
      - a local file ('.shp' or '.geojson'), or
      - a URL returning GeoJSON.
    Shapefiles are read via GeoPandas and converted to GeoJSON.
    """
    # --- support in-memory GeoJson dicts ---------------
    if source_type == 'geojson' or isinstance(source, dict):
        return source
    ## --- fallback to file/URL logic
    ext = os.path.splitext(source)[1].lower()
    # 1) Local file
    if source_type == "file":
        if ext == ".shp":
            # Read shapefile and convert to GeoJSON
            try:
                gdf = gpd.read_file(source)
            except UnicodeDecodeError:
                # try a fallback encoding if needed
                gdf = gpd.read_file(source, encoding="ISO-8859-1")
            # ensure we have text-friendly property names
            geojson_str = gdf.to_json()
            return json.loads(geojson_str)
        elif ext in (".geojson", ".json"):
            with open(source, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    # 2) Remote URL
    elif source_type in ("url", "online"):
        resp = requests.get(source)
        resp.raise_for_status()
        return resp.json()
    else:
        raise ValueError(f"Unknown source_type '{source_type}', expected 'file' or 'url'.")


class GIS:
    """
    Lightweight helper to plot GeoJSON layers (choropleth or scatter)
    with Streamlit-ECharts, now with optional Matplotlib colormap and hover-only labels.
    """
    _maps: Dict[str, Map] = {}  # cache Map instances

    def __init__(self, layers: List[Dict[str, Any]]):
        if not layers:
            raise ValueError("Provide at least one layer configuration.")
        self.layers = []
        for layer in layers:
            map_name = layer["map_name"]
            geojson = load_geojson(layer["source"], layer.get("source_type", "file"))
            key = layer.get("name_field") or self._detect_name_field(geojson)

            names = set()
            for feat in geojson.get("features", []):
                props = feat.setdefault("properties", {})
                raw = props.get(key)
                clean = (
                    re.sub(r"^Co\.?\s+", "", str(raw)).strip().title()
                    if raw is not None else None
                )
                props["name"] = clean
                if clean:
                    names.add(clean)

            if map_name not in self._maps:
                self._maps[map_name] = Map(map_name, geojson)

            self.layers.append({
                "map_name": map_name,
                "names": names,
                "map": self._maps[map_name],
            })

    @staticmethod
    def _detect_name_field(geojson: Dict[str, Any]) -> str:
        features = geojson.get("features", [])
        if not features:
            raise RuntimeError("GeoJSON has no features to inspect.")
        candidates = ["name", "county", "pc", "postcode", "routingkey", "id"]
        for field in features[0].get("properties", {}):
            if field.lower() in candidates:
                return field
        return next(iter(features[0]["properties"]))

    @staticmethod
    def clean_area(series, collapse_dublin: bool = False):
        """Remove 'Co.' prefix and title-case area names."""
        series = (
            series.fillna("")
            .str.replace(r"^Co\.?\s+", "", regex=True)
            .str.strip()
            .str.title()
        )
        if collapse_dublin:
            series = series.str.replace(r"Dublin\s*\d+[A-Za-z]*", 'Dublin', regex=True)
        return series

    def plot(
            self,
            df,
            *,
            county_col: Optional[str] = None,
            value_col: Optional[str] = None,
            lat_col: Optional[str] = None,
            lon_col: Optional[str] = None,
            # scatter options
            symbol_size: int = 8,
            # choropleth options
            visual_map: bool = True,
            tooltip_title: Optional[str] = None,
            map_title: Optional[str] = 'Map of Ireland',
            cmap: Optional[Union[str, Sequence[str]]] = None,
            cmap_steps: int = 7,
            # label options
            label_show: bool = False,
            label_size: int = 12,
            label_on_hover: bool = False,
            hover_label_size: Optional[int] = None,
            # styling
            fill_color: Optional[str] = None,
            fill_opacity: Optional[float] = None,
            hover_color: Optional[str] = None,
            extra_geo_opts: Optional[Dict[str, Any]] = None,
            extra_series_opts: Optional[Dict[str, Any]] = None,
            height: Union[int, str] = "600px",
            width: Optional[Union[int, str]] = None,
    ):
        def _resolve_cmap(spec, steps):
            if spec is None:
                return None
            if isinstance(spec, (list, tuple)):
                return [mcolors.to_hex(c) for c in spec]
            if isinstance(spec, str):
                m = cm.get_cmap(spec, steps)
                return [mcolors.to_hex(m(i)) for i in range(m.N)]
            raise TypeError("`cmap` must be a colormap name or list of colours")

        geo_opts = extra_geo_opts or {}
        series_opts = extra_series_opts or {}

        # map title opts ------Main Title Options
        title_opts = {
            'text': map_title,
            'subtext': 'Clinical Data Department \n The Mater Misericordiae University Hospital',
            'left': 'right'
        }

        # ---- Options for Tooltip title
        if tooltip_title:
            tooltip_title_html = (
                f"<span "
                f"style='color:darkgray; font-size:14px; font-wight:bold;'>"
                f"{tooltip_title}</span><br/>"
            )
        else:
            tooltip_title_html = ""
        tooltip_opts = {
            'trigger': 'item',
            'formatter': f"{tooltip_title_html}{{b}}: {{c}}",
            "backgroundColor": 'white'
        }

        # --------------toolbox
        toolbox_opts = {
            'show': True,
            # // orient: 'vertical',
            'left': 'left',
            'top': 'top',
            'feature': {
                'dataView': {'readOnly': True},
                'restore': {},
                'saveAsImage': {'name': map_title,
                                'type': 'png'}
            }
        }

        ## ------------------------ Type of Plots --------------------
        # 1) Scatter mode
        if lat_col and lon_col:
            data = [
                [r[lon_col], r[lat_col], r.get(value_col)]
                for r in df.to_dict("records")
            ]
            opts = {
                'title': title_opts,
                "tooltip": tooltip_opts,
                "geo": {
                    "map": self.layers[0]["map_name"],
                    "roam": True,
                    "label": {"show": label_show, "fontSize": label_size},
                    **geo_opts,
                },

                "series": [{
                    "name": value_col or "",
                    "type": "scatter",
                    "coordinateSystem": "geo",
                    "symbolSize": symbol_size,
                    "label": {"show": label_show,
                              "fontSize": label_size,
                              'color': 'red',
                              },

                    "emphasis": {
                        "label": {"show": label_on_hover,
                                  "fontSize": hover_label_size or label_size},
                    },
                    "data": data,
                    **series_opts,
                }],
            }
            st_echarts(opts, map=self.layers[0]["map"], height=height, width=width)
            return

        # 2) Choropleth mode
        if not county_col or not value_col:
            raise ValueError("Both 'county_col' and 'value_col' are required for a choropleth.")
        areas = df[county_col].dropna().astype(str).str.title().unique()
        # pick the layer that matches most names
        _, layer = max(
            [(len(set(areas) & l["names"]), l) for l in self.layers],
            key=lambda x: x[0]
        )
        missing = set(areas) - layer["names"]
        if missing:
            # import streamlit as st
            st.warning(f"Areas not found in map '{layer['map_name']}': {sorted(missing)}")

        data = [
            {"name": r[county_col].strip().title(), "value": r[value_col]}
            for r in df.to_dict("records") if isinstance(r[county_col], str)
        ]

        # label configurations
        label_opts = {
            "show": label_show and not label_on_hover,
            "fontSize": label_size,
            'formatter': '{b}',
            'position': 'right',
            'offset': [18, 0]
        }
        emphasis_label = {
            "show": label_on_hover,
            "fontSize": hover_label_size or label_size
        } if label_on_hover else {}

        # item & emphasis styling
        style = {}
        if fill_color:
            style["areaColor"] = fill_color
        if fill_opacity is not None:
            style["opacity"] = fill_opacity

        emphasis_style = {}
        if hover_color:
            emphasis_style["areaColor"] = hover_color

        opts = {
            'title': title_opts,  # Title for map
            "tooltip": tooltip_opts,  # title for tooltip
            'toolbox': toolbox_opts,
            "series": [{
                "name": value_col,
                "type": "map",
                "map": layer["map_name"],
                "roam": True,  # pan the entire choropleth
                "label": label_opts,
                "itemStyle": style,
                "emphasis": {
                    "label": emphasis_label,
                    "itemStyle": emphasis_style
                },
                "data": data,
                **series_opts,
            }],
        }

        if visual_map:
            vis = {
                "min": float(df[value_col].min()),
                "max": float(df[value_col].max()),
                "left": "right",
                "top": "bottom",
                "text": ["High", "Low"],
                "calculable": True,
                "outOfRange": {'color': ['rgba(0,0,0,0)']},
            }
            cmap_list = _resolve_cmap(cmap, cmap_steps)
            if cmap_list:
                vis["inRange"] = {"color": cmap_list}
            opts["visualMap"] = vis

        # note: no 'geo' key here!
        st_echarts(opts, map=layer["map"], height=height, width=width)


# helper to lighten a hex color by fraction (0→full light)
def lighten_hex(hex_color: str, fraction: float) -> str:
    """Return a lighter hex string by interpolating toward white."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    # convert to HLS, bump lightness
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    l = min(1, l + fraction * (1 - l))
    nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(nr * 255):02x}{int(ng * 255):02x}{int(nb * 255):02x}"


class ECharts:
    """
    A collection of static methods for rendering common ECharts visualizations in Streamlit.
    Supports:
      - Pie / Donut (with rounded corners, inside & center-hover labels)
      - Bar (vertical or horizontal, with rounded corners, data labels)
      - Radar (multi-axis comparisons)
      - KDE (smoothed density estimate for continuous variables like LOS)
      - Histogram (count or density)
    """

    @classmethod
    def init_gis(cls, **gis_kwargs):
        cls.gis = GIS(**gis_kwargs)

    @staticmethod
    def pie(
            df: pd.DataFrame,
            names: str,
            values: str,
            title: Optional[str] = None,
            radius: str = "50%",
            inner_radius: Optional[str] = None,
            border_radius: int = 0,
            height: str = "400px",
            start_angle: int = 45,

            # legend placement
            legend_orient: Literal["vertical", "horizontal"] = "vertical",
            legend_left: str = "left",
            legend_top: Optional[Union[str, int]] = None,
            legend_bottom: Optional[Union[str, int]] = None,

            # labeling
            label_font_size: int = 10,
            label_inside: bool = False,
            label_inside_formatter: str = "{b}: {c} ({d}%)",
            label_outside: bool = False,
            label_outside_formatter: str = "{b}: {c} ({d}%)",
            center_on_hover: bool = False,
            center_label_formatter: str = "{b}\n{c}",
            center_label_font_size: int = 18,
            center_label_font_weight: str = "bold",

            # overlap avoidance
            avoid_label_overlap: bool = True,

            **kwargs
    ) -> None:
        """
        Renders a Pie/Donut chart with flexible legend & label placement.

        Args:
          df: DataFrame with your data.
          names: Column for slice names.
          values: Column for slice values.
          title: Optional centered title.
          radius: Outer radius or [inner, outer] for donut.
          inner_radius: Shortcut for donut inner radius.
          border_radius: px to round slice edges.
          height: CSS height.

        Legend placement:
          legend_orient: "vertical" or "horizontal".
          legend_left: "left","center","right" or px.
          legend_top: CSS top offset (e.g. "5%" or 20).
          legend_bottom: CSS bottom offset.

        Labeling:
          label_inside: Show labels inside slices.
          label_inside_formatter: Formatter for inside labels.
          label_outside: Show labels outside with guide lines.
          label_outside_formatter: Formatter for outside labels.
          center_on_hover: For donuts, show center label on hover.
          center_label_formatter: Formatter for hover-center label.
          center_label_font_size: Font size for hover-center.
          center_label_font_weight: Font weight for hover-center.

        Overlap avoidance:
          avoid_label_overlap: let ECharts try to prevent label collisions.

        **kwargs** are merged into the root ECharts `option`.

        Examples of nudging the legend to the bottom to clear outside labels:

            # Outside labels + legend at bottom
            ECharts.pie(
                df, names="Category", values="Count",
                title="Outside Labels & Bottom Legend",
                label_outside=True,
                legend_orient="horizontal",
                legend_left="center",
                legend_bottom="5%"       # move legend down
            )

            # Donut with outside labels, rounded corners,
            # legend on top at 10% to clear space
            ECharts.pie(
                df, names="Category", values="Count",
                title="Donut & Top Legend",
                inner_radius="30%", radius="60%",
                border_radius=6,
                label_outside=True,
                legend_orient="horizontal",
                legend_left="center",
                legend_top="10%",        # push legend up
                avoid_label_overlap=True
            )
        """
        # handle donut radii
        if inner_radius is not None:
            radius = [inner_radius, radius] if isinstance(radius, str) else radius

        data = [{"name": str(n), "value": float(v)} for n, v in zip(df[names], df[values])]

        if label_inside:
            lbl = {
                "show": True,
                "position": "inside",
                "formatter": label_inside_formatter,
                "fontSize": label_font_size
            }
            line = {"show": False}
        elif label_outside:
            lbl = {
                "show": True,
                "position": "outside",
                "formatter": label_outside_formatter,
                "fontSize": label_font_size
            }
            line = {"show": True, "length": 15, "length2": 10}
        else:
            lbl = {"show": False}
            line = {"show": False}

        # build legend dict
        legend_cfg: dict = {"orient": legend_orient, "left": legend_left}
        if legend_top is not None:    legend_cfg["top"] = legend_top
        if legend_bottom is not None: legend_cfg["bottom"] = legend_bottom

        # series config
        series_item = {
            "name": names,
            "startAngle": start_angle,
            "type": "pie",
            "radius": radius,
            "data": data,
            "avoidLabelOverlap": avoid_label_overlap,
            "label": lbl,
            "labelLine": line,
            "emphasis": {
                "label": {
                    "show": center_on_hover,
                    "position": "center",
                    "formatter": center_label_formatter,
                    "fontSize": center_label_font_size,
                    "fontWeight": center_label_font_weight,
                },
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                },
            },
        }
        if border_radius:
            series_item.setdefault("itemStyle", {})["borderRadius"] = border_radius

        # assemble option
        option = {
            **({"title": {"text": title, "left": "center"}} if title else {}),
            "tooltip": {"trigger": "item",
                        "confine": True,
                        "formatter": "{b}: {c} ({d}%)"},
            "legend": legend_cfg,
            "series": [series_item],
            **kwargs,
        }

        st_echarts(options=option, height=height)

    @staticmethod
    def bar(
            df: pd.DataFrame,
            x: str,
            y: str,
            hue: Optional[str] = None,
            chart_type: Literal["stacked", "grouped"] = "grouped",
            title: Optional[str] = None,
            orientation: Literal["v", "h"] = "v",
            height: str = "400px",

            # styling parameters
            palette: Optional[Sequence[str]] = None,
            use_gradient: bool = False,
            gradient_colors: Sequence[str] = ("#83bff6", "#188df0"),
            bar_max_width: Optional[Union[int, str]] = None,
            bar_border_radius: int = 4,
            show_labels: bool = False,
            label_formatter: str = "{c}",
            label_font_size: int = 12,
            label_color: str = "#333",

            axis_label_rotate: int = 0,
            axis_label_font_size: int = 12,
            axis_label_color: str = "#666",
            show_grid: bool = True,

            **kwargs
    ) -> None:
        """
        Renders a clean Bar chart without animation delay.

        Args:
          df: DataFrame with the data.
          x: Column for the category axis (or value axis if horizontal).
          y: Column for the value axis (or category axis if horizontal).
          hue: Optional grouping column; one series per unique value if provided.
          chart_type: 'grouped' or 'stacked'.
          title: Optional chart title.
          orientation: 'v' for vertical, 'h' for horizontal bars.
          height: CSS height of the chart.

          palette: List of colors for each series.
          use_gradient: Whether to apply a vertical gradient fill.
          gradient_colors: Two colors defining the gradient.
          bar_max_width: Maximum width of bars (px or '%').
          bar_border_radius: Corner rounding in pixels.
          show_labels: If True, show data labels on bars.
          label_formatter: Formatter for labels (default '{c}').
          label_font_size: Font size for data labels.
          label_color: Color for data labels.

          axis_label_rotate: Rotation angle (deg) for axis labels.
          axis_label_font_size: Font size for axis labels.
          axis_label_color: Color for axis labels.
          show_grid: Whether to show horizontal grid lines.

          **kwargs: Any additional ECharts options to merge in.
        """
        # Prepare axes
        if orientation == "v":
            cat_axis = {"type": "category"}
            val_axis = {"type": "value"}
            label_pos = "top"
        else:
            cat_axis = {"type": "value"}
            val_axis = {"type": "category"}
            label_pos = "right"

        series_list = []
        legend_items = []

        # Build data series
        if hue:
            pivot = df.groupby([x, hue])[y].sum().unstack(fill_value=0)
            cat_axis["data"] = pivot.index.astype(str).tolist()
            for lvl in pivot.columns:
                data = pivot[lvl].tolist()
                item = {
                    "name": str(lvl),
                    "type": "bar",
                    "data": data,
                    "label": {
                        "show": show_labels,
                        "position": label_pos,
                        "formatter": label_formatter,
                        "fontSize": label_font_size,
                        "color": label_color,
                    },
                    "barBorderRadius": bar_border_radius,
                }
                if chart_type == "stacked":
                    item["stack"] = "total"
                if bar_max_width:
                    item["barMaxWidth"] = bar_max_width
                if use_gradient:
                    item["itemStyle"] = {
                        "color": {
                            "type": "linear",
                            "x": 0, "y": 0, "x2": 0, "y2": 1,
                            "colorStops": [
                                {"offset": 0, "color": gradient_colors[0]},
                                {"offset": 1, "color": gradient_colors[1]},
                            ],
                        },
                        "shadowBlur": 8,
                        "shadowColor": "rgba(0, 0, 0, 0.2)",
                    }
                series_list.append(item)
                legend_items.append(str(lvl))
        else:
            categories = df[x].astype(str).tolist() if orientation == "v" else df[y].astype(str).tolist()
            values = df[y].tolist() if orientation == "v" else df[x].tolist()
            cat_axis["data"] = categories
            item = {
                "name": y if orientation == "v" else x,
                "type": "bar",
                "data": values,
                "label": {
                    "show": show_labels,
                    "position": label_pos,
                    "formatter": label_formatter,
                    "fontSize": label_font_size,
                    "color": label_color,
                },
                "barBorderRadius": bar_border_radius,
            }
            if bar_max_width:
                item["barMaxWidth"] = bar_max_width
            if use_gradient:
                item["itemStyle"] = {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": gradient_colors[0]},
                            {"offset": 1, "color": gradient_colors[1]},
                        ],
                    },
                    "shadowBlur": 8,
                    "shadowColor": "rgba(0, 0, 0, 0.2)",
                }
            series_list = [item]

        # Assemble option without any animation delay logic
        option = {
            **({"title": {"text": title, "left": "center"}} if title else {}),
            **({"legend": {"data": legend_items}} if hue else {}),
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            **({"color": list(palette)} if palette else {}),
            "grid": {"left": "10%", "right": "10%", "bottom": "15%", "containLabel": True},
            "xAxis": {
                **cat_axis,
                "axisLabel": {
                    "interval": 0,
                    "rotate": axis_label_rotate,
                    "fontSize": axis_label_font_size,
                    "color": axis_label_color,
                },
                "axisTick": {"show": False},
                "axisLine": {"lineStyle": {"color": "#ccc"}},
            },
            "yAxis": {
                **val_axis,
                "axisLabel": {"fontSize": axis_label_font_size, "color": axis_label_color},
                "splitLine": {"show": show_grid, "lineStyle": {"color": "#eee"}},
            },
            "series": series_list,
            **{k: v for k, v in kwargs.items() if v is not None}
        }

        st_echarts(options=option, height=height)

    @staticmethod
    def radar(
            indicators: Sequence[dict],
            data: Sequence[Sequence[float]],
            series_names: Optional[Sequence[str]] = None,
            title: Optional[str] = None,
            height: str = "400px",
            **kwargs
    ) -> None:
        """
        Renders a Radar chart.

        Args:
          indicators: List of {name: <axis name>, max: <axis max>}.
          data: List of value-lists; each sublist matches indicators.
          series_names: Optional names for each data series.
          title: Chart title (centered).
          height: CSS height of chart container.
          **kwargs: Any additional ECharts option overrides.
        """
        series_data = []
        for i, vals in enumerate(data):
            name = series_names[i] if series_names else f"Series {i + 1}"
            series_data.append({"value": vals, "name": name})

        option = {
            **({"title": {"text": title, "left": "center"}} if title else {}),
            "tooltip": {
                "confine": True
            },
            "radar": {"indicator": list(indicators)},
            "series": [{
                "type": "radar",
                "data": series_data,
                'itemStyle': {
                    # 'color': '#F9713C' # this will make all the trials the same color
                },
                "areaStyle": {
                    "opacity": 0.2
                }
            }
            ],
            **kwargs,
        }

        st_echarts(options=option, height=height)

    @staticmethod
    def kde(
            df: pd.DataFrame,
            column: str,
            hue: Optional[str] = None,
            title: Optional[str] = None,
            title_top: str = '5%',
            legend_top: str = '12%',
            height: str = "400px",
            bandwidth: Optional[float] = None,
            grid_size: int = 200,
            show_metrics: bool = False,
            annotate_metrics: bool = False,
            annotate_offset: Optional[float] = None,
            annotate_label_offset: int = 10,
            **kwargs
    ) -> None:
        """
        Renders a KDE (kernel density) line chart for a numeric column,
        with each legend entry showing its median.

        Args:
          df: DataFrame with your data.
          column: Numeric column to plot (e.g. "LOS").
          hue: Optional column name to group by (one curve per level).
          title: Chart title (centered).
          height: CSS height of the chart.
          bandwidth: Bandwidth for gaussian_kde (passed to `bw_method`).
          grid_size: Number of x-points at which to evaluate the KDE.
          show_metrics: If True, draws full vertical dashed lines at mean/median.
          annotate_metrics: If True, draws short dashed pointers labeled “Mean: x”/“Median: y”.
          annotate_offset: Horizontal data-unit offset for pointer lines (default 1% of x-span).
          annotate_label_offset: Vertical pixel offset for annotation labels (alternates up/down).
          **kwargs: Any additional ECharts option overrides.
        """
        # 1) Prepare the x grid
        vals_all = df[column].dropna().astype(float).values
        xmin, xmax = vals_all.min(), vals_all.max()
        xs = np.linspace(xmin, xmax, grid_size)

        def get_metrics(vals: np.ndarray):
            out = {'mean': float(vals.mean()), 'median': float(np.median(vals))}
            return out

        def build_markline_data(vals: np.ndarray, ys: np.ndarray):
            entries = []
            offs_x = annotate_offset if annotate_offset is not None else (xmax - xmin) * 0.01
            metrics = get_metrics(vals)
            for idx, (m, x) in enumerate(metrics.items()):
                label = f"{m.capitalize()}: {x:.1f}"
                # full vertical line
                if show_metrics:
                    entries.append({"name": label, "xAxis": x})
                # horizontal pointer + bold label
                if annotate_metrics:
                    i = np.abs(xs - x).argmin()
                    y = float(ys[i])
                    y_off = annotate_label_offset * (1 if idx % 2 else -1)
                    entries.append([
                        {"coord": [x, y]},
                        {
                            "coord": [x + offs_x, y],
                            "name": label,
                            "label": {
                                "show": True,
                                "formatter": "{b}",
                                "position": "end",
                                "offset": [0, y_off],
                                "fontWeight": "bold"
                            }
                        }
                    ])
            return entries

        # 2) Build each series, baking median into the legend name
        series_list = []
        legend_data = []
        groups = df.groupby(hue) if hue else [(None, df)]
        for lvl, sub in groups:
            arr = sub[column].dropna().astype(float).values
            if len(arr) < 2:
                continue

            # compute KDE
            kde = gaussian_kde(arr, bw_method=bandwidth)
            ys = kde(xs)

            # compute metrics
            metrics = get_metrics(arr)
            med = metrics['median']
            # bake median into series name
            base_name = str(lvl) if hue else column
            series_name = f"{base_name} (Median: {med:.1f} days)"

            cfg = {
                "name": series_name,
                "type": "line",
                "smooth": True,
                "data": list(zip(xs.tolist(), ys.tolist())),
                "showSymbol": False,
            }
            # optional vertical lines & pointers
            if show_metrics or annotate_metrics:
                cfg["markLine"] = {
                    "symbol": ["none", "none"],
                    "lineStyle": {"type": "dashed", "opacity": 0.4},
                    "data": build_markline_data(arr, ys)
                }

            series_list.append(cfg)
            if hue:
                legend_data.append(series_name)

            # 3) Assemble the option

            # **({"title": {"text": title, "left": "center"}} if title else {}),
            # **({"legend": {"data": legend_data}} if hue else {}),
            # Build title + legend with adjustable tops
            title_cfg = {'text': title, 'left': 'center', 'top': title_top} if title else {}
            legend_cfg = {'data': legend_data, 'orient': 'horizontal', 'left': 'center',
                          'top': legend_top} if hue else {}

            option = {
                **({"title": title_cfg} if title_cfg else {}),
                **({'legend': legend_cfg} if legend_cfg else {}),
                "tooltip": {'show': False, "trigger": "axis", "axisPointer": {"type": "line"}},
                "xAxis": {"type": "value", "name": column},
                "yAxis": {"type": "value", "name": "Density"},
                "series": series_list,
                **kwargs
            }

        st_echarts(options=option, height=height)

    @staticmethod
    def histogram(
            df: pd.DataFrame,
            column: str,
            bins: int = 10,
            density: bool = False,
            title: Optional[str] = None,
            height: str = "400px",
            **kwargs
    ) -> None:
        """
        Renders a Histogram as a bar chart.

        Args:
          df: DataFrame with your data.
          column: Numeric column to bin.
          bins: Number of bins.
          density: If True, show density instead of counts.
          title: Chart title (centered).
          height: CSS height of chart container.
          **kwargs: Any additional ECharts option overrides.
        """
        vals = df[column].dropna().astype(float).values
        counts, edges = np.histogram(vals, bins=bins, density=density)
        labels = [f"{edges[i]:.1f}–{edges[i + 1]:.1f}" for i in range(len(counts))]

        option = {
            **({"title": {"text": title, "left": "center"}} if title else {}),
            "tooltip": {"trigger": "axis", "formatter": "{b}: {c}"},
            "xAxis": {"type": "category", "data": labels, "name": column},
            "yAxis": {"type": "value", "name": "Density" if density else "Count"},
            "series": [{
                "type": "bar",
                "data": counts.tolist(),
            }],
            **kwargs,
        }

        st_echarts(options=option, height=height)

    @staticmethod
    def text_stroke_animation(
            text: str,
            font_size: int = 80,
            font_weight: str = "bold",
            stroke_color: str = "#000",
            stroke_width: int = 1,
            line_dash: Sequence[int] = (0, 200),
            fill_color: str = "transparent",
            duration: int = 3000,
            loop: bool = True,
            position: Optional[dict] = None,
            height: str = "400px",
            **kwargs
    ) -> None:
        """
        Renders a stroke-reveal text animation matching the ECharts graphic-stroke-animation example.

        Args:
          text: Text to animate.
          font_size: Font size in px.
          font_weight: CSS font weight (e.g., 'bold').
          stroke_color: Outline color of the text.
          stroke_width: Outline thickness in px.
          line_dash: [dashLen, gapLen] pattern for the stroke.
          fill_color: Initial fill color (default 'transparent').
          duration: Duration of one animation cycle in ms.
          loop: Whether to loop the animation.
          position: Placement dict (e.g. {'left':'center','top':'center'}); defaults to center.
          height: CSS height of the chart container.
          **kwargs: Additional ECharts option overrides.
        """
        # Default to centered positioning
        if position is None:
            position = {"left": "center", "top": "center"}

        # Create the graphic text element with stroke and dash animation
        elem = {
            "type": "text",
            **position,
            "style": {
                "text": text,
                "fontSize": font_size,
                "fontWeight": font_weight,
                "lineDash": list(line_dash),
                "lineDashOffset": 0,
                "fill": fill_color,
                "stroke": stroke_color,
                "lineWidth": stroke_width
            },
            "keyframeAnimation": {
                "duration": duration,
                "loop": loop,
                "keyframes": [
                    {
                        "percent": 0.7,
                        "style": {
                            "fill": fill_color,
                            "lineDashOffset": line_dash[1],
                            "lineDash": [line_dash[1], 0]
                        }
                    },
                    {
                        "percent": 0.8,
                        "style": {"fill": fill_color}
                    },
                    {
                        "percent": 1,
                        "style": {"fill": stroke_color}
                    }
                ]
            }
        }

        # Assemble the option with the graphic element
        option = {"graphic": {"elements": [elem]}, **kwargs}

        st_echarts(options=option, height=height)

    @staticmethod
    def sunburst(
            df: pd.DataFrame,
            path: list[str],
            values: str,
            title: str = "Sunburst Monochrome",
            radius: list[str] | None = None,
            center: list[str] | None = None,
            base_color: str = "#5470C6",
            height: str = "500px",
            **kwargs
    ) -> None:
        """
        Renders a monochrome-style Sunburst chart and labels each slice with its value.

        Args:
          df: DataFrame source.
          path: Hierarchy columns, root→leaf.
          values: Numeric column for slice sizes.
          title: Chart title.
          radius: [inner, outer] radii (e.g. ['20%','75%']).
          center: [x,y] center position (e.g. ['50%','50%']).
          base_color: Hex base color—child slices get progressively lighter.
          height: Container height.
          **kwargs: Other ECharts options to merge.

        Example:
            ECharts.sunburst(
                df,
                path=["Continent","Country","City"],
                values="Population",
                base_color="#c23531",
                radius=["20%","80%"]
            )
        """
        import colorsys

        # defaults
        radius = radius or ["20%", "75%"]
        center = center or ["50%", "50%"]

        # build tree
        tree: dict = {}
        for _, row in df.iterrows():
            node = tree
            for lvl in path:
                key = row[lvl] if pd.notna(row[lvl]) else "<NA>"
                if key not in node:
                    node[key] = {"__value": 0, "__children": {}}
                node[key]["__value"] += float(row[values])
                node = node[key]["__children"]

        def build_nodes(subtree: dict, depth: int = 0) -> list:
            out = []
            for name, meta in subtree.items():
                item = {
                    "name": name,
                    "value": meta["__value"],
                    "itemStyle": {
                        # compute a lighter variant per depth
                        "color": lighten_hex(base_color, depth / (len(path)))
                    },
                    "label": {
                        "formatter": "{b}: {c}",
                        "rotate": "radial"
                    }
                }
                children = build_nodes(meta["__children"], depth + 1)
                if children:
                    item["children"] = children
                out.append(item)
            return out

        data = build_nodes(tree)

        option = {
            "title": {"text": title, "left": "center"},
            "series": [{
                "type": "sunburst",
                "radius": radius,
                "center": center,
                "data": data,
                "label": {"rotate": "radial"}
            }],
            **kwargs
        }

        st_echarts(options=option, height=height)

    @staticmethod
    def sankey_multi(
            df: pd.DataFrame,
            levels: Sequence[str],
            value: str,
            node_width: Union[int, str] = 20,
            node_gap: int = 8,
            layout: Literal["none", "orthogonal"] = "none",
            orient: Literal["horizontal", "vertical"] = "horizontal",
            emphasis: Optional[dict] = None,
            height: str = "400px",
            **kwargs
    ) -> None:
        """
        Draw an N-stage Sankey diagram using ECharts via Streamlit.

        Parameters
        ----------
        df : pd.DataFrame
            Your raw data, containing one column per "level" and a numeric flow column.
        levels : Sequence[str]
            Ordered list of column names in `df` that define each stage of the flow.
            e.g. ["Country", "Region", "City", "Store"].
        value : str
            Column name in `df` containing the numeric weight of each record.
        node_width : int or str, default 20
            Width of each node (px or percent string).
        node_gap : int, default 8
            Gap in px between adjacent nodes.
        layout : {"none", "orthogonal"}, default "none"
            - "none": straight-line connections
            - "orthogonal": right-angled links
        orient : {"horizontal", "vertical"}, default "horizontal"
            Chart orientation.
        emphasis : dict, optional
            ECharts emphasis settings, e.g. {"focus":"adjacency"} to highlight connected flows.
        height : str, default "400px"
            CSS height for the chart container.
        **kwargs
            Any other top-level ECharts option entries to merge in, e.g.
            `backgroundColor`, custom `tooltip`, `series[0].color`, etc.

        Behavior
        --------
        1. **Aggregate** – For each adjacent pair in `levels`, sums `value` by (src, tgt).
        2. **Nodes** – Collects the unique union of all level values.
        3. **Links** – Builds the ECharts-style `{"source":…, "target":…, "value":…}` list.
        4. **Render** – Calls `st_echarts(option, height=height)`.

        Example
        -------
        ```python
        ECharts.sankey_multi(
            df=my_df,
            levels=["L1","L2","L3","L4"],
            value="amount",
            node_width=18,
            node_gap=12,
            layout="orthogonal",
            orient="vertical",
            emphasis={"focus":"adjacency"},
            height="600px",
            tooltip={"trigger":"item","formatter":"{b}: {c}"}
        )
        ```
        """
        # 1) build aggregated links for each adjacent pair of levels
        links = []
        for src_col, tgt_col in zip(levels, levels[1:]):
            grouped = (
                df
                .groupby([src_col, tgt_col], as_index=False)[value]
                .sum()
            )
            for _, row in grouped.iterrows():
                links.append({
                    "source": str(row[src_col]),
                    "target": str(row[tgt_col]),
                    "value": float(row[value])
                })

        # 2) collect all unique node names across every level
        unique_nodes = pd.unique(df[levels].values.ravel())
        nodes = [{"name": str(n)} for n in unique_nodes]

        # 3) assemble the full ECharts option
        option = {
            "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
            "series": [{
                "type": "sankey",
                "layout": layout,
                "orient": orient,
                "data": nodes,
                "links": links,
                "nodeWidth": node_width,
                "nodeGap": node_gap,
                **({"emphasis": emphasis} if emphasis is not None else {})
            }],
            **kwargs,
        }

        # 4) render via Streamlit
        st_echarts(options=option, height=height)
