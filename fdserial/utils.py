#!/bin/python3
import os


def execBash(command):
    import subprocess
    response, error = subprocess.Popen(
        ["bash", "-c", command], stdout=subprocess.PIPE).communicate()
    return response


def binaryToString(binary):
    return binary.decode("utf-8").rstrip("\r\n")


def findFreeDeckDeviceWin():
    return "COM14"  # automate this


def findFreeDeckDeviceLinux():
    import subprocess
    devices = execBash("find /sys/bus/usb/devices/usb*/ -name dev")

    for device in devices.splitlines():
        devicePath = device.decode("utf-8").rstrip("/dev")
        deviceNameRaw = execBash("udevadm info -q name -p %s" % devicePath)
        deviceName = binaryToString(deviceNameRaw)
        if deviceName.find("bus/") != -1:
            continue

        info = execBash(
            "eval $(udevadm info -q property --export -p %s) && echo $ID_VENDOR_ID:$ID_MODEL_ID:$SUBSYSTEM" % devicePath)
        identifier = binaryToString(info)
        if identifier == "2341:8037:tty" or identifier == "f1f0:4005:tty":
            print("found device on %s" % deviceName)
            return "/dev/%s" % deviceName
    raise Exception('no device found')


def getFreeDeckPort():
    if os.name == "nt":
        return findFreeDeckDeviceWin()
    else:
        return findFreeDeckDeviceLinux()
