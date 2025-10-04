#!/bin/bash -e

# Add fallback DNS servers to handle network resolution issues
echo "Adding fallback DNS configuration..."

# Backup original resolv.conf
if [ -f "${ROOTFS_DIR}/etc/resolv.conf" ]; then
    cp "${ROOTFS_DIR}/etc/resolv.conf" "${ROOTFS_DIR}/etc/resolv.conf.backup"
fi

# Add multiple DNS servers for reliability
cat > "${ROOTFS_DIR}/etc/resolv.conf" << 'EOF'
nameserver 8.8.8.8
nameserver 8.8.4.4
nameserver 1.1.1.1
nameserver 1.0.0.1
EOF

echo "DNS fallback configuration added"