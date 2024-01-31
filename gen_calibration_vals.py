import os
from PIL import Image

directory = "./config/"
image_files = [
    f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
]

config_file = open("./config/calibration.cfg", "a")

for file_name in image_files:
    image_path = os.path.join(directory, file_name)
    if image_path.endswith(".jpg"):
        image = Image.open(image_path)
        pixels = image.load()

        min_red = 255
        max_red = 0
        min_green = 255
        max_green = 0
        min_blue = 255
        max_blue = 0

        width, height = image.size

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if r < min_red:
                    min_red = r
                if r > max_red:
                    max_red = r
                if g < min_green:
                    min_green = g
                if g > max_green:
                    max_green = g
                if b < min_blue:
                    min_blue = b
                if b > max_blue:
                    max_blue = b

        # write to config file
        if file_name == "calibration_red_1.jpg":
            config_file.write(f"red_lower = [{min_red}, {min_green}, {min_blue}] \n")
            config_file.write(f"red_upper = [{max_red}, {max_green}, {max_blue}] \n")
            config_file.write("\n")
        elif file_name == "calibration_green_1.jpg":
            config_file.write(f"green_lower = [{min_red}, {min_green}, {min_blue}] \n")
            config_file.write(f"green_upper = [{max_red}, {max_green}, {max_blue}] \n")
            config_file.write("\n")
        elif file_name == "calibration_blue_1.jpg":
            config_file.write(f"blue_lower = [{min_red}, {min_green}, {min_blue}] \n")
            config_file.write(f"blue_upper = [{max_red}, {max_green}, {max_blue}] \n")
            config_file.write("\n")
        elif file_name == "calibration_white_1.jpg":
            config_file.write(f"white_lower = [{min_red}, {min_green}, {min_blue}] \n")
            config_file.write(f"white_upper = [{max_red}, {max_green}, {max_blue}] \n")
            config_file.write("\n")
        elif file_name == "calibration_grey_1.jpg":
            config_file.write(f"grey_lower = [{min_red}, {min_green}, {min_blue}] \n")
            config_file.write(f"grey_upper = [{max_red}, {max_green}, {max_blue}] \n")

        print(f"Color value range for {file_name}:")
        print(f"Red: {min_red} - {max_red}")
        print(f"Green: {min_green} - {max_green}")
        print(f"Blue: {min_blue} - {max_blue}")
        print()
