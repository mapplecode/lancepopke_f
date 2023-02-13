import requests,json,xmltodict
from datetime import datetime
from saleslayerRecord import Fetch_all_api_products
from copy import copy
from tokenHere import token


HereToken = token()
print(HereToken,"____________________________________--")
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
                url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/item?minorversion=4"
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
createCategory()  
def getcategory():
    AllCategoryListHere = list()
    url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/query?query=select * from Item where Type='Category'&minorversion=4"
    payload = ""
    headers = {'Authorization': f'Bearer {HereToken}'}
    response = requests.request("GET", url, headers=headers, data=payload)
    data_dict = dict(xmltodict.parse(response.text))
    if data_dict.get('IntuitResponse').get('QueryResponse') == None:
        print("None Value of Category +++++++++++++++++++++++")
        createCategory()
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
            try:
                if saleslayer.get('brand_name') == category.get('GetNameHere'):  
                    StoreCategoryHere = copy(saleslayer)
                    StoreCategoryHere['Category_Id'] = category.get('HereIdHere')
                    StoreCategoryHere['categorycreate_time'] = category.get('CreateTime')
                    storeSalesLayer.append(StoreCategoryHere)
                # else:
                    # print("Creating New category______________________________________")
                    # createCategory()
            except Exception as e:
                pass
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
                url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/class?minorversion=65"
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
createClass()

def MatchClassHere():
    url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/query?query=select  * from Class&minorversion=65"
    headers = {'Authorization': f'Bearer {HereToken}'}
    response = requests.request("GET", url, headers=headers)
    data_dict = dict(xmltodict.parse(response.text))
    if data_dict.get('IntuitResponse').get('QueryResponse') == None:
        print("None Value of Class +++++++++++++++++++++++")
        createClass()
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
            # else:
            #     createClass()
    return NewlistHeres

def CreateItem():
    try:
        AllRecordsHere = MatchClassHere() 
        for dt in AllRecordsHere:
            if dt.get('barcode'):
                barcode = dt.get('barcode')
            else:
                barcode = dt.get('refrence') 
            product_refrence = dt.get('refrence')
            product_image = dt.get('image')
            product_name = dt.get('name')
            print(product_name)
            product_size = dt.get('size')
            brandname = dt.get('brand_name')
            classfication = dt.get('classfication')
            suplier_item_name = dt.get('suplier_item_name')
            brand_Subcategory = dt.get('brand_Subcategory')
            preferred_Supplier = dt.get('preferred_Supplier')
            Category_Id = dt.get('Category_Id')
            if dt.get('Units_hand'):
                quantity = dt.get('Units_hand')
            else:
                quantity = 0   
            categorycreate_time = dt.get('categorycreate_time')  
            GetClassId = dt.get('GetClassId')
            url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/item?minorversion=65"
            payload = json.dumps({
                "Name": barcode,
                "Sku": product_refrence,
                "Description":  product_name + " " + product_size ,
                "Active": True,
                "SubItem": True,
                "ParentRef": {
                    "value": Category_Id,
                    "name": brandname,
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
                "QtyOnHand": quantity,
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
            break
        
    except Exception as e:
        pass
                  
CreateItem()



def GetAllItems():
    startPosition = 0
    maxResults = 1000
    companyId = 9130354741563326
    Boolean = True
    try:
        while Boolean:
            url = f"https://quickbooks.api.intuit.com/v3/company/{companyId}/query?query=SELECT * FROM Item STARTPOSITION {startPosition} MAXRESULTS {maxResults}&minorversion=4"
            response = requests.request("GET", url, headers=SUBHEADER)
            data_dict = dict(xmltodict.parse(response.text))
            Records = data_dict.get('IntuitResponse').get('QueryResponse').get('Item')
            if data_dict.get('IntuitResponse').get('QueryResponse') == None:
                Boolean = False
            startPosition += maxResults
            yield data_dict
    except Exception as e:
        pass
data = GetAllItems()
count = 0
AllSalesRecords = MatchClassHere()
Item_result = [j.get('Sku') for entry in data for j in entry.get('IntuitResponse').get('QueryResponse').get('Item')]
Sales_Results = [sales for sales in AllSalesRecords]
for getItem_Result in Sales_Results:
    if getItem_Result.get('refrence') not in Item_result:
        CreateItem()
        
        
        
def updateitem():
    newList = list()
    AllItemHere = GetAllItems()
    AllRecordsHere = MatchClassHere()
    for showrecords in AllRecordsHere:
        for showitem in AllItemHere:
            if showrecords.get('name') == showitem.get('ProductNameHere'):
                FilterRecords = copy(showrecords)
                FilterRecords['ProductId'] =  showitem.get('ProductId')
                FilterRecords['SyncToken'] = showitem.get('ProductTokenHere')
                FilterRecords['Product_Name'] = showitem.get('ProductNameHere')
                newList.append(FilterRecords)
                print(newList,)
               
    for items_data in newList:
        url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/item?minorversion=40"
        payload = json.dumps({
        "Name": "tesrrrrrrs",
        "Sku": "product_refrence",
        "Id": items_data.get('ProductId'),
        "SyncToken": items_data.get('ProductTokenHere'),
        "Description": "product_name",
        "Active": True,
        "Taxable": False,
        "SalesTaxIncluded": False,
        "Type": "Inventory",
        "IncomeAccountRef": {
            "value": "15",
            "name": "Sales of Product Income"
        },
        "PurchaseDesc": "product_namessss",
        "PurchaseCost": 35,
        "PurchaseTaxIncluded": False,
        "ExpenseAccountRef": {
            "value": "16",
            "name": "Cost of Goods Sold"
        },
        "AssetAccountRef": {
            "value": "17",
            "name": "Inventory Asset"
        },
        "TrackQtyOnHand": True,
        "QtyOnHand": 8,
        "InvStartDate": "2022-11-01"
        })
        response = requests.request("POST", url, headers=SUBHEADER, data=payload)
        print(response.text)
updateitem()



