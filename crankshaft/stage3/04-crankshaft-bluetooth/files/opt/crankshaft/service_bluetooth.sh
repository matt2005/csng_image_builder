#!/bin/bash -e

source /opt/crankshaft/crankshaft_default_env.sh
source /opt/crankshaft/crankshaft_system_env.sh

cs_autoconnect() {
list=""
# Check if modern bluetoothctl is available (Trixie+) or fallback to deprecated bt-device
if command -v bluetoothctl >/dev/null 2>&1; then
    # Use bluetoothctl (modern approach)
    bluetoothctl paired-devices | awk '{print $2}' | while read line
    do
        # Use timeout to prevent hanging and better error handling for Trixie
        timeout 10 bluetoothctl connect "$line" > /dev/null 2>&1
        # Check connection status using bluetoothctl with timeout
        check=$(timeout 5 bluetoothctl info "$line" 2>/dev/null | grep "Connected:" | awk '{print $2}')
        if [ "$check" == "yes" ]; then
            exit 0
        fi
    done
elif command -v bt-device >/dev/null 2>&1; then
    # Fallback to deprecated bt-device (Buster/Bullseye)
    bt-device -l 2>/dev/null | grep -E -o '[[:xdigit:]]{2}(:[[:xdigit:]]{2}){5}' | while read line
    do
        # Use timeout for bluetoothctl connect command
        timeout 10 bluetoothctl connect "$line" > /dev/null 2>&1
        check=$(bt-device -i "$line" 2>/dev/null | grep Connected | sed 's/ //g' | cut -d: -f2)
        if [ "$check" == "1" ]; then
            exit 0
        fi
    done
else
    log_echo "Error: No bluetooth management tool available (bluetoothctl or bt-device)"
    return 1
fi
}

if [ $ENABLE_BLUETOOTH -eq 1 ]; then
    touch /tmp/bluetooth_enabled

    # Set controller in correct mode with version-aware commands
    log_echo "Init bluetooth adapter defaults"
    if command -v bluetoothctl >/dev/null 2>&1; then
        # Use bluetoothctl (modern approach for Trixie+) with individual commands for reliability
        timeout 10 bluetoothctl power on > /dev/null 2>&1
        timeout 10 bluetoothctl discoverable on > /dev/null 2>&1
        timeout 10 bluetoothctl discoverable-timeout 0 > /dev/null 2>&1
    elif command -v bt-adapter >/dev/null 2>&1; then
        # Fallback to deprecated bt-adapter (Buster/Bullseye)
        sudo bt-adapter --set Powered 1
        sudo bt-adapter --set Discoverable 1
        sudo bt-adapter --set DiscoverableTimeout 0
    else
        log_echo "Error: No bluetooth adapter management tool available"
    fi
    if [ $ENABLE_PAIRABLE -eq 1 ]; then
        log_echo "Set bluetooth adapter pairable for 120 seconds"
        /usr/local/bin/crankshaft bluetooth pairable
    fi
    # Try 5 attempts to connect
    counter=0
    while [ $counter -lt 5 ] && [ ! -f /tmp/btdevice ]; do
        log_echo "Bluetooth auto connect attempt: $counter"
        cs_autoconnect
        sleep 5
        counter=$((counter+1))
    done
fi
