#!/bin/bash -e

# Add OpenCarDev tweaks
echo "Adding OpenCarDev tweaks..."
# This runs in chroot context so we can use normal file paths
# Copy zram-generator configuration
install -Dm644 files/etc/systemd/zram-generator.conf /etc/systemd/zram-generator.conf
systemctl daemon-reload && systemctl start systemd-zram-setup@zram0.service

# Apply sysctl tweaks
install -Dm644 files/etc/sysctl.conf /etc/sysctl.conf
sysctl --system

echo "OpenCarDev tweaks setup completed successfully"
