# Additional native installers

The rebrand's six package jobs passed, but publishing failed because 1.3.1 already exists. Publish 1.3.2 instead of overwriting its Cohnsoft artifacts. Preserve all six old basenames. Add two Windows NSIS installers and two Linux AppImage plus two .deb files; publication verifies twelve deliverables and checksums only after the native platform jobs pass.

NSIS 3.13 and appimagetool 1.9.1 are downloaded from their official distribution endpoints and verified against pinned SHA-256 values in packaging/toolchain.json. Windows installs per user without elevation. Its uninstaller removes only the build's enumerated files and empty directories, preserving other files, profiles and projects. Existing Qt app identifiers and keychain behavior are unchanged.

AppImages are checked without requiring FUSE. Debian payloads are extracted and launched in CI. Windows CI installs and launches the installed program. Native Mac DMG verification remains. Linux minimum runtime follows the Ubuntu 24.04 build baseline (glibc 2.39); this is not a claim of universal Linux compatibility. Existing user launchers are not deleted; avoid mixing distribution formats.
