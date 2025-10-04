#!/bin/bash -e

if [ -f $CONTINUE ]; then
  set +e
fi

# enable headset mode and allow auto switch between hfp and a2dp
sed -i 's/load-module module-bluetooth-discover.*/load-module module-bluetooth-discover headset=ofono/' /etc/pulse/default.pa
sed -i 's/load-module module-bluetooth-discover.*/load-module module-bluetooth-discover headset=ofono/' /etc/pulse/system.pa

# enable correct service state
systemctl disable bluetooth
systemctl disable hciuart
systemctl disable ofono
systemctl enable csng-bluetooth
systemctl enable btautopair
systemctl enable btdevicedetect
systemctl enable btrestore

# config.txt
#echo "" >> /boot/config.txt
#echo "# Bluetooth" >> /boot/config.txt
#echo "dtoverlay=pi3-disable-bt" >> /boot/config.txt

usermod -G bluetooth -a pi
usermod -G bluetooth -a pulse
usermod -G bluetooth -a root

# Enable compat and disable sap
sed -i 's/ExecStart=.*/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd --compat --noplugin=sap/' /usr/lib/systemd/system/bluetooth.service

# Set default bt privacy
sed -i 's/# Privacy = off/Privacy = off/' /etc/bluetooth/main.conf

# Set default controller mode
sed -i 's/#ControllerMode = dual/ControllerMode = bredr/' /etc/bluetooth/main.conf

# Set controller to fast connectable
sed -i 's/#FastConnectable.*/FastConnectable = true/' /etc/bluetooth/main.conf

# Link test script files (with compatibility check for different Debian versions)
# bluez-test-scripts package location changed between Debian versions
BLUEZ_SCRIPTS_DIR=""
if [ -d "/usr/share/doc/bluez-test-scripts/examples" ]; then
    BLUEZ_SCRIPTS_DIR="/usr/share/doc/bluez-test-scripts/examples"
elif [ -d "/usr/share/bluez/test" ]; then
    BLUEZ_SCRIPTS_DIR="/usr/share/bluez/test"
else
    echo "Warning: Bluez test scripts not found, skipping symlink creation"
fi

if [ -n "$BLUEZ_SCRIPTS_DIR" ]; then
    echo "Creating bluez test script symlinks from: $BLUEZ_SCRIPTS_DIR"
    # Only create symlinks if the source files exist
    [ -f "$BLUEZ_SCRIPTS_DIR/list-devices" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/list-devices" /usr/local/bin/list-devices
    [ -f "$BLUEZ_SCRIPTS_DIR/monitor-bluetooth" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/monitor-bluetooth" /usr/local/bin/monitor-bluetooth
    [ -f "$BLUEZ_SCRIPTS_DIR/test-adapter" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-adapter" /usr/local/bin/test-adapter
    [ -f "$BLUEZ_SCRIPTS_DIR/test-heartrate" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-heartrate" /usr/local/bin/test-heartrate
    [ -f "$BLUEZ_SCRIPTS_DIR/test-manager" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-manager" /usr/local/bin/test-manager
    [ -f "$BLUEZ_SCRIPTS_DIR/test-nap" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-nap" /usr/local/bin/test-nap
    [ -f "$BLUEZ_SCRIPTS_DIR/test-network" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-network" /usr/local/bin/test-network
    [ -f "$BLUEZ_SCRIPTS_DIR/test-profile" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-profile" /usr/local/bin/test-profile
    [ -f "$BLUEZ_SCRIPTS_DIR/test-proximity" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-proximity" /usr/local/bin/test-proximity
    [ -f "$BLUEZ_SCRIPTS_DIR/test-sap-server" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-sap-server" /usr/local/bin/test-sap-server
    [ -f "$BLUEZ_SCRIPTS_DIR/test-thermometer" ] && ln -sf "$BLUEZ_SCRIPTS_DIR/test-thermometer" /usr/local/bin/test-thermometer
fi

exit 0