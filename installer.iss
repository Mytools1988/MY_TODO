#define MyAppName "MY TODO"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "LATIF Jackstadt"
#define MyAppURL "noch keine webseite"
#define MyAppExeName "MY TODO_APP.exe"

[Setup]
AppId={{B7A98E42-7B23-4F4C-8D52-C5F3E2F89D63}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=mytodo-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startupicon"; Description: "Beim Windows-Start automatisch starten"; GroupDescription: "Autostart"

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "todos.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "categories.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "settings.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent 