#!/bin/bash -e

# Check if we're running on a Debian version before Bookworm
# Prebuilt Qt5 OpenGLES2 was compiled for VideoCore drivers (Buster/Bullseye)
# Modern Debian versions (Bookworm+) use Mesa drivers and may conflict with this prebuilt version
if [ -f "${ROOTFS_DIR}/etc/os-release" ]; then
    # Safely extract VERSION_ID without sourcing the file
    VERSION_ID=$(grep '^VERSION_ID=' "${ROOTFS_DIR}/etc/os-release" | cut -d= -f2 | tr -d '"')
    # Extract version number (11 for Bullseye, 12 for Bookworm, 13 for Trixie)
    DEBIAN_VERSION=$(echo "$VERSION_ID" | cut -d. -f1)
    
    # Only install prebuilt Qt5 for Debian versions before Bookworm (< 12)
    if [ -n "$DEBIAN_VERSION" ] && [ "$DEBIAN_VERSION" -lt 12 ]; then
        echo "Debian version $VERSION_ID detected - installing prebuilt Qt5 OpenGLES2 for VideoCore compatibility"
        # qt5 from prebuilts
        cat $BASE_DIR/prebuilts/qt5/Qt_5151_armv7l_OpenGLES2.tar.xz* > files/qt5/Qt5_OpenGLES2.tar.xz
        
        #qt5
        tar -xf files/qt5/Qt5_OpenGLES2.tar.xz -C ${ROOTFS_DIR}/
    else
        echo "Debian version $VERSION_ID detected - skipping prebuilt Qt5 OpenGLES2 (conflicts with Mesa drivers on Bookworm+)"
        echo "Modern Qt5 packages will be used from official repositories instead"
    fi
else
    echo "Warning: Could not detect OS version, skipping prebuilt Qt5 OpenGLES2 installation"
fi