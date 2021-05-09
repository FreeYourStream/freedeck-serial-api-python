#!/bin/python3
from fdserial.api import FreeDeckSerialAPI
import time


def main():
    api = FreeDeckSerialAPI()

    print("FreeDeck Serial Test")
    print("--------------------")
    print("Firmware: %s" % api.getFirmwareVersion())
    print("Page Count: %i" % api.getPageCount())
    currentPage = api.getCurrentPage()
    print("Current Page: %i" % currentPage)
    api.setCurrentPage(1)
    time.sleep(1)
    api.setCurrentPage(currentPage)


if __name__ == "__main__":
    main()
