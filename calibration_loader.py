import re


def load_calibration():
    red_lower = []
    red_upper = []

    green_lower = []
    green_upper = []

    blue_lower = []
    blue_upper = []

    with open("calibration.txt", "r") as f:
        for line in f:
            if re.match("red_lower", line):
                red_lower = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("red_upper", line):
                red_upper = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("green_lower", line):
                green_lower = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("green_upper", line):
                green_upper = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("blue_lower", line):
                blue_lower = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("blue_upper", line):
                blue_upper = re.findall(r"[-+]?\d*\.\d+|\d+", line)

    for i in red_lower:
        i = float(i)
    for i in red_upper:
        i = float(i)
    for i in green_lower:
        i = float(i)
    for i in green_upper:
        i = float(i)
    for i in blue_lower:
        i = float(i)
    for i in blue_upper:
        i = float(i)
    return red_lower, red_upper, green_lower, green_upper, blue_lower, blue_upper
