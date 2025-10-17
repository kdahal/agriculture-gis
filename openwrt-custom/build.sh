#!/bin/sh
# Basic OpenWrt build for ath79/generic (customized for UAV mesh)

set -e

echo "Starting OpenWrt build..."

# Clone OpenWrt source if not present (for CI/full build)
if [ ! -d .git ]; then
  git clone https://git.openwrt.org/openwrt/openwrt.git .
fi

# Update feeds (add custom feeds if feeds.conf.default exists)
if [ -f feeds.conf.default ]; then
  ./scripts/feeds update -a
  ./scripts/feeds install -a
fi

# Apply base config if present
if [ -f config.seed ]; then
  cp config.seed .config
fi

# Build
make defconfig
make -j$(nproc) image PROFILE="generic" V=s

echo "Build complete! Check bin/targets/ath79/generic/"