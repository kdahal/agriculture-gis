#!/bin/sh
# One-click mesh setup for Vehicle Tracking and Agriculture GIS
# Usage: ./deploy-mesh.sh (from scripts/ dir)
# Applies UCI config and restarts network services.

set -e  # Exit immediately if a command exits with a non-zero status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "${GREEN}Setting up 802.11s mesh network...${NC}"

# Check for required config file
CONFIG_PATH="../configs/mesh-uci.conf"
if [ ! -f "$CONFIG_PATH" ]; then
    echo "${RED}Error: $CONFIG_PATH not found. Run from scripts/ dir or create the config.${NC}"
    exit 1
fi

# Import UCI network config
uci import network < "$CONFIG_PATH"
uci commit network

# Reload WiFi interfaces
wifi reload

# Optional: Start GPS relay if script exists
GPS_SCRIPT="../configs/gps-aggregation.sh"
if [ -f "$GPS_SCRIPT" ]; then
    chmod +x "$GPS_SCRIPT"
    "$GPS_SCRIPT" &
    echo "${GREEN}GPS relay started in background.${NC}"
fi

echo "${GREEN}Mesh setup complete! Verify with 'iw dev mesh0 info'.${NC}"