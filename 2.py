import requests,xmltodict
from main import MatchClassHere
from tokenHere import token
HereToken = token()
from copy import copy
from main import CreateItem

SUBHEADER = {
        'Authorization': f'Bearer {HereToken}',
        'Content-Type': 'application/json'
    }



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
count = 0 
# for getItem_Result in Sales_Results:
    
#     if getItem_Result.get('refrence') not in Item_result:
    #     data = rus(dt)
    # print(data,"=========")
    
        
        
        
        
# def updateitem():
#     itemdata= list()
#     newList = list()
#     AllItemHere = GetAllItems()
#     AllRecordsHere = MatchClassHere()
#     count = 0
#     for showrecords in AllRecordsHere:
#         for showitem in AllItemHere:
#             Records = showitem.get('IntuitResponse').get('QueryResponse').get('Item')
#             for data in Records:
#                 itemID = data.get('Id')
#                 itemtoken = data.get('SyncToken')
#                 Name = data.get('Name')
#                 itemdata.append({"ProductId":itemID,"ProductTokenHere":itemtoken,"ProductNameHere":Name})  
#                 FilterRecords = copy(showrecords)
#                 FilterRecords['ProductId'] =  showitem.get('Id')
#                 FilterRecords['SyncToken'] = showitem.get('SyncToken')
#                 FilterRecords['Product_Name'] = showitem.get('Name')
#                 newList.append(FilterRecords)
# #                 print(newList,'+++++++++++++++++++++++++++++++++++++++++++++')

# # updateitem()