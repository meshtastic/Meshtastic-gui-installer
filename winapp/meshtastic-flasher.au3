; meshtastic-flasher install

FileChangeDir(@HomePath)

If Not FileExists("meshtastic-flasher\") Then
	MsgBox("", "test2", "creating dir")
	DirCreate("meshtastic-flasher")
EndIf
FileChangeDir("meshtastic-flasher")

If Not FileExists("venv\") Then
	$CMD = "py -m venv venv"
	RunWait(@ComSpec & " /c " & $CMD)
Endif

$CMD = "venv\Scripts\activate & py -m pip install --upgrade pip & pip install --upgrade meshtastic-flasher & meshtastic-flasher"
RunWait(@ComSpec & " /c " & $CMD)
