from time import sleep
from approxeng.input.controllers import find_matching_controllers, ControllerRequirement
from approxeng.input.selectbinder import bind_controllers
import redboard
import curses

discovery = None

# Connect to controller
while discovery is None:
    try:
        discovery = find_matching_controllers(
            ControllerRequirement(require_snames=["lx", "ly", "rx", "ry"])
        )[0]
    except IOError:
        print("No suitable controller found yet")
        sleep(0.5)


# Bind the controller to the function
unbind_function = bind_controllers(discovery, print_events=False)

stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(True)


def main(stdscr):
    motor1 = 0
    motor2 = 0

    while True:

        curses.halfdelay(1)

        try:
            for lx, ly, rx, ry in discovery.controller.stream["lx", "ly", "rx", "ry"]:
                print("Left stick: x={}, y={}\n".format(lx, ly))
                print("Right stick: x={}, y={}\n".format(rx, ry))
                if lx > 0:
                    motor1 += 100 * lx
                    motor2 -= 100 * lx
                if lx < 0:
                    motor1 -= 100 * lx
                    motor2 += 100 * lx

                redboard.M1(motor1)
                redboard.M2(motor2)

                # Control motors based on right joystick
                if ry > 0:
                    motor1 += 100 * ry
                    motor2 += 100 * ry
                if ry < 0:
                    motor1 -= 100 * ry
                    motor2 -= 100 * ry

                redboard.M1(motor1)
                redboard.M2(motor2)

                sleep(0.1)
                motor1 = 0
                motor2 = 0
        except StopIteration:
            # Raised when the stream ends
            print("Controller disconnected")
            pass


curses.wrapper(main)

# Clean up
unbind_function()
