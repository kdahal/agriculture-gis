#!/bin/sh
# Basic OpenWrt build script for ath79/generic target
# Assumes OpenWrt source is in /builder (clone via git if needed)
# Usage: ./build.sh

set -e  # Exit on error

echo "Building OpenWrt firmware for ath79/generic..."

# Update feeds (if feeds.conf exists)
if [ -f feeds.conf.default ]; then
    ./scripts/feeds update -a
    ./scripts/feeds install -a
fi

# Build image (use your device PROFILE, e.g., "generic" for sim)
make defconfig
make -j$(nproc) image PROFILE="generic" V=s

echo "Build complete! Images in bin/targets/ath79/generic/"