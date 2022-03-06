from typing import Iterable
from fdserial.utils import getFreeDeckPort
from serial import Serial
from more_itertools import chunked

# you should wait (number of displays * 30ms) after a page changing command
# if you want to immediately call the api again to give the freedeck time
# to finish refreshing

commands = {
    "init": 0x3,
    "getFirmwareVersion": 0x10,
    "readConfig": 0x20,
    "writeConfig": 0x21,
    "getCurrentPage": 0x30,
    "setCurrentPage": 0x31,
    "getPageCount": 0x32
}


class FreeDeckSerialAPI:
    freedeck: Serial = None
    pageCount: int

    def __init__(self, port: str = None):
        if port != None:
            self.freedeck = Serial(port, 4000000)
        else:
            self.freedeck = Serial(getFreeDeckPort(), 4000000)
        self.pageCount = self.getPageCount()

    def intToAsciiVal(self, number: int):
        numberStr = str(number)
        numberCharArr = []
        for char in numberStr:
            numberCharArr.append(ord(char))
        return numberCharArr

    def prepare(self, data: Iterable):
        dataWithNL = bytearray()
        for bytes in data:
            if isinstance(bytes, list):
                for byte in bytes:
                    dataWithNL.append(byte)
            else:
                dataWithNL.append(bytes)
            dataWithNL.append(0xa)
        return dataWithNL

    def writeOnly(self, data: Iterable):
        self.freedeck.read_all()
        self.freedeck.write(self.prepare(data))
        return

    def readWrite(self, data: Iterable):
        self.freedeck.read_all()
        self.freedeck.write(self.prepare(data))
        return self.freedeck.read_until().decode('utf-8').rstrip("\r\n")

    def getFirmwareVersion(self):
        return self.readWrite([commands['init'], commands["getFirmwareVersion"]])

    def getCurrentPage(self):
        return int(self.readWrite([commands['init'], commands["getCurrentPage"]]))

    def setCurrentPage(self, page: int):
        if page > self.pageCount - 1:
            print("OOB")
            return
        return self.readWrite(
            [commands['init'], commands["setCurrentPage"], self.intToAsciiVal(page)])

    def getPageCount(self):
        return int(self.readWrite([commands['init'], commands['getPageCount']]))

    def readConfig(self, filename):
        configSizeStr = self.readWrite([commands['init'], commands['readConfig']])
        configSize = int(configSizeStr)

        configData = self.freedeck.read(configSize)

        with open(filename, "wb") as configFile:
            configFile.write(configData)

        return configSize

    def writeConfig(self, filename):
        with open(filename, "rb") as configFile:
            configData = configFile.read()

        configFileSize = len(configData)

        self.writeOnly([commands['init'],
                        commands['writeConfig'],
                        self.intToAsciiVal(configFileSize)])
        
        # Every 4KiB of data, the firmware sends back over the number of bytes
        # received.
        for chunk in chunked(configData, 4096):
            self.freedeck.write(chunk)
            bytes_received = self.freedeck.read_all()
