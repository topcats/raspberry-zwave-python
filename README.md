# raspberry-zwave-python
Raspberry PI Z-Wave board Python Interface

>This is currently written for Python 2.7, but there is the intention to make a Python 3 version.


## How to Use

```python
from zWaveApi import *

oZWave = zWaveApi('username', 'password', 'zwaveurl')
oZDevices = oZWave.getDevices()

```


## Requires
* urllib2
* urllib
* httplib
* base64
* json
* time
* socket


## Functions

### getDevices()
Returns a list of json Devices

### setDeviceCommand(deviceid, newcommand)
newcommand options:
* switchMultilevel on / off / min / max / exact?level=40 / increase / decrease / update
* switchBinary on / off / update
* toggleButton on

Returns either 1 or 0 dependant on command being accepted