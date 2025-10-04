#!/bin/bash -e

# Handle wiringpi compatibility - package may not exist in newer Debian versions
set +e  # Temporarily disable exit on error
apt-get purge wiringpi -y 2>/dev/null
PURGE_RESULT=$?
set -e  # Re-enable exit on error

echo "Wiringpi purge result: $PURGE_RESULT (0=success, non-zero=package not found/already removed)"

# Clear hash and install local wiringpi package if it exists
hash -r
if [ -f /root/wiringpi-latest.deb ]; then
    echo "Installing local wiringpi package..."
    dpkg -i /root/wiringpi-latest.deb
    echo "Wiringpi installation completed"
else
    echo "Warning: wiringpi-latest.deb not found, skipping installation"
fi
