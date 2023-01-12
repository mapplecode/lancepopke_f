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
        pass
        
def getcategory():
    import requests
    AllCategoryListHere = list()
    url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/query?query=select * from Item where Type='Category'&minorversion=4"
    payload = ""
    headers = {'Authorization': f'Bearer {HereToken}'}
    response = requests.request("GET", url, headers=headers, data=payload)
    data_dict = dict(xmltodict.parse(response.text))
    GetresponseHere = data_dict.get('IntuitResponse').get('QueryResponse').get('Item')
    for showResponse in GetresponseHere:
        AllCategoryListHere.append({"HereIdHere":showResponse.get('Id'),"GetNameHere":showResponse.get('Name'),"CreateTime":showResponse.get('MetaData').get('CreateTime')})
    return AllCategoryListHere



def getcategoryRecordsFromXml():
    mst = timezone('MST')
    store = datetime.now(mst)
    from datetime import timedelta
    GetCurrent_MSTTime = str(store).split('.')[0]
    getnewList = list()
    StoreCategoryHere = getcategory()
    
    for getcat in StoreCategoryHere:
        storeId = getcat.get('HereIdHere')
        storeName = getcat.get('GetNameHere')
        storeCreateDate = getcat.get('CreateTime')
        n = str(storeCreateDate).replace('T'," ").split('-08:00')[0]
        datetime_object = datetime.strptime(n, '%Y-%m-%d %H:%M:%S')
        currentdt= GetCurrent_MSTTime
        currentobj = datetime.strptime(currentdt, '%Y-%m-%d %H:%M:%S')
        minus = currentobj-datetime_object
        getnewList.append({"Name":storeName,"Date":storeCreateDate,"Id":storeId})
    return getnewList

def createClass():
    ClassAndIdHere = list()
    all_pro = Fetch_all_api_products()
    removeduplicateValue = list()
    lst =[i.get('classfication') for i in all_pro]
    for i in lst:
        if i not in removeduplicateValue:
            removeduplicateValue.append(i) 
    for classification in removeduplicateValue:
        try:
            if classification!='':
                url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/class?minorversion=65"
                payload = json.dumps({
                    "Name": classification,
                })    
                headers = {
                'Authorization': f'Bearer {HereToken}',
                'Content-Type': 'application/json'}
                reasponse = requests.request("POST", url, headers=headers, data=payload)
                data_dict = dict(xmltodict.parse(reasponse.text))
                
                ClassAndIdHere.append({"ClassNameHere":data_dict.get('IntuitResponse').get('Class').get('Name'),"ClassIdHere":data_dict.get('IntuitResponse').get('Class').get('Id')})
        except Exception as e:
            pass
    return ClassAndIdHere
from copy import copy


def CreateItem():
    import requests
    import json
    data = getcategoryRecordsFromXml()
    AllClassRecordsListHere = list()

    classdata = createClass()
    all_pro = Fetch_all_api_products()
    for product in all_pro:
        for category in data:
            for i in classdata:
                new_item = copy(product)
                new_item['ClassNameHere'] = i.get('ClassNameHere')
                new_item['ClassIdHere'] = i.get('ClassIdHere')
                new_item['Category_Name'] = category.get('Name')
                new_item['Category_Date'] = category.get('Date')
                new_item['Category_Id'] = category.get('Id')
                AllClassRecordsListHere.append(new_item)
    for dt in AllClassRecordsListHere:
        
        barcode = dt.get('barcode')
        if barcode:
            product_refrence = dt.get('refrence')
            product_image = dt.get('image')
            product_name = dt.get('name')
            product_size = dt.get('size')
            brandname = dt.get('brand_name')
            url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/item?minorversion=65"
            payload = json.dumps({
                "Name": barcode,
                "Sku": product_refrence,
                "Description":  product_name + " " + product_size ,
                "Active": True,
                "SubItem": True,
                "ParentRef": {
                    "value": '46',
                    "name": dt.get('Category_Name')
                },
                "Type": "Inventory",
                "IncomeAccountRef": {
                    "value": "67",
                    "name": "Sales of Product Income"
                },
                "PurchaseDesc": product_name,
                "PurchaseTaxIncluded": False,
                "PurchaseCost": 0,
                "ExpenseAccountRef": {
                    "value": "84",
                    "name": "Cost of Goods Sold"
                },
                "AssetAccountRef": {
                    "value": "85",
                    "name": "Inventory Asset"
                },
                "TrackQtyOnHand": True,
                "QtyOnHand": 1,
                "InvStartDate": "2023-01-03",
                "ClassRef": {
                    "value": dt.get('ClassIdHere'),
                    "name": dt.get('ClassNameHere'),
                },
                
            })
            headers = {
            'Authorization': f'Bearer {HereToken}',
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
            break
        
        
                
CreateItem()