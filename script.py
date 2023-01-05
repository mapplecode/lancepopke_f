import requests
import json   
import xmltodict
from datetime import datetime
from pytz import timezone
from sales import Fetch_all_api_products
import xml.etree.cElementTree as ET

from tok import token
HereToken = token()

def createCategory():
    try:
        all_pro = Fetch_all_api_products()
        removeduplicateValue = list()
        lst =[i.get('brand_name') for i in all_pro]
        for i in lst:
            if i not in removeduplicateValue:
                removeduplicateValue.append(i)
        for brandname in removeduplicateValue:
            if brandname!='':
                url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/item?minorversion=4"
                payload = json.dumps({
                "Name": brandname,
                "Type": "Category"
                })    
                headers = {
                'Authorization': f'Bearer {HereToken}',
                'Content-Type': 'application/json'
                }
                requests.request("POST", url, headers=headers, data=payload).text
    except Exception as e:
        print(e)
        
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

def getcategoryRecordsFromXml():
   
    mst = timezone('MST')
    store = datetime.now(mst)
    from datetime import timedelta
    GetCurrent_MSTTime = str(store).split('.')[0]
    getnewList = list()
    
    # Convert Xml File To json
    with open('GFG.xml','r') as f:
        dt = f.read()
        s = str(dt).replace('</IntuitResponse />','</IntuitResponse>')
        data_dict = dict(xmltodict.parse(s))
        storeResponse = data_dict.get('IntuitResponse').get('QueryResponse').get('Item')
        for getresponse in storeResponse:
            storeName = getresponse.get('Name')
            storeCreateDate = getresponse.get('MetaData').get('CreateTime')
            storeId = getresponse.get('Id')
            n = str(storeCreateDate).replace('T'," ").split('-08:00')[0]
            datetime_object = datetime.strptime(n, '%Y-%m-%d %H:%M:%S')
            currentdt= GetCurrent_MSTTime
            currentobj = datetime.strptime(currentdt, '%Y-%m-%d %H:%M:%S')
            minus = currentobj-datetime_object
            if len(str(minus)) <8:
                getnewList.append({"Name":storeName,"Date":storeCreateDate,"Id":storeId})
    # print(getnewList,'---------------------------------------------')
    return getnewList
    
getcategoryRecordsFromXml()  

def CreateItem():
    import requests
    import json
    data = getcategoryRecordsFromXml()
    all_pro = Fetch_all_api_products()
    for product in all_pro:
        barcode = data.get('barcode')
        if barcode:
            product_refrence = product.get('refrence')
            product_image = product.get('image')
            product_name = product.get('name')
            product_size = product.get('size')
        
    for i in data:
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/item?minorversion=65"
        payload = json.dumps({
        "Name": barcode,
        "Sku": product_refrence,
        "Active": True,
        "Description" : product_name + " " + product_size ,
        "PurchaseDesc": product_name,
        "SubItem": True,
        "ParentRef": {
            "value": i.get('Id'),
            "name": i.get('Name')
        },
        "TrackQtyOnHand": True,
        "QtyOnHand": 12,
        "Type": "Inventory",
        "IncomeAccountRef": {
            "value": "79",
            "name": "Sales of Product Income"
        },
        "PurchaseDesc": "This is purchasing information",
        "PurchaseCost": 0,
        "ExpenseAccountRef": {
            "value": "80",
            "name": "Cost of Goods Sold"
        },
        "InvStartDate": "2022-12-28",
        "AssetAccountRef": {
            "value": "81",
            "name": "Inventory Asset"
        }
        })
        headers = {
        'Authorization': f'Bearer {HereToken}',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    
CreateItem()