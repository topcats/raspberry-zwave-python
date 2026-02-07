# raspberry-zwave-python

Raspberry PI Z-Wave board Python Interface
Provides a quick and easy interface into the ZWAY Automation API

> This was orignally  written for Python 2.7.  
> But there now is a Python 3 version.

*Due to the way Python 2 and Python 3 work, there are 2 different libraries, but the calls and functionally remains the same.*

## How to Use - Python 3

```python
from zWaveApi3 import *

oZWave = zWaveApi3('username', 'password', 'zwaveurl')
oZDevices = oZWave.getDevices()
```

## How to Use - Python 2

```python
from zWaveApi import *

oZWave = zWaveApi('username', 'password', 'zwaveurl')
oZDevices = oZWave.getDevices()
```

## Requires

* json
* Python 3
  * http.client
  * json

* Python 2:
  * urllib2
  * urllib
  * httplib

## Functions

### getDevices()

Returns a list of zWave Devices as a JSON array

### setDeviceCommand(deviceid, newcommand)

Sends a Command to a zWave Device

* **deviceid** - The unique zWave device ID
* **newcommand** - The Require command for the device  
    This depends on the device type, see below
  * switchMultilevel : on / off / min / max / exact?level=40 / increase / decrease / update
  * switchBinary     : on / off / update
  * toggleButton     : on

**Returns** either 1 or 0 dependant on command being accepted
