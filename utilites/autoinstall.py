#!/usr/bin/env python3
import importlib.util, subprocess, sys
# an auto gen script to install libraries 
# Function to check if a package is installed
def check_and_install(package_name):
    if importlib.util.find_spec(package_name) is None:
        print(f"Package '{package_name}' is missing. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    else:
        print(f"Package '{package_name}' is already installed.")

# List of required packages
#required_packages = ["spidev", "pyvisa", "keyboard", "zeroconf", "psutil", "pyserial", "pyusb"]
required_packages = [ "pyvisa", "zeroconf", "psutil", "pyserial", "pyusb"]

# Check and install each package
for pkg in required_packages:
    check_and_install(pkg)

# This shell script creates and intializes udev scripts
mk_udev="""
echo "LOL IDK.."
"""
#Todo: figure out how to write this script.
