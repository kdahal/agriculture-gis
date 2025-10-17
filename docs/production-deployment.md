# Production Deployment Guide

Deploy a resilient ground station for 90+ drone swarms. Uses Docker for isolation/portability.

## Prerequisites
- Docker & Docker Compose v2+.
- Ground station hardware: x86/ARM server with Ethernet/WiFi bridge to mesh.

## 1. MQTT Broker (Mosquitto)
Handles GPS data relay from drones.

### docker-compose.yml (Ground Station)
```yaml
version: '3.8'
services:
  mosquitto:
    image: eclipse-mosquitto:2.0
    restart: unless-stopped
    ports:
      - "1883:1883"  # MQTT
      - "9001:9001"  # WebSocket (optional)
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    environment:
      - MOSQUITTO_USERNAME=${MQTT_USER}  # e.g., admin
      - MOSQUITTO_PASSWORD=${MQTT_PASS}  # Strong pass

  gis-dashboard:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "8000:80"
    volumes:
      - ../gis-web:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - mosquitto

  # Optional: Prometheus for metrics
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
