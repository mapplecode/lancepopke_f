import requests,json,xmltodict
from datetime import datetime
from saleslayerRecord import Fetch_all_api_products
from copy import copy
from tokenHere import token
from items import rus

HereToken = token()
SUBHEADER = {
        'Authorization': f'Bearer {HereToken}',
        'Content-Type': 'application/json'
    }
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
                requests.request("POST", url, headers=SUBHEADER, data=payload).text                        
    except Exception as e:
        pass
createCategory()

def getcategory():
    AllCategoryListHere = list()
    url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/query?query=select * from Item where Type='Category'&minorversion=4"
    response = requests.request("GET", url, headers=SUBHEADER)
    data_dict = dict(xmltodict.parse(response.text))
    if data_dict.get('IntuitResponse').get('QueryResponse') == None:
        print("None Value of Category +++++++++++++++++++++++")       
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
                    # url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/item?minorversion=4" 
                    # payload = json.dumps({
                    # "Name": 'brandname',
                    # "Type": "Category"
                    # })
                    # requests.request("POST", url, headers=SUBHEADER, data=payload).text
                    # createCategory()
            except Exception as e:
                pass
            
    return storeSalesLayer
    
MatchCategory()

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
                reasponse = requests.request("POST", url, headers=SUBHEADER, data=payload)
                data_dict = dict(xmltodict.parse(reasponse.text))
                ClassAndIdHere.append({"ClassNameHere":data_dict.get('IntuitResponse').get('Class').get('Name'),"ClassIdHere":data_dict.get('IntuitResponse').get('Class').get('Id')})
        except Exception as e:
            pass
createClass()

def MatchClassHere():
    url = "https://quickbooks.api.intuit.com/v3/company/9130354741563326/query?query=select  * from Class&minorversion=65"
    response = requests.request("GET", url, headers=SUBHEADER)
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
        print(getItem_Result,'+++++++++++++++++++++++++++++++')
        data = rus(getItem_Result)



 

