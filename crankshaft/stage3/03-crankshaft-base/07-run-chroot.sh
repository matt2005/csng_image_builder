#!/bin/bash -e

# Check if we're running on a Debian version before Bookworm
# VideoCore legacy libraries were deprecated in Bookworm and removed in Trixie
if [ -f /etc/os-release ]; then
    # Safely extract VERSION_ID without sourcing the file
    VERSION_ID=$(grep '^VERSION_ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
    # Extract version number (11 for Bullseye, 12 for Bookworm, 13 for Trixie)
    DEBIAN_VERSION=$(echo "$VERSION_ID" | cut -d. -f1)
    
    # Only create symlinks for Debian versions before Bookworm (< 12)
    if [ -n "$DEBIAN_VERSION" ] && [ "$DEBIAN_VERSION" -lt 12 ]; then
        echo "Debian version $VERSION_ID detected - creating VideoCore legacy library symlinks"
        # fix Pi2 eglfs on Buster/Bullseye
        ln -s /opt/vc/lib/libbrcmEGL.so /usr/lib/arm-linux-gnueabihf/libEGL.so
        ln -s /opt/vc/lib/libbrcmGLESv2.so /usr/lib/arm-linux-gnueabihf/libGLESv2.so
        ln -s /opt/vc/lib/libbrcmOpenVG.so /usr/lib/arm-linux-gnueabihf/libOpenVG.so
        ln -s /opt/vc/lib/libbrcmWFC.so /usr/lib/arm-linux-gnueabihf/libWFC.so
    else
        echo "Debian version $VERSION_ID detected - skipping VideoCore legacy library symlinks (not needed for Bookworm+)"
    fi
else
    echo "Warning: Could not detect OS version, skipping VideoCore legacy library symlinks"
fi
