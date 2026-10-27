Unicode True
!include "MUI2.nsh"
Name "Vigil Social"
OutFile "${OUTPUT}"
InstallDir "$LOCALAPPDATA\Programs\AltStackSocial"
RequestExecutionLevel user
SetCompressor /SOLID lzma
!define MUI_ICON "${REPO}\assets\logo.ico"
!define MUI_UNICON "${REPO}\assets\logo.ico"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${REPO}\LICENSE"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
Section "Vigil Social"
  SetShellVarContext current
  SetOutPath "$INSTDIR"
  File /r "${SOURCE}\*"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortCut "$SMPROGRAMS\Vigil Social.lnk" "$INSTDIR\AltStackSocial.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AltStackSocial" "DisplayName" "Vigil Social"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AltStackSocial" "Publisher" "VigilTech"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AltStackSocial" "DisplayVersion" "1.3.2"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AltStackSocial" "UninstallString" '$\"$INSTDIR\Uninstall.exe$\"'
SectionEnd
Section "Uninstall"
  SetShellVarContext current
  ; Generated commands remove only packaged files and empty directories, never a profile or arbitrary tree.
  !include "${REMOVAL_MANIFEST}"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  Delete "$SMPROGRAMS\Vigil Social.lnk"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AltStackSocial"
SectionEnd
