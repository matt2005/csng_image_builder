#!/bin/bash -e

# Network retry logic for stage4 packages
echo "Configuring network retry logic for package installation..."

# Function to test network connectivity
test_network() {
    local host="$1"
    echo "Testing connectivity to $host..."
    if timeout 10 ping -c 1 "$host" >/dev/null 2>&1; then
        echo "✓ Successfully reached $host"
        return 0
    else
        echo "✗ Failed to reach $host"
        return 1
    fi
}

# Test connectivity to package repositories
echo "Testing repository connectivity..."
test_network "archive.raspberrypi.com" || echo "Warning: archive.raspberrypi.com unreachable"
test_network "raspbian.raspberrypi.com" || echo "Warning: raspbian.raspberrypi.com unreachable"
test_network "8.8.8.8" || echo "Warning: Basic internet connectivity failed"

# Add apt retry configuration
cat > "${ROOTFS_DIR}/etc/apt/apt.conf.d/80retries" << 'EOF'
APT::Acquire::Retries "3";
APT::Acquire::http::Timeout "30";
APT::Acquire::https::Timeout "30";
APT::Acquire::ftp::Timeout "30";
EOF

echo "Network retry configuration completed"