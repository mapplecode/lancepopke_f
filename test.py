import requests
import json   
import xmltodict
from datetime import datetime
from pytz import timezone
from sales import Fetch_all_api_products
import xml.etree.cElementTree as ET

from tok import token
HereToken = token()


def getcategory():
    import requests
    url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/query?query=select * from Item where Type='Category'&minorversion=4"
    payload = ""
    headers = {
    'Authorization': f'Bearer {HereToken}'
    }
    response = requests.request("GET", url, headers=headers, data=payload).text
    store = response.replace('<?','?').replace('</IntuitResponse>','</IntuitResponse')
    data = ET.Element(store)
    b_xml = ET.tostring(data)
    with open("GFG.xml", "wb") as f:
        f.write(b_xml)
# getcategory()
import xml.etree.ElementTree as ETree
with open('GFG.xml','r') as f:
    dt = f.read()
    s = str(dt).replace('</IntuitResponse />','</IntuitResponse>')
    data_dict = dict(xmltodict.parse(s))
    print(data_dict,"==")
    
