#!/bin/bash -e

on_chroot <<EOF
# Check if lpadmin group exists before trying to add user to it
if getent group lpadmin > /dev/null 2>&1; then
    echo "Adding user $FIRST_USER_NAME to lpadmin group"
    adduser "$FIRST_USER_NAME" lpadmin
else
    echo "Warning: lpadmin group does not exist - printing system not installed"
    echo "Skipping print support user configuration"
fi
EOF
