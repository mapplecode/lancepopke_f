import requests,json
from sales import Fetch_all_api_products
from tok import token
import xmltodict

HereToken = token()

def createClass():
    try:
        ClassAndIdHere = list()
        all_pro = Fetch_all_api_products()
        removeduplicateValue = list()
        allclass = list()
        lst =[i.get('classfication') for i in all_pro]
        for i in lst:
            if i not in removeduplicateValue:
                removeduplicateValue.append(i)
        for classification in removeduplicateValue:
            if classification!='':
                url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/class?minorversion=65"
                payload = json.dumps({
                    "Name": classification,
                })    
                headers = {
                'Authorization': f'Bearer {HereToken}',
                'Content-Type': 'application/json'
                }
                reasponse = requests.request("POST", url, headers=headers, data=payload)
                allclass.append(reasponse.text)
                data_dict = dict(xmltodict.parse(reasponse.text))
                ClassAndIdHere.append({"ClassNameHere":data_dict.get('IntuitResponse').get('Class').get('Name'),"ClassIdHere":data_dict.get('IntuitResponse').get('Class').get('Id')})
    except Exception as e:
        print(e)
    return ClassAndIdHere

        
    



