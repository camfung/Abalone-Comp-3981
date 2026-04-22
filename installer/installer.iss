; Inno Setup script for Abalone Game
; Build with: ISCC.exe installer\installer.iss  (from project root)
; Or run installer\build.bat which handles everything automatically.

#define AppName "Abalone Game"
#define AppVersion "1.0.0"
#define AppExeName "Abalone_Game.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Abalone Game
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
OutputBaseFilename=Abalone_Game_Setup
Compression=lzma
SolidCompression=yes
; UninstallDisplayIcon={app}\{#AppExeName}
; WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; All files from the PyInstaller onedir output
Source: "..\dist\Abalone_Game\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
; Start menu shortcut
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"
; Desktop shortcut
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: postinstall nowait skipifsilent
