; meshtastic-flasher WinApp - create python virtual environment and run meshtastic-flasher

#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=meshtastic.ico
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

#pragma compile(UPX, False)
#pragma compile(FileDescription, Meshtastic Flasher WinApp)
#pragma compile(ProductName, Meshtastic Flasher)
#pragma compile(ProductVersion, 1.0.2)
#pragma compile(FileVersion, 1.0.2.0)
#pragma compile(CompanyName, 'Meshtastic.org')

#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>

FileChangeDir(@HomePath)

If Not FileExists("meshtastic-flasher\") Then
	MsgBox("", "Info", "creating dir")
	DirCreate("meshtastic-flasher")
EndIf
FileChangeDir("meshtastic-flasher")

; check if py is a valid command
Local $sPython = "py"
Local $CMD = $sPython & " --version"
Local $iPid = Run(@ComSpec & " /c " & $CMD, @TempDir, @SW_HIDE, $STDOUT_CHILD)

; wait until the process has closed
ProcessWaitClose($iPid)

; read the output from the first python check
Local $sOutput = StdoutRead($iPid)
;MsgBox($MB_SYSTEMMODAL, "Info", "output:" & $sOutput)

; see if we found a valid python3 version
Local $iPosition = StringInStr($sOutput, "Python 3.")
;MsgBox($MB_SYSTEMMODAL, "Info", "iPosition:" & $iPosition)

If $iPosition = 0 Then
	; check if python3 is a valid command
	$sPython = "python3"
	$CMD = $sPython & " --version"
	$iPid = Run(@ComSpec & " /c " & $CMD, @TempDir, @SW_HIDE, $STDOUT_CHILD)

	; wait until the process has closed
	ProcessWaitClose($iPid)

	; read the output from the first python check
	$sOutput = StdoutRead($iPid)
	;MsgBox($MB_SYSTEMMODAL, "Info", "output:" & $sOutput)

	$iPosition = StringInStr($sOutput, "Python 3.")
	;MsgBox($MB_SYSTEMMODAL, "Info", "iPosition:" & $iPosition)

	If $iPosition = 0 Then
		MsgBox($MB_SYSTEMMODAL, "Warning", "Error: Could not find 'py' nor 'python3'. Please install Python3 before continuing.")
		$sPython = ""
	Endif
Endif

; if we found a valid python
If $sPython <> "" Then
	If Not FileExists("venv\") Then
		$CMD = $sPython & " -m venv venv"
		RunWait(@ComSpec & " /c " & $CMD)
	Endif

	$CMD = "venv\Scripts\activate & " & $sPython & " -m pip install --upgrade pip & pip install --upgrade meshtastic-flasher & meshtastic-flasher"
	RunWait(@ComSpec & " /c " & $CMD)
EndIf