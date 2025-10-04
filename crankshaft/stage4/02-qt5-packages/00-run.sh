#!/bin/bash -e

# Install Qt5 packages conditionally based on Debian version
# For Trixie (Debian 13+), install modern Qt5 packages instead of prebuilt version

if [ -f "${ROOTFS_DIR}/etc/os-release" ]; then
    source "${ROOTFS_DIR}/etc/os-release"
    # Extract version number (11 for Bullseye, 12 for Bookworm, 13 for Trixie)
    DEBIAN_VERSION=$(echo "$VERSION_ID" | cut -d. -f1)
    
    # Install modern Qt5 packages for Debian Bookworm and later (≥ 12)
    if [ -n "$DEBIAN_VERSION" ] && [ "$DEBIAN_VERSION" -ge 12 ]; then
        echo "Debian version $VERSION_ID detected - installing modern Qt5 packages for Mesa driver compatibility"
        
        on_chroot << EOF
# Install Qt5 development and runtime packages
apt-get update
apt-get install -y \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    libqt5bluetooth5 \
    libqt5multimedia5 \
    qtmultimedia5-dev \
    qml-module-qtbluetooth \
    qtconnectivity5-dev

echo "Qt5 packages installation completed for modern Mesa drivers"
EOF
    else
        echo "Debian version $VERSION_ID detected - skipping modern Qt5 packages (using prebuilt version for VideoCore compatibility)"
    fi
else
    echo "Warning: Could not detect OS version, skipping Qt5 package installation"
fi