# Security Hardening for Production

Follow these steps post-flash for secure UAV mesh deployments.

## 1. Update Packages
```bash
opkg update
opkg upgrade
opkg install luci-app-attendedsysupgrade  # For seamless updates