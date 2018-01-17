### Backlight.py
Command line tool to change backlight brightness.
Only works with intel graphics, only tested on Fedora 27.

* -i  -  increment backlight
* -d  -  decrement backlight
* -r  -  display current value
* -s  -  set backlight

#### Examples:
_Values must be a percentage or an integer._
* backlight -i 100  -  increase by 100
* backlight -d 10%%  -  decrease by 10%
* backlight -s 50%%  -  set to 50%
