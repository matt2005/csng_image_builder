#!/bin/bash -e

on_chroot << EOF
pip3 install smbus --break-system-packages
pip3 install python-tsl2591 --break-system-packages
EOF
