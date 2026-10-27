#!/bin/sh
set -eu
SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET="$HOME/.local/opt/altstack-social"
mkdir -p "$TARGET" "$HOME/.local/share/applications" "$HOME/.local/share/icons/hicolor/512x512/apps" "$HOME/.local/bin"
# Copies files without deleting unrelated user data. No root privileges are needed.
cp -R "$SOURCE"/. "$TARGET"/
chmod +x "$TARGET/AltStackSocial"
ln -sf "$TARGET/AltStackSocial" "$HOME/.local/bin/AltStackSocial"
ln -sf "$TARGET/AltStackSocial" "$HOME/.local/bin/altstack-social"
cp "$TARGET/_internal/assets/logo.png" "$HOME/.local/share/icons/hicolor/512x512/apps/altstack-social.png"
sed "s|Exec=AltStackSocial|Exec=\"$TARGET/AltStackSocial\"|" "$SOURCE/altstack-social.desktop" > "$HOME/.local/share/applications/altstack-social.desktop"
printf '%s\n' 'Installed Cohnsoft Social for the current user.'
