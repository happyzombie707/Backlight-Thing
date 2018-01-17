#!/bin/python

import sys
from enum import Enum
import re

#mode enum
class Mode(Enum):
    INC = 0
    DEC = 1
    SET = 2
    READ = 3

#clamp a value between a minimum and a maximum
def clamp(n, n_min, n_max):
    return max(n_min, min(n, n_max))

#display help text
def show_help():
    print("Backlight help:\n"+
          "\t-i  -  increment backlight\n"+
          "\t-d  -  decrement backlight\n"+
          "\t-r  -  display current value\n"+
          "\t-s  -  set backlight\n"+
          "\nExamples:\n"+
          "\t\x1B[3mValues must be a percentage or an integer.\x1B[23m\n"+
          "\tbacklight -i 100  -  increase by 100\n" +
          "\tbacklight -d 10%%  -  decrease by 10%\n"+
          "\tbacklight -s 50%%  -  set to 50%\n")

    sys.exit(0)

#sets backlight to th new value
def set_brightness(new_value):

    #open file, write new value and close
    backlight_file = open("/sys/class/backlight/intel_backlight/brightness", "w")
    backlight_file.write(repr(new_value) + "\n")
    backlight_file.close()


#process change value
def parse_value(val, mode):

    #find current brightness
    current_backlight_file = open("/sys/class/backlight/intel_backlight/brightness", "r")
    current_backlight = int(current_backlight_file.read())
    current_backlight_file.close()

    #if in read mode
    if mode == mode.READ:
        print repr(current_backlight)    #print current brightness
        sys.exit(0)  #exit

    #find max brightness
    max_backlight_file = open("/sys/class/backlight/intel_backlight/max_brightness", "r")
    max_backlight = int(max_backlight_file.read())
    max_backlight_file.close()

    #set up variabls to store whether value given is a % and the change in brightness
    is_percentage = False
    change = 0

    #if value is a %, remove % sign and set flag
    if "%" in val:
        val = val.strip('%')
        is_percentage = True

    #if it's a % set the change to be a percentage of the max value
    if is_percentage:
        change = max_backlight * int(val) / 100
    #else set change to be the given value (absolute)
    else:
        change = int(val)

    #if inc set backlight to current + change
    if mode == mode.INC:
        set_brightness(clamp(current_backlight + change, 0, max_backlight))
    #if dec set to current - change
    elif mode == mode.DEC:
        set_brightness(clamp(current_backlight - change, 0, max_backlight))
    #if absolute set to change
    elif mode == mode.SET:
        set_brightness(clamp(change, 0, max_backlight))
    #if for some reason the above don't work set to half of the max
    else:
        set_brightness(max_backlight / 2)


#processes command arument (-i, -d etc)
def process_command():
    argc = len(sys.argv)
    #help
    if sys.argv[1].lower() == "-h":
        show_help()
    #read brightness
    elif sys.argv[1].lower() == "-r":
        parse_value(-1, Mode.READ)
    #invalud argument
    elif len(sys.argv) != 3 or not re.match('^\d+%?$', sys.argv[2]):
        print "Invalid arguments, use -h for help."
        return
    #increment brightness
    elif sys.argv[1].lower() == "-i":
        mode = Mode.INC
    #decrement brightness
    elif sys.argv[1].lower() == "-d":
        mode = Mode.DEC
    #set brightness
    elif sys.argv[1].lower() == "-s":
        mode = Mode.SET

    #anything else
    else:
        print "Invalid arguments, use -h for help."
        return

    #parse value (2nd argument),  mode provided to calculate new brightness value
    parse_value(sys.argv[2], mode)
#main function
def main():
    #call process command function
    process_command()

#begin
if __name__ == "__main__":
    main()
