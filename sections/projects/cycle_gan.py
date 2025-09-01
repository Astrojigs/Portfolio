from __future__ import annotations

import io
from functools import lru_cache
from typing import Dict, List

import requests
from PIL import Image
import streamlit as st

from core.utils import custom_write


@lru_cache(maxsize=32)
def load_image_from_url(url: str) -> Image.Image:
    """Fetch an image from a remote URL and return it as a PIL Image.

    The function is cached to reduce latency when the same image is
    requested multiple times.  If the download fails, a placeholder
    image with a descriptive error message is returned.

    Args:
        url: The raw GitHub URL pointing to the image.

    Returns:
        A PIL Image object containing the requested image.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as exc:  # pylint: disable=broad-except
        # Create a simple placeholder image with an error message
        placeholder = Image.new("RGB", (512, 384), color=(240, 240, 240))
        error_text = f"Failed to load image\n{exc}"[:100]
        try:
            from PIL import ImageDraw, ImageFont

            draw = ImageDraw.Draw(placeholder)
            draw.text((10, 10), error_text, fill=(255, 0, 0))
        except Exception:
            pass
        return placeholder


def introduction_section() -> None:
    """Render the introduction section of the app."""
    st.header("Introduction")
    st.write(
        rf"""
        Converting **aerial photographs** into map‑style renderings is a
        challenging computer vision problem.  Unlike classical supervised
        learning tasks, there is rarely a one‑to‑one correspondence between
        aerial pictures and their map representations.  To bridge this
        gap, the CycleGAN algorithm learns *bidirectional* mappings between
        two domains using **unpaired** training data.  It trains two
        generator networks $(G: X \rightarrow Y)$ and $(F: Y \rightarrow X)$ and
        two discriminators that judge how well the generators fool them.
        The cycle consistency constraint encourages compositions of the
        generators to reproduce the original image.  This project applies
        CycleGAN to translate satellite photographs into simplified map
        images using a dataset from Kaggle.
        """
    )
    st.page_link(page="https://www.kaggle.com/datasets/suyashdamle/cyclegan", label=":blue[Link to Dataset]",
                 icon=":material/link:")
    st.page_link(page="https://github.com/Astrojigs/Aerial-images-to-maps", label=":orange[GitHub Repository]",
                 icon=":material/link:")

def dataset_section(aerial_url: str, map_url: str) -> None:
    """Render the dataset section with example images.

    Args:
        aerial_url: URL of a sample aerial photograph.
        map_url: URL of the corresponding map representation.
    """
    st.header("Dataset Overview")
    st.write(
        """
        The dataset contains **unpaired** images of aerial photographs and
        their corresponding map representations.  Because the images are
        unpaired, the network does not learn from direct pixelwise
        differences but instead relies on adversarial losses and cycle
        consistency.  The following side‑by‑side example illustrates the
        two domains used during training.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image(load_image_from_url(aerial_url), caption="Aerial photograph", use_container_width=True)
    with col2:
        st.image(load_image_from_url(map_url), caption="Map representation", use_container_width=True)

    st.info(
        """
        The images above come from the [CycleGAN dataset on Kaggle](https://www.kaggle.com/datasets/suyashdamle/cyclegan),
        which provides unpaired collections of aerial and map images.
        Models were trained on images resized to **128×128** and **256×256** pixels.
        """
    )


def architecture_section(generator_url: str, discriminator_url: str) -> None:
    """Render the model architecture diagrams.

    Args:
        generator_url: URL of the generator architecture diagram.
        discriminator_url: URL of the discriminator architecture diagram.
    """
    st.header("Model Architecture")
    st.write(
        """
        The CycleGAN framework uses two generator networks and two
        discriminators.  Each generator is a deep convolutional neural
        network built with down‑sampling and up‑sampling layers to convert
        images from one domain to the other.  The discriminators are
        patch‑based convolutional classifiers that evaluate whether a
        generated image looks like a real sample from the target domain.
        The diagrams below illustrate the overall architecture of the
        networks used in this project.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Generator")
        with st.container(height=500):
            st.image(load_image_from_url(generator_url), use_container_width=True)
    with col2:
        st.subheader("Discriminator")
        with st.container(height=500):
            st.image(load_image_from_url(discriminator_url), use_container_width=True)


def losses_section() -> None:
    """Render the loss functions and equations."""
    st.header("Loss Functions")
    st.write(
        """
        Training a CycleGAN involves multiple objective terms.  The
        **adversarial loss** encourages the generators to produce
        photorealistic outputs that fool the discriminators.  For a
        discriminator \\(D\\) and generator \\(G\\) the adversarial losses can be
        written as:
        """
    )
    st.latex(
        r"\mathcal{L}_D = \tfrac{1}{2}\,\mathbb{E}_{x \sim p_{\text{data}}}\big[\big(D(x)-1\big)^2\big] + "
        r"\tfrac{1}{2}\,\mathbb{E}_{z \sim p_z}\big[D\big(G(z)\big)^2\big]"
    )
    st.latex(
        r"\mathcal{L}_G^{\text{adv}} = \mathbb{E}_{z \sim p_z}\big[\big(D\big(G(z)\big)-1\big)^2\big]"
    )
    st.write(
        """
        In our implementation we use the binary cross entropy variant of
        these losses as described in the TensorFlow CycleGAN tutorial.

        Because training pairs are not available, we include a
        **cycle‑consistency loss** that forces the composition of the two
        generators to reconstruct the original image.  Forward and
        backward cycle consistency losses are computed as the mean
        backward cycle consistency losses are computed as the mean
        absolute error between the input image and its reconstruction:
        """
    )
    st.latex(
        r"\mathcal{L}_{\text{cycle}} = \mathbb{E}_{x \sim p_X} \big[ \|F(G(x)) - x\|_1 \big] + "
        r"\mathbb{E}_{y \sim p_Y} \big[ \|G(F(y)) - y\|_1 \big]"
    )
    st.write(
        """
        Finally, the **identity loss** encourages each generator to preserve
        images that already belong to the target domain.  If we pass a map
        image through the aerial‑to‑map generator \\(G\\) or an aerial image
        through the inverse generator \\(F\\) the outputs should remain
        unchanged:
        """
    )
    st.latex(
        r"\mathcal{L}_{\text{id}} = \mathbb{E}_{y \sim p_Y} \big[ \|G(y) - y\|_1 \big] + "
        r"\mathbb{E}_{x \sim p_X} \big[ \|F(x) - x\|_1 \big]"
    )
    st.write(r"""The full objective combines all terms as""")

    st.latex(
        r"""
        \mathcal{L}_{\text{CycleGAN}}
        = \mathcal{L}_G^{\text{adv}}
        + \mathcal{L}_D
        + \lambda_{\text{cycle}} \, \mathcal{L}_{\text{cycle}}
        + \lambda_{\text{id}} \, \mathcal{L}_{\text{id}}
        """
    )

    st.write(
        r"""
        where the hyper-parameters $\lambda_{\text{cycle}}$ and
        $\lambda_{\text{id}}$ weight the relative importance of each component.
        """
    )


def training_section(loss_curve_url: str, example_results: Dict[int, str]) -> None:
    """Render the training section with curves and result images.

    Args:
        loss_curve_url: URL to an image showing the generator and
            discriminator loss curves over epochs.
        example_results: mapping from epoch number to URL of a composite
            image showing inputs and outputs at that epoch.
    """
    st.header("Training & Results")
    st.write(
        """
        The model was trained using mini‑batch stochastic gradient descent
        with the Adam optimizer.  Loss curves can reveal whether the
        adversarial game between generators and discriminators stabilizes.
        Below is an example of the generator and discriminator losses for
        one of the training runs.  You can interactively explore
        qualitative results from different epochs using the slider beneath
        the plot.
        """
    )
    st.image(load_image_from_url(loss_curve_url), caption="Loss curves", use_container_width=True)

    # Epoch slider and image display
    if example_results:
        epoch_numbers = sorted(example_results.keys())
        default_idx = len(epoch_numbers) - 1  # default to the last epoch
        selected_epoch = st.slider(
            "Select an epoch to view example translations",
            min_value=int(epoch_numbers[0]),
            max_value=int(epoch_numbers[-1]),
            value=int(epoch_numbers[default_idx]),
            step=epoch_numbers[1] - epoch_numbers[0] if len(epoch_numbers) > 1 else 1,
        )
        # Find the nearest epoch available
        nearest_epoch = min(epoch_numbers, key=lambda x: abs(x - selected_epoch))
        result_image = load_image_from_url(example_results[nearest_epoch])
        st.image(
            result_image,
            caption=f"CycleGAN results after {nearest_epoch} training epochs",
            use_container_width=True,
        )

    st.write(
        """
        The composite images above show a set of aerial photographs (top row)
        followed by their generated maps (bottom row) for the selected
        epoch.  Early in training the outputs are noisy and lack
        structure, but they gradually learn to capture roads, fields and
        other geographic features as training progresses.
        """
    )


def conclusion_section() -> None:
    """Render the conclusion and future work section."""
    st.header("Conclusion")
    st.write(
        """
        Using CycleGAN we successfully translated aerial imagery into
        simplified map‑style renderings without requiring paired
        supervision.  The network learns a deep understanding of
        geographical structures by enforcing both adversarial realism and
        cycle consistency.  While the results are promising, there is
        still room for improvement.  Training on higher resolution
        images, experimenting with attention mechanisms, or integrating
        additional semantic information could further enhance the
        quality of the generated maps.

        Thank you for exploring this project!  Feel free to browse the
        source code and notebooks linked in the [GitHub
        repository](https://github.com/Astrojigs/Aerial-images-to-maps)
        for more details.
        """
    )


def render() -> None:
    """Main entry point for the Streamlit application."""
    custom_write("Aerial Images to Maps using CycleGAN", type="h1")

    # Define image URLs used in the app
    base_url = "https://raw.githubusercontent.com/Astrojigs/Aerial-images-to-maps/main/Images"
    aerial_img_url = f"{base_url}/example%20image%20aerial%20-%20Copy.jpg"
    map_img_url = f"{base_url}/example%20image%20map%20-%20Copy.jpg"

    generator_arch_url = f"{base_url}/architectures/generator_common.png"
    discriminator_arch_url = f"{base_url}/architectures/discriminator_architecture_without_shapes.png"

    loss_curve_url = f"{base_url}/loss%20curves/128GAN_bs1_loss_curves.png"
    # Example results at different epochs
    example_results = {
        1: f"{base_url}/example%20images/128GAN_bs1_epoch1_results.png",
        50: f"{base_url}/example%20images/128GAN_bs1_epoch50_results.png",
        75: f"{base_url}/example%20images/128GAN_bs1_epoch75_results.png",
        95: f"{base_url}/example%20images/128GAN_bs1_epoch95_results.png",
    }

    introduction_section()

    dataset_section(aerial_img_url, map_img_url)
    architecture_section(generator_arch_url, discriminator_arch_url)
    losses_section()
    training_section(loss_curve_url, example_results)
    conclusion_section()
