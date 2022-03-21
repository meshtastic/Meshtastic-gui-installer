Install AutoIt

Build/release process:
- after development is done, bump the version in the .au3 script
- Compile to x86 from the SciTE - Lite editor (right click on .au3 file and select "Edit")
- Open ssl.com manager, code signing, sign and timestamp:
    input file is the .exe
    select cert
    ssl.com timestamping service
    "sign"
- zip
- upload zip to release