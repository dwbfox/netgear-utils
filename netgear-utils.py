'''
     Netgear Utils
'''
 
import urllib2
 
try:
    from bs4 import BeautifulSoup as bs
except:
    raise 
  
class Router(object):
     
    def __init__(self,username,password,routerip):
 
        self.user = username
        self.passwd = password
        self.routerip = routerip
 
    def request(self,url):
        try:
            url = 'http://%s%s' % (self.routerip,url)
            pMan = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pMan.add_password(None,url,self.user,self.passwd)
            hAuth = urllib2.HTTPBasicAuthHandler(pMan)
            opener = urllib2.build_opener(hAuth)
            urllib2.install_opener(opener)
            return urllib2.urlopen(url).read()
        except:
            return False
         
    def current_status(self):
        url = '/s_status.htm&todo=cfg_init'
        data = self.request(url)
        soup = bs(data)        
        return soup.find('td',text='Modem Status').find_next_sibling().text
 
 
    def downstream(self):
        url = '/s_status.htm&todo=cfg_init'
        data =  self.request(url)
        soup = bs(data)
        return soup.find('td', text='DownStream Connection Speed').find_next_sibling().text
 
    def upstream(self):
        url = '/s_status.htm&todo=cfg_init'
        data =  self.request(url)
        soup = bs(data)
        return soup.find('td', text='DownStream Connection Speed').find_next_sibling().text
 
    def attached_devices(self):
        devices = []
        data = self.request('/setup.cgi?todo=nbtscan&next_file=devices.htm')
         
        if data == False:
            return "Unable to contact router."
        soup = bs(data)
        
        tds =  soup.findAll('table')[1].findAll('td')
        for child in tds:
            item = child.find('b')
 
            if item != None:
                devices.append  (item.text.strip())
             
        return devices
 
 
 
mynetgear = Router('yourusername','yourpass','192.168.0.1') # and your netgear router's IP
 
 
while True:
 
    print "Contacting router and querying attached devices..."
    print mynetgear.attached_devices()
     
    print "\nChecking downstream..."
    print mynetgear.downstream()
     
    print "\nChecking upstream..."
    print mynetgear.upstream()
 
    print "\nChecking current router status..."
    print mynetgear.current_status()
