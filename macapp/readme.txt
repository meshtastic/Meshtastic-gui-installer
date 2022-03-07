Thanks to Discord user jasonwindsor for the tip of using Automator for this.

Steps used to create it:
- use Automator to create a script that runs from bash
- run/save (this creates in /Applications)
- Sign (where XXX is the cert used in signing)
  codesign --force --options runtime --deep --sign "XXX" "/Applications/Meshtastic-flasher.app/"
- Validate signed
  codesign -dv --verbose=4 "/Applications/Meshtastic-flasher.app/"
- update icon
  Downloaded logo from meshtastic-design
  Open login in preview, highlight all, copy
  Open .app in Finder, show info, right click on upper left image, control-v
- zip up the .app and publish to release manually - this app should not change very often
