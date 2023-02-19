#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "/Users/solo/desktopdb/dist/desktopdb.app" dist/dmg
# If the DMG already exists, delete it.
test -f "/Users/solo/desktopdb/dist/desktopdb.dmg" && rm "/Users/solo/desktopdb/dist/desktopdb.dmg"
create-dmg \
  --volname "DesktopDB" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "desktopdb.app" \
  --app-drop-link 425 120 \
  "/Users/solo/desktopdb/dist/DesktopDB.dmg" \
  "dist/dmg/"