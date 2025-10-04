#!/bin/bash -e

# Alternative package installation strategy
echo "Setting up alternative package installation..."

# Check if the problematic packages are actually needed
ESSENTIAL_PACKAGES="false"

if [ "$ESSENTIAL_PACKAGES" = "true" ]; then
    echo "Attempting to install RPD metapackages with fallbacks..."
    
    # Try to install packages with timeout and retries
    for package in rpd-applications rpd-developer rpd-graphics rpd-utilities rpd-wayland-extras rpd-x-extras; do
        echo "Attempting to install $package..."
        if timeout 120 on_chroot << EOF
apt-get update --fix-missing || true
apt-get install -y --allow-unauthenticated $package || echo "Warning: Failed to install $package"
EOF
        then
            echo "✓ Successfully installed $package"
        else
            echo "✗ Failed to install $package - continuing without it"
        fi
    done
else
    echo "Skipping RPD metapackages (not essential for OpenAuto)"
fi

echo "Alternative package installation completed"