### Backlight.py
Command line tool to change backlight brightness.
Only works with intel graphics.

* -i  -  increment backlight
* -d  -  decrement backlight
* -r  -  display current value
* -s  -  set backlight

#### Examples:
_Values must be a percentage or an integer._
* `backlight -i 100  -  increase by 100`
* `backlight -d 10% -  decrease by 10%`
* `backlight -s 50%  -  set to 50%`


#### Installing:
To install, move or link the script somewhere in your PATH (e.g. `/usr/bin`)

If desired the systemd service can be used to change the write permission of the backlight file, allowing use without sudo. Move it to the appropriate location and enable the service. 
`# cp backlight-permission.service`
`# systemctl enable backlight-permission.service`
