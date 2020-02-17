import urllib
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
#install lxml & Beautifulsoup(using cmd "pip install ..."

class wificlass():
    def __init__(self):
        pass

    def connect(self,netName="maze_beacon"):
        self.connectStr = "netsh wlan connect name="+netName
        self.profilePath = r"C:\Users\group1\Desktop\Final_Code_Folder\trialBeacon.xml"  
        os.system("netsh wlan add profile filename="+self.profilePath)
        os.system("netsh wlan disconnect")
        os.system(self.connectStr)

    def getString(self):
        self.url = "http://10.10.10.1"
        self.html = urllib.request.urlopen(self.url).read()
        self.soup = BeautifulSoup(self.html,"lxml")
        self.text = self.soup.get_text()
        return self.text
