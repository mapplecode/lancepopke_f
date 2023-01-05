import requests,json


def Fetch_all_api_products():
    url = "https://api.saleslayer.com/?code=CN21061H4125C8733&time&unique&key=89dd1d3ad5c849eb6ac4b04a36cbd553"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    all_products_ = data.get('data').get('products')
    all_products = []
    for product in all_products_:
        if product:
            try:
                a_product = {
                    'barcode':product[-2] if product[-2] else '',
                    'refrence':product[4] if product[4] else '',
                    'image':product[8][0][-1] if product[8] and product[8][0] else '',
                    'name':product[5] if product[5] else '',
                    'size':product[14] if product[14] else '',
                    'brand_name':product[-3][0] if product[-3] and product[-3][0] else '',
                    'classfication':product[12][0] if product[12] and product[12][0] else '',
                    'suplier_item_name':product[5] if product[5] else '',
                    
                }
                all_products.append(a_product)
            except:
                print(product)
    
    return all_products
