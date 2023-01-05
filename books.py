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
    root = ET.Element(store) 
    xml_data = ET.tostring(root) 
    with open('coordinates.xml', 'w') as f:  
        f.write(xml_data.decode('utf-8'))

    
# getcategory()

def getcategoryRecordsFromXml():
   
    mst = timezone('MST')
    store = datetime.now(mst)
    from datetime import timedelta
    GetCurrent_MSTTime = str(store).split('.')[0]
    getnewList = list()
    tree = ET.parse('GFG.xml')
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
    data_dict = dict(xmltodict.parse(xmlstr))
    print(data_dict,"==")
    
    
    
getcategoryRecordsFromXml()  
        
        
        
        
        
        
        
    #     d = xmltodict.parse(fd.read())
    #     print(d,"==")
    # with open('sample.xml', 'r') as xml_file:
    #     data_dict = xmltodict.parse(xml_file.read())
    #     # data_dict = f.read()
    #     print(data_dict)
         
        # storeResponse = data_dict.get('IntuitResponse').get('QueryResponse').get('Item')
        # for getresponse in storeResponse:
        #     storeName = getresponse.get('Name')
        #     storeCreateDate = getresponse.get('MetaData').get('CreateTime')
        #     storeId = getresponse.get('Id')

        #     n = str(storeCreateDate).replace('T'," ").split('-08:00')[0]
        #     datetime_object = datetime.strptime(n, '%Y-%m-%d %H:%M:%S')
            
        #     currentdt= GetCurrent_MSTTime
        #     currentobj = datetime.strptime(currentdt, '%Y-%m-%d %H:%M:%S')
        #     minus = currentobj-datetime_object

        #     if len(str(minus)) <8:
        #         getnewList.append({"Name":storeName,"Date":storeCreateDate,"Id":storeId})
        #         print(getnewList,'---------------------------------------------')
    # return getnewList
    
# getcategoryRecordsFromXml()  

# def CreateItem():
#     import requests
#     import json
#     data = getcategoryRecordsFromXml()
#     all_pro = Fetch_all_api_products()
#     for product in all_pro:
#         barcode = data.get('barcode')
#         if barcode:
#             product_refrence = product.get('refrence')
#             product_image = product.get('image')
#             product_name = product.get('name')
#             product_size = product.get('size')
        
#     for i in data:
#         print(i,'==========================')
#         # url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/item?minorversion=65"
#         # payload = json.dumps({
#         # "Name": barcode,
#         # "Sku": product_refrence,
#         # "Active": True,
#         # "Description" : product_name + " " + product_size ,
#         # "PurchaseDesc": product_name,
#         # "SubItem": True,
#         # "ParentRef": {
#         #     "value": i.get('Id'),
#         #     "name": i.get('Name')
#         # },
#         # "TrackQtyOnHand": True,
#         # "QtyOnHand": 12,
#         # "Type": "Inventory",
#         # "IncomeAccountRef": {
#         #     "value": "79",
#         #     "name": "Sales of Product Income"
#         # },
#         # "PurchaseDesc": "This is purchasing information",
#         # "PurchaseCost": 0,
#         # "ExpenseAccountRef": {
#         #     "value": "80",
#         #     "name": "Cost of Goods Sold"
#         # },
#         # "InvStartDate": "2022-12-28",
#         # "AssetAccountRef": {
#         #     "value": "81",
#         #     "name": "Inventory Asset"
#         # }
#         # })
#         # headers = {
#         # 'Authorization': f'Bearer {HereToken}',
#         # 'Content-Type': 'application/json'
#         # }
        

#         # response = requests.request("POST", url, headers=headers, data=payload)
#         # print(response.text)
    
# CreateItem()