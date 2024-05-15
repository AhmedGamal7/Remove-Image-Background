import base64
from io import BytesIO
import streamlit as st
from PIL import Image
import rembg


def remove_image_background(image, alpha_matte=True):
    """
    Removes the background of an image using the Rembg library.
        Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the output image file.
        alpha_matte (bool, optional): Whether to include an alpha channel
            representing transparency in the output image. Defaults to False.
        Returns:
        None
    """
    try:
        # Load the image using PIL (Rembg internally uses PIL)
        image = Image.open(image)
        # Use Rembg to remove the background
        output = rembg.remove(image)
        # Optionally add an alpha channel for transparency
        if alpha_matte:
            output = output.convert("RGBA")  # Add alpha channel
            mask = output.getchannel("A")  # Extract alpha mask
            mask = mask.point(
                lambda p: 255 if p > 200 else 0
            )  # Threshold for transparency
            output.putalpha(mask)  # Apply refined alpha mask
            # Save the output image
        output.save("output_path.png")
        print(f"Background removed and image saved to: ")
    except FileNotFoundError:
        print(f"Error: Input image file not found at: ")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_image_download_link(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}">Download Image</a>'
    return href


def main():
    st.title("Image Background Removal")

    # File uploader to get image from user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, width=100, caption="Original Image", use_column_width=True)

        # Remove background
        if st.button("Remove Background"):
            with st.spinner("Removing Background..."):
                result_image = remove_image_background(image)

            # Display processed image
            st.image(
                result_image,
                caption="Image with Background Removed",
                use_column_width=True,
            )

            # Allow user to download processed image
            st.markdown(get_image_download_link(result_image), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
