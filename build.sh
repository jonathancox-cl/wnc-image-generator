#!/usr/bin/env bash
set -e

pip install -r requirements.txt

# Download DejaVu fonts directly into repo fonts/ directory
mkdir -p fonts

DEJAVU_URL="https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2"

echo "Downloading DejaVu fonts..."
curl -L "$DEJAVU_URL" -o /tmp/dejavu.tar.bz2
tar -xjf /tmp/dejavu.tar.bz2 -C /tmp
cp /tmp/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf fonts/
cp /tmp/dejavu-fonts-ttf-2.37/ttf/DejaVuSans-Bold.ttf fonts/
cp /tmp/dejavu-fonts-ttf-2.37/ttf/DejaVuSerif-Bold.ttf fonts/
rm -f /tmp/dejavu.tar.bz2
echo "Fonts downloaded successfully."
ls -la fonts/
