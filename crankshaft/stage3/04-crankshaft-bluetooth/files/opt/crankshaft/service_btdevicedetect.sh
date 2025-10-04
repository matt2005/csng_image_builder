#!/bin/bash

source /opt/crankshaft/crankshaft_default_env.sh
source /opt/crankshaft/crankshaft_system_env.sh

if [ $ENABLE_BLUETOOTH -eq 1 ]; then
    # Check loop for connected btdevice with version-aware commands
    while true; do
        if command -v bluetoothctl >/dev/null 2>&1; then
            # Use bluetoothctl (modern approach for Trixie+)
            bluetoothctl paired-devices 2>/dev/null | awk '{print $2}' | while read paired; do
                # Get device info using bluetoothctl with timeout for reliability
                info=$(timeout 5 bluetoothctl info "$paired" 2>/dev/null | grep -E "Name:|Connected:" | awk -F: '{print $2}' | sed 's/^ *//g' | sed 's/ *$//g' | tr '\n' '#')
                device=$(echo $info | cut -d# -f1 | tr -d '\n')
                state=$(echo $info | cut -d# -f2 | tr -d '\n')
                if [ "$state" == "yes" ]; then
                    if [ ! -f /tmp/btdevice ]; then
                        echo "${device}" > /tmp/btdevice
                        log_echo "Bluetooth device connected: ${device} -> stop timers"
                        /usr/local/bin/crankshaft timers stop
                    fi
                else
                    if [ -f /tmp/btdevice ]; then
                        rm -f /tmp/btdevice
                        log_echo "Bluetooth device removed -> start timers"
                        /usr/local/bin/crankshaft timers start
                    fi
                fi
            done
        elif command -v bt-device >/dev/null 2>&1; then
            # Fallback to deprecated bt-device (Buster/Bullseye) with error handling
            bt-device -l 2>/dev/null | grep -e '(' | grep -e ':' | cut -d'(' -f2 | cut -d')' -f1 | while read paired; do
                info=$(bt-device --info="$paired" 2>/dev/null | grep -e 'Name:' -e 'Connected:' | cut -d: -f2 | sed 's/^ *//g' | sed 's/ *$//g' | tr '\n' '#')
                device=$(echo $info | cut -d# -f1 | tr -d '\n')
                state=$(echo $info | cut -d# -f2 | tr -d '\n')
                if [ "$state" == "1" ]; then
                    if [ ! -f /tmp/btdevice ]; then
                        echo "${device}" > /tmp/btdevice
                        log_echo "Bluetooth device connected: ${device} -> stop timers"
                        /usr/local/bin/crankshaft timers stop
                    fi
                else
                    if [ -f /tmp/btdevice ]; then
                        rm -f /tmp/btdevice
                        log_echo "Bluetooth device removed -> start timers"
                        /usr/local/bin/crankshaft timers start
                    fi
                fi
            done
        else
            log_echo "Error: No bluetooth device management tool available"
            sleep 10
        fi
        sleep 5
    done
fi
