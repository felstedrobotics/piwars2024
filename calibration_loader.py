import re


def load_calibration():
    red_lower = []
    red_upper = []

    green_lower = []
    green_upper = []

    blue_lower = []
    blue_upper = []

    white_lower = []
    white_upper = []

    grey_lower = []
    grey_upper = []

    with open("./config/calibration.cfg", "r") as f:
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
            elif re.match("white_lower", line):
                white_lower = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("white_upper", line):
                white_upper = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("grey_lower", line):
                grey_lower = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elif re.match("grey_upper", line):
                grey_upper = re.findall(r"[-+]?\d*\.\d+|\d+", line)

    try:
        for i in red_lower:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in red_upper:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in green_lower:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in green_upper:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in blue_lower:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in blue_upper:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in white_lower:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in white_upper:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in grey_lower:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
        for i in grey_upper:
            i = int(i)
            if len(str(i)) > 3:
                i = i[:3]
    except ValueError:
        print("Error: Calibration values must be integers or floats.")
        exit()
    return (
        red_lower,
        red_upper,
        green_lower,
        green_upper,
        blue_lower,
        blue_upper,
        white_lower,
        white_upper,
        grey_lower,
        grey_upper,
    )
