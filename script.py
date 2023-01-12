import requests,json,xmltodict
from datetime import datetime
from saleslayerRecord import Fetch_all_api_products
from copy import copy
from tokenHere import token

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


def MatchCategory():
    storeSalesLayer = list()
    GetsalesLayerRecords = Fetch_all_api_products()
    getcategoryRecordsHere = getcategory()
    for saleslayer in GetsalesLayerRecords: 
        for category in getcategoryRecordsHere:
            if saleslayer.get('brand_name') == category.get('GetNameHere'):
                StoreCategoryHere = copy(saleslayer)
                StoreCategoryHere['Category_Id'] = category.get('HereIdHere')
                StoreCategoryHere['categorycreate_time'] = category.get('CreateTime')
                storeSalesLayer.append(StoreCategoryHere)
    return storeSalesLayer

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



def MatchClassHere():
    url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/query?query=select  * from Class&minorversion=65"
    headers = {'Authorization': f'Bearer {HereToken}'}
    response = requests.request("GET", url, headers=headers)
    data_dict = dict(xmltodict.parse(response.text))
    GetresponseHere = data_dict.get('IntuitResponse').get('QueryResponse').get('Class')
    MatchCategoryHere = MatchCategory()
    NewlistHeres = list()
    for category in MatchCategoryHere:
        for GetClass in GetresponseHere:
            if category.get('classfication') == GetClass.get('Name'):
                if GetClass.get('Name') != None and category.get('classfication')!= None :
                    new_items = copy(category)
                    new_items['GetClassId'] = GetClass.get('Id')
                    NewlistHeres.append(new_items)
    return NewlistHeres


def CreateItem():
    try:
        AllRecordsHere = MatchClassHere()
        count = 0
        for dt in AllRecordsHere:
            if dt.get('barcode'):
                barcode = dt.get('barcode')
                product_refrence = dt.get('refrence')
                product_image = dt.get('image')
                product_name = dt.get('name')
                product_size = dt.get('size')
                brandname = dt.get('brand_name')
                classfication = dt.get('classfication')
                suplier_item_name = dt.get('suplier_item_name')
                brand_Subcategory = dt.get('brand_Subcategory')
                preferred_Supplier = dt.get('preferred_Supplier')
                Category_Id = dt.get('Category_Id')
                categorycreate_time = dt.get('categorycreate_time')  
                GetClassId = dt.get('GetClassId')
                url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/item?minorversion=65"
                payload = json.dumps({
                    "Name": barcode,
                    "Sku": product_refrence,
                    "Description":  product_name + " " + product_size ,
                    "Active": True,
                    "SubItem": True,
                    "ParentRef": {
                        "value": Category_Id,
                        "name": brandname
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
                        "value": GetClassId,
                        "name": classfication,
                    },
                    
                })
                headers = {
                'Authorization': f'Bearer {HereToken}',
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text,"========")
    except Exception as e:
        pass                 
CreateItem()
