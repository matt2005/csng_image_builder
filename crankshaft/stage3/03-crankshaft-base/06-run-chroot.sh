#!/bin/bash -e

# Try to purge wiringpi if it exists (may not be available in newer Debian versions)
apt-get purge wiringpi -y || true
hash -r
dpkg -i /root/wiringpi-latest.deb
