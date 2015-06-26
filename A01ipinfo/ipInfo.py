import requests
import socket
import uuid
import re

def get_ip_from_taobao():
    global code, external_ip, country_id, location, isp, source, headers
    url = "http://ip.taobao.com/service/getIpInfo.php"
    req = requests.get(url, params="ip=myip", headers=headers)
    code = eval(req.content)['code']
    if code == 0:
        external_ip = eval(req.content)['data']['ip']
        country_id = eval(req.content)['data']['country_id']
        country = eval(req.content)['data']['country'].decode('unicode_escape')
        area = eval(req.content)['data']['area'].decode('unicode_escape')
        region = eval(req.content)['data']['region'].decode('unicode_escape')
        city = eval(req.content)['data']['city'].decode('unicode_escape')
        county = eval(req.content)['data']['county'].decode('unicode_escape')
        isp = eval(req.content)['data']['isp'].decode('unicode_escape')
        location = country + area + region + city + county
        source = 'ip.taobao.com'

def get_ip_from_sohu():
    global code, external_ip, country_id, location, isp, source, headers
    url = "http://pv.sohu.com/cityjson"
    req = requests.get(url, headers=headers)
    data = re.search('\{.*?\}', req.content).group()
    external_ip = eval(data)['cip']
    location = eval(data)['cname']
    source = 'pv.sohu.com'
    if external_ip == '0':
        code = 1

def show_result():
    if code == 1:  # Fail to obtain information
        print "All ip API sources are broken. Please modify the code for future uses!"
    else:
        print "The host name is: " + host_name
        print "The mac addresss is: {}".format(mac_addr)
        print "Interal IP Addr: {}".format(internal_ip)
        print "External IP Addr: {}".format(external_ip)
        print "The country code is: {}".format(country_id)
        print "The location is " + location
        print "The isp provider is " + isp
        print "The information is gathered from: {}".format(source)

# something wrong with mac
def get_local_info():
    global internal_ip, host_name, mac_addr
    internal_ip = socket.gethostbyname(socket.gethostname())
    host_name = socket.getfqdn(socket.gethostname())
    mac_addr = uuid.UUID(int = uuid.getnode()).hex[-12:]
    mac_addr = ":".join([mac_addr[e:e+2] for e in range(0, 11, 2)])

code, external_ip, country_id, location, isp, source, internal_ip, host_name, mac_addr = 0, '0', '0', '0', '0', '0', '0', '0', '0'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}

get_ip_from_taobao()
#get_ip_from_sohu()
get_local_info()
show_result()
