import http.client
import json

class zWaveApi3(object):
    """
    zWave zWay Automation API access

    This is a library for Python 3

    from https://github.com/topcats/raspberry-zwave-python

    Methods:
        getDevices       - Gets a full List of zWave Devices
        setDeviceCommand - Sends a command to a zWave Device

    Init Variables:
        zUsername - Username with access to API
        zPassword - password for API
        zBaseUrl  - full url for the ZAutomation api path
    """
    
    __zlogin_cookie = ''
    __zlogin_username = ''
    __zlogin_password = ''
    __zlogin_apibaseURL = 'http://localhost:8083/ZAutomation/api/v1/'
    __strServer = 'localhost:8083'
    __strServerPath = ''


    def __init__(self, zUsername, zPassword, zBaseUrl):
        """
        zWave zWay Automation API access

        :param zUsername: Username with access to API
        :type zUsername: string
        :param zPassword: password for API
        :type zPassword: string
        :param zBaseUrl: full url for the ZAutomation api path
        :type zBaseUrl: string
        """

        self.__zlogin_username = zUsername
        self.__zlogin_password = zPassword
        self.__zlogin_apibaseURL = zBaseUrl
        self.__strServer = self.__zlogin_apibaseURL.replace('http://', '')
        self.__strServer = self.__strServer[:self.__strServer.index('/')]
        self.__strServerPath = self.__zlogin_apibaseURL.replace('http://'+self.__strServer,'')


    def __DoLogin(self):
        """
        Does the initial authentication before anything else
        Is run only when needed, you do not need to run directly.

        :return: HTTP Response code from login attempt
        :rtype: integer
        """

        try:
            post_login = json.dumps({'form': True, 'login': self.__zlogin_username, 'password': self.__zlogin_password, 'keepme': False, 'default_ui': 1})
            webheaders = {"Content-type": "application/json", "Accept": "application/json"}
            webconn = http.client.HTTPConnection(self.__strServer)
            webconn.request("POST", self.__strServerPath+'login', body=post_login.encode(), headers=webheaders, encode_chunked=False)
            webresponse = webconn.getresponse()
            webresponseCookie = webresponse.getheader('set-cookie') # ['ZWAYSession']
            webresponseCookie = webresponseCookie.replace(' ','')
            webresponseCookie = webresponseCookie[webresponseCookie.index('ZWAYSession='):].replace('ZWAYSession=','')
            webresponseCookie = webresponseCookie[:webresponseCookie.index(';')]
            self.__zlogin_cookie = webresponseCookie
            webconn.close()
            return webresponse.status
        except:
            self.__zlogin_cookie == ''
            return 0


    def getDevices(self):
        """
        Get a list of all zWave Devices

        :return: JSON Object of zWave Devices
        :rtype: JSON Object
        """

        # Double check login
        if (self.__zlogin_cookie == ''):
            self.__DoLogin()

        try:
            if (self.__zlogin_cookie == ''):
                raise ValueError('Login Failed')
            webheaders = {'Content-type': 'application/json', "Accept": "application/json", "Cookie": "ZWAYSession="+self.__zlogin_cookie}
            webconn = http.client.HTTPConnection(self.__strServer)
            webconn.request("GET", self.__strServerPath+'devices?since=0', '', webheaders)
            webresponse = webconn.getresponse()
            webdata = webresponse.read()
            webconn.close()
            json_obj = json.loads(webdata.decode())
            return json_obj['data']['devices']
        except:
            return []


    def setDeviceCommand(self, deviceid, newcommand):
        """
        Send a Command to a zWave Device

        Init Variables:
            deviceid   - The unique zWave device ID
            newcommand - The Require command for the device
                         This depends on the device type, see below

        switchMultilevel : on / off / min / max / exact?level=40 / increase / decrease / update
        switchBinary     : on / off / update
        toggleButton     : on

        :param deviceid: zWave Device ID
        :type deviceid: string
        :param newcommand: Command to send to Device
        :type newcommand: string
        :return: 1 if successful, 0 if failed
        :rtype: integer
        """

        # Double check login
        if (self.__zlogin_cookie == ''):
            self.__DoLogin()

        # Check inputs
        if (deviceid == ''):
            return 0
        if (newcommand == ''):
            return 0

        # Do Command
        try:
            if (self.__zlogin_cookie == ''):
                raise ValueError('Login Failed')
            webheaders = {'Content-type': 'application/json', "Accept": "application/json", "Cookie": "ZWAYSession="+self.__zlogin_cookie}
            webconn = http.client.HTTPConnection(self.__strServer)
            webconn.request("GET", self.__strServerPath+'devices/'+deviceid+'/command/'+newcommand, '', webheaders)
            webresponse = webconn.getresponse()
            webdata = webresponse.read()
            webconn.close()

            # Check Response
            json_obj = json.loads(webdata.decode())
            if (json_obj['code'] == 200):
                return 1
            else:
                return 0
        except:
            return 0
