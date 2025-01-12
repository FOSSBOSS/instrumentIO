#!/bin/bash
# this script requires rootly power....
# this script attempts to autogen 
echo "Generating udev rules for your instrument:
      plug your USB instrument in....
       55-instrumentIO.rules 
     will be writen
       "
read
#Todo: check existing rules and append

rules="55-instrumentIO.rules"       
rulesPath="/etc/udev/rules.d/"$rules
# List of typical device classes to ignore (keyboard, mouse, camera, etc.)
IGNORE_CLASSES=("03" "E0")
# Function to check if a device class is in the ignore list
is_ignored_class() {
    local class="$1"
    for ignore in "${IGNORE_CLASSES[@]}"; do
        if [[ "$class" == "$ignore" ]]; then
            return 0
        fi
    done
    return 1
}
# Run lsusb and parse the output
lsusb | while read -r line; do
    # Extract bus, device, vendor ID, product ID, and device class
    bus=$(echo "$line" | awk '{print $2}')
    device=$(echo "$line" | awk '{print $4}' | sed 's/://')
    vendor=$(echo "$line" | awk '{print $6}' | cut -d: -f1)
    product=$(echo "$line" | awk '{print $6}' | cut -d: -f2)
    device_class=$(lsusb -s ${bus}:${device} -v 2>/dev/null | grep "bDeviceClass" | awk '{print $2}' | head -n 1)

    # Check if the device class should be ignored
    if is_ignored_class "$device_class"; then
        continue
    fi

    # Generate a udev rule
    echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"${vendor}\", ATTR${idProduct}==\"${product}\", MODE=\"0666\""
done > $rules
# this is a temp script for later integration to an auto installer Im writing.
sudo cp $rules $rulesPath

# Reload udev rules and trigger
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Udev rules have been generated and applied."
