# freedeck-serial-api

A python library to speak to the FreeDeck.

## Usage

```python
from fdserial.api import FreeDeckSerialAPI
api = FreeDeckSerialAPI()
print("Firmware: %s" % api.getFirmwareVersion())
print("Page Count: %i" % api.getPageCount())
currentPage = api.getCurrentPage()
print("Current Page: %i" % currentPage)
api.setCurrentPage(1)
time.sleep(1)
api.setCurrentPage(currentPage)
```

This will print your firmware version, your number of pages and the current page.
Then it will go to page one, wait a second and go back.
