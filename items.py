import requests,json
from tokenHere import token
HereToken = token()
SUBHEADER = {
        'Authorization': f'Bearer {HereToken}',
        'Content-Type': 'application/json'
    }
def rus(dt):
    if dt.get('barcode'):
        barcode = dt.get('barcode')
    else:
        barcode = dt.get('refrence') 
    product_refrence = dt.get('refrence')
    product_cost = dt.get('cost')
    product_image = dt.get('image')
    product_name = dt.get('name')
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
        "Description": product_name + " " + product_size,
        "Active": True,
        "SubItem": True,
        "ParentRef": {
            "value": Category_Id,
            "name": brandname
        },
        
        "Taxable": False,
        "SalesTaxIncluded": False,
        "Type": "Inventory",
        "IncomeAccountRef": {
        "value": "15",
        "name": "Sales of Product Income"
        },
        "PurchaseDesc":  product_name,
        "PurchaseCost": product_cost,
        "QtyOnHand": quantity,
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
        "QtyOnHand": quantity,
        "ClassRef": {
            "value": GetClassId,
            "name": classfication,
        },
        "InvStartDate": "2022-11-01",
                        
    })
    response = requests.request("POST", url, headers=SUBHEADER, data=payload)
    return response
