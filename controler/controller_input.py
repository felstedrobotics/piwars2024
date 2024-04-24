import curses
from time import sleep

from approxeng.input.controllers import ControllerRequirement, find_matching_controllers
from approxeng.input.selectbinder import bind_controllers

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

stdscr = curses.initscr()  # Initialize curses
curses.noecho()  # Turn off automatic echoing of keys to the screen
curses.cbreak()  # React to keys instantly, without requiring the Enter key
stdscr.keypad(True)  # Enable special keys


def main(stdscr):
    motor1 = 0
    motor2 = 0

    while True:
        stdscr.clear()
        try:
            for lx, ly, rx, ry in discovery.controller.stream["lx", "ly", "rx", "ry"]:
                stdscr.addstr(0, 0, "Left stick: x={}, y={}".format(lx, ly))
                stdscr.addstr(1, 0, "Right stick: x={}, y={}".format(rx, ry))

                presses = (
                    discovery.controller.check_presses()
                )  # Check for button presses

                if "cross" in presses:
                    stdscr.addstr(2, 0, "Cross pressed")
                if "circle" in presses:
                    stdscr.addstr(3, 0, "Circle pressed")
                if "triangle" in presses:
                    stdscr.addstr(4, 0, "Triangle pressed")
                if "square" in presses:
                    stdscr.addstr(5, 0, "Square pressed")

                stdscr.addstr(6, 0, "RT pressed, {}".format(discovery.controller.r2))

                stdscr.addstr(7, 0, "LT pressed, {}".format(discovery.controller.l2))
                if "r1" in presses:
                    stdscr.addstr(8, 0, "RB pressed")
                if "l1" in presses:
                    stdscr.addstr(9, 0, "LB pressed")

                stdscr.refresh()

                if ly > 0.05:  # the deadzone
                    motor1 += 100 * ly
                    motor2 -= 100 * ly
                if ly < 0.05:  # the deadzone
                    motor1 -= -100 * ly
                    motor2 += -100 * ly

                # Control motors based on right joystick
                if ry > 0.05:  # the deadzone
                    motor1 += 100 * rx
                    motor2 += 100 * rx
                if ry < 0.05:  # the deadzone
                    motor1 -= 100 * rx
                    motor2 -= 100 * rx

                sleep(0.1)
                motor1 = 0
                motor2 = 0
        except StopIteration:
            # Raised when the stream ends
            print("Controller disconnected")
            pass
        except KeyboardInterrupt:
            # Raised when the user presses Ctrl+C
            print("Exiting...")
            sleep(0.1)
            break


curses.wrapper(main)

# Clean up
unbind_function()
