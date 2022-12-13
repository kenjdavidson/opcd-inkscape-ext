# OPCD Inkscape Extensions

A couple helper extensions for working with OPCD files within inkscape.  For more information on the inkscape/OPCD process check out https://www.youtube.com/@GolfCourseDesign/playlists?view=50&sort=dd&shelf_id=4.

## Install

Download the package and unzip it to your Inkscape extensions directory.  Since the OPCD tools are designed for Windows, you're most likely going to be in `C:\Users\User\AppData\Roaming\inkscape\extensions`.

## Extensions

### Export No Sat

Right off the hop, the one process that gets super tedious is saving the no-sat version and then running it through the conversion tool.

> Under the menu `Extensions` > `OPCD` > `Export No Sat`

#### Configuration

The options are available:

**Layer Name** - by default this is `Satellite`, change this to your name.

**Export Path** - where your file should be saved.  This should also be the same directory as the `GSProSVGConvert` tool.

> This could probably be made into another option

**Run Conversion** - if for some reason you don't want to run conversion after export, uncheck this.

**Debug Messages** - if anything goes wrong, turn on the debugging.

## Contributing

By no means do I fancy myself a **Python** developer - which means these are super crude.  Feel free to throw some corrections or ideas in.