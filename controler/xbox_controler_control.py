from time import sleep
from approxeng.input.controllers import find_matching_controllers, ControllerRequirement
from approxeng.input.selectbinder import bind_controllers
import redboard

discovery = None

# Connect to controler
while discovery is None:
    try:
        discovery = find_matching_controllers(
            ControllerRequirement(require_snames=["lx", "ly"])
        )[0]
    except IOError:
        print("No suitable controller found yet")
        sleep(0.5)


# Bind the controller to the function
unbind_function = bind_controllers(discovery, print_events=False)

# Set LED colour
redboard.RedBoard._set_led_rgb(0, 0, 255)


try:
    for lx, ly in discovery.controller.stream["lx", "ly"]:
        print("Left stick: x={}, y={}".format(lx, ly))
        if lx > 0:
            motor1 = 100 * lx
            motor2 = -100 * lx
            redboard.M1(motor1)
            redboard.M2(motor2)
        if lx < 0:
            motor1 = -100 * lx
            motor2 = 100 * lx
            redboard.M1(motor1)
            redboard.M2(motor2)
        if ly > 0:
            motor1 = 100 * ly
            motor2 = 100 * ly
            redboard.M1(motor1)
            redboard.M2(motor2)
        if ly < 0:
            motor1 = -100 * ly
            motor2 = -100 * ly
            redboard.M1(motor1)
            redboard.M2(motor2)
        # check for the stop button
        if discovery.controller.has_presses("cross"):
            print("Stop")
            motor1 = 0
            motor2 = 0
            redboard.M1(motor1)
            redboard.M2(motor2)
        sleep(0.1)
except StopIteration:
    # Raised when the stream ends
    print("Controller disconnected")
    pass

# Clean up
unbind_function()
