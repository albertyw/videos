import urllib
import time
import mysql
'''
This class manages communications between us and the server
@author: Albert Wang
'''
class Comm(urllib.FancyURLopener):
    version="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 GTB6"
    def __init__(self):
        urllib.FancyURLopener.__init__(self)
        self.mysql = mysql.Mysql()
        self.latencyAverageComputeTime = 0
        pass
    
    def open(self, fullurl, data=None, recordLatency = True):
        return urllib.FancyURLopener.open(self,fullurl,data)
        
    def prompt_user_passwd(self,host, realm):
        return ('movies','m00vi3s')
        
