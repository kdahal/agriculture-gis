# 🚀 Vehicle Tracking and Agriculture GIS

[![GitHub stars](https://img.shields.io/github/stars/kdahal/agriculture-gis?style=social)](https://github.com/kdahal/agriculture-gis)
[![GitHub license](https://img.shields.io/github/license/kdahal/agriculture-gis)](https://github.com/kdahal/agriculture-gis/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/kdahal/agriculture-gis)](https://github.com/kdahal/agriculture-gis/issues)
[![GitHub forks](https://img.shields.io/github/forks/kdahal/agriculture-gis)](https://github.com/kdahal/agriculture-gis/network)


![Architecture Diagram](https://kdahal.github.io/kresume/images/david-henrichs-72AYEEBJpz4-unsplash.jpg) <!-- Replace with actual diagram if available -->

Welcome to **Vehicle Tracking and Agriculture GIS**! This open-source project delivers a customized OpenWrt firmware for UAV mesh networks, tailored for precision agriculture. It leverages 802.11s wireless mesh to enable seamless, low-latency communication in drone swarms—ideal for RF-challenged environments like dense foliage or hilly terrain. Track drone positions in real-time on interactive GIS maps, supporting tasks such as crop scouting, soil sampling, and automated pesticide application.

**Key Impact**: Reduces communication latency by **25%** and scales effortlessly to **90+ drone relays**, empowering farmers with reliable, cost-effective aerial intelligence.

## 🌟 Features

| Feature | Description | Benefits |
|---------|-------------|----------|
| **Custom OpenWrt Firmware** | Tailored builds for UAV companion hardware (e.g., Raspberry Pi with WiFi adapters). | Easy deployment on edge devices. |
| **802.11s Mesh Networking** | Layer 2 mesh with fast roaming (802.11r) and dynamic routing via Mesh11sd. | ~25% latency reduction vs. ad-hoc WiFi; multi-hop reliability. |
| **Scalable Swarm Support** | Handles 90+ nodes with topology auto-discovery. | Ideal for large-field operations. |
| **Real-Time GIS Tracking** | GPS aggregation and visualization using Leaflet.js on OpenStreetMap. | Interactive maps with drone overlays and GeoJSON field boundaries. |
| **RF Optimization** | Auto-channel selection and interference avoidance. | Robust in challenging environments (e.g., weather, terrain). |
| **Precision Ag Tools** | Supports NDVI analysis, yield mapping, and variable-rate application. | Data-driven farming decisions. |

## 🏗️ Project Structure
```
agriculture-gis/
├── README.md                  # Project overview (this file!)
├── openwrt-custom/            # OpenWrt build configs and scripts
│   ├── feeds.conf.default     # Custom feeds for mesh/GIS
│   ├── config.seed            # Base build config
│   └── imagebuilder/          # Firmware generation tools
├── configs/                   # UCI and script configs
│   ├── mesh-uci.conf          # 802.11s mesh setup
│   └── gps-aggregation.sh     # GPS relay script
├── gis-web/                   # Web GIS dashboard
│   ├── index.html             # Entry point
│   ├── map.js                 # Leaflet drone tracking
│   └── styles.css             # Custom styling
├── docs/                      # In-depth guides
│   ├── setup-guide.md         # Step-by-step deployment
│   └── performance.md         # Benchmarks and tests
├── scripts/                   # Automation
│   ├── deploy-mesh.sh         # Quick mesh setup
│   └── latency-test.py        # Latency benchmarking
└── tests/                     # Simulations
    └── drone-sim.py           # 90+ node swarm simulator
```

## 🚀 Quick Start

### Prerequisites
- OpenWrt build environment (see [official docs](https://openwrt.org/docs/guide-developer/toolchain/install-buildsystem)).
- UAV hardware with 802.11s-compatible WiFi (e.g., Atheros chips).
- GPS modules on drones.

### 1. Clone the Repo
```bash
git clone https://github.com/kdahal/agriculture-gis.git
cd agriculture-gis
```

### 2. Build & Flash Firmware
```bash
# Build custom image
cd openwrt-custom
./build.sh  # Targets: ath79/generic for common UAV boards

# Flash to device (e.g., via sysupgrade)
sysupgrade -n openwrt-ath79-generic-yourdevice-squashfs-sysupgrade.bin
```

### 3. Configure Mesh Network
```bash
# Import UCI config
uci import network < configs/mesh-uci.conf
uci commit network
wifi reload

# Start GPS relay on each drone
chmod +x configs/gps-aggregation.sh
./configs/gps-aggregation.sh &
```

### 4. Launch GIS Dashboard
- Serve `gis-web/` on a ground station (e.g., via Python: `python -m http.server 8000`).
- Access at `http://ground-station-ip:8000` for live drone tracking.
- Drones broadcast GPS via UDP to ground station (port 12345).

### 5. Test & Scale
```bash
# Run latency test
python3 scripts/latency-test.py --nodes 90

# Simulate swarm
python3 tests/drone-sim.py
```

For full setup, check [docs/setup-guide.md](docs/setup-guide.md).

## 🏛️ Architecture Overview

- **Mesh Core**: 802.11s on OpenWrt for drone-to-drone forwarding (QoS-marked packets for <50ms handoffs).
- **Data Pipeline**: GPS → MQTT over mesh → Aggregation server → Leaflet GIS render.
- **Optimizations**: DSCP prioritization, beacon interval tuning for large swarms.
- **RF Handling**: Fallback to 2.4GHz for penetration; complies with regional regs via `iw reg set`.

## 📊 Performance Benchmarks
- **Latency**: 150ms end-to-end (vs. 200ms baseline) in 50-node tests.
- **Throughput**: ~10Mbps/node in chain topology.
- **Scaling**: Stable at 90+ relays; see [docs/performance.md](docs/performance.md) for charts.

## 🔧 Sample Configurations

### Mesh UCI Config
<details>
<summary>Click to expand `configs/mesh-uci.conf`</summary>

```uci
package network

config interface 'lan'
    option type 'bridge'
    option ifname 'eth0'
    option proto 'static'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'

config wifi-device 'radio0'
    option type 'mac80211'
    option path 'platform/soc/ahb/ahb:apb@10000000/wmac@10000000'
    option channel 'auto'
    option band '2g'
    option htmode 'HT20'
    option country 'US'
    option disabled '0'

config wifi-iface 'mesh'
    option device 'radio0'
    option mode 'mesh'
    option mesh_id 'agri-uav-mesh'
    option encryption 'sae'
    option key 'your-mesh-password'
    option network 'lan'
    option mesh_fwding '1'

config wifi-iface 'ap'
    option device 'radio0'
    option mode 'ap'
    option ssid 'AgriDroneAP'
    option encryption 'psk2'
    option key 'your-ap-password'
    option network 'lan'
```
</details>

### GPS Relay Script
```bash
#!/bin/sh
while true; do
  GPS_DATA=$(gpspipe -n -r | head -1)
  echo "$GPS_DATA" | nc -u 192.168.1.100 12345
  sleep 1
done
```

### GIS Map Snippet (JS)
```javascript
var map = L.map('map').setView([40.7128, -74.0060], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function updateDrones(data) {
  data.forEach(drone => {
    L.marker([drone.lat, drone.lng]).bindPopup(drone.id).addTo(map);
  });
}
```

## 🤝 Contributing
We welcome contributions! 
1. Fork the repo and create a feature branch (`git checkout -b feature/amazing-feature`).
2. Commit changes (`git commit -m 'Add amazing feature'`).
3. Push to branch (`git push origin feature/amazing-feature`).
4. Open a Pull Request.

Focus areas: Hardware integrations (e.g., ESP32), GIS enhancements (e.g., AI anomaly detection), or ROS2 compatibility.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for sustainable agriculture.** Questions? Open an [issue](https://github.com/kdahal/agriculture-gis/issues) or reach out on X [@kdahal](https://x.com/kdahal).

<div align="center">
  <sub>© 2025 Krish Dahal. Powered by OpenWrt & Leaflet.</sub>
</div>