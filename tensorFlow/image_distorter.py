from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os
import random


def add_red_filter(image_path, output_path):
    # Open the image file
    img = Image.open(image_path)
    img = img.convert("RGB")

    # Split the image into RGB channels
    r, g, b = img.split()

    # Increase the red channel
    r = r.point(lambda i: i * 1.5)

    # Decrease the green and blue channels
    g = g.point(lambda i: i * 0.5)
    b = b.point(lambda i: i * 0.5)

    # Merge the channels back
    img = Image.merge("RGB", (r, g, b))

    # Save the output image
    img.save(output_path)


# add green filter
def add_green_filter(image_path, output_path):
    # Open the image file
    img = Image.open(image_path)
    img = img.convert("RGB")

    # Split the image into RGB channels
    r, g, b = img.split()

    # Increase the green channel
    g = g.point(lambda i: i * 1.5)

    # Decrease the red and blue channels
    r = r.point(lambda i: i * 0.5)
    b = b.point(lambda i: i * 0.5)

    # Merge the channels back
    img = Image.merge("RGB", (r, g, b))

    # Save the output image
    img.save(output_path)


# add blue filter
def add_blue_filter(image_path, output_path):
    # Open the image file
    img = Image.open(image_path)
    img = img.convert("RGB")

    # Split the image into RGB channels
    r, g, b = img.split()

    # Increase the blue channel
    b = b.point(lambda i: i * 1.5)

    # Decrease the red and green channels
    r = r.point(lambda i: i * 0.5)
    g = g.point(lambda i: i * 0.5)

    # Merge the channels back
    img = Image.merge("RGB", (r, g, b))

    # Save the output image
    img.save(output_path)


def distort_image(image_path, output_path, distortion_scale=0.3, brightness_factor=1.2):
    # Open the image file
    img = Image.open(image_path)
    img = img.convert("RGB")

    # Convert to numpy array
    data = np.asarray(img)

    # Create x and y indices
    y, x = np.indices((img.size[1], img.size[0]))

    # Create random distortion
    distortion = (
        np.sin(x / img.size[0] * (2 * np.pi + random.uniform(0, 2 * np.pi)))
        * distortion_scale
    )

    # Apply distortion to y coordinates
    y += distortion.astype(int)

    # Ensure y indices are within bounds
    y = np.clip(y, 0, img.size[1] - 1)

    # Apply distortion to image data
    result = data[y, x]

    # Convert back to Image and enhance brightness
    distorted_img = Image.fromarray(result, "RGB")
    enhancer = ImageEnhance.Brightness(distorted_img)
    distorted_img = enhancer.enhance(brightness_factor)

    # Randomly apply color filter
    color_enhancer = ImageEnhance.Color(distorted_img)
    distorted_img = color_enhancer.enhance(
        random.uniform(0.5, 1.5)
    )  # Random color balance between 0.5 and 1.5

    # Create reflection
    reflection = ImageOps.flip(distorted_img)
    reflection = ImageEnhance.Brightness(reflection).enhance(
        0.5
    )  # Make the reflection darker
    reflection = ImageEnhance.Contrast(reflection).enhance(
        1.5
    )  # Increase the contrast of the reflection
    reflection = ImageOps.flip(reflection)

    # Combine original image and reflection
    final_img = Image.new("RGB", (distorted_img.width, distorted_img.height))
    final_img.paste(reflection, (0, 0))

    # add color filter
    number = random.randint(1, 3)
    if number == 1:
        add_red_filter(image_path, output_path)
    elif number == 2:
        add_green_filter(image_path, output_path)
    else:
        add_blue_filter(image_path, output_path)

    # Save the output image
    final_img.save(output_path)


def process_directory(
    input_dir,
    output_dir,
    num_distorted_images=20,
    min_distortion=0.1,
    max_distortion=2.0,
):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Construct full file path
            input_path = os.path.join(input_dir, filename)

            # Generate multiple distorted versions of the image
            for i in range(num_distorted_images):
                output_path = os.path.join(
                    output_dir,
                    f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}",
                )
                distortion_scale = min_distortion + (
                    max_distortion - min_distortion
                ) * i / (num_distorted_images - 1)
                distort_image(input_path, output_path, distortion_scale)


# Usage
process_directory(
    input_dir="/home/user/repos/piwars/tensorFlow/images/",
    output_dir="/home/user/repos/piwars/tensorFlow/output/",
)
