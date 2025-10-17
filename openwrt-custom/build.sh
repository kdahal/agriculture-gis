#!/bin/sh
# Basic OpenWrt build for ath79/generic (UAV mesh optimized)

set -e

echo "Starting OpenWrt build for agriculture-gis..."

# Clone OpenWrt source if not present (CI needs this)
if [ ! -d .git ]; then
  git clone https://git.openwrt.org/openwrt/openwrt.git .
  git checkout stable-v23.05  # Use stable branch for reliability
fi

# Update feeds (custom for mesh: add 802.11s packages)
./scripts/feeds update -a
./scripts/feeds install -a luci-app-mesh11sd kmod-80211s  # Example mesh packages

# Apply seed config if present
if [ -f config.seed ]; then
  cp config.seed .config
fi

# Build firmware
make defconfig
make -j$(nproc) image PROFILE="generic" V=s

echo "Build complete! Firmware in bin/targets/ath79/generic/"
ls -la bin/targets/ath79/generic/*.bin  # List outputs for CI