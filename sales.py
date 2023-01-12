import requests,random,time,hashlib,base64,json


def Fetch_all_api_products():

    code= "CN21061H4125C8733"
    secrect_key = "35425b44a2182aea38b9be0a2c8445bd"
    unique = random.randrange(10**5)
    timeInSeconds = int(time.time())
    sigString = code + secrect_key + str(timeInSeconds) + str(unique)
    hashling = hashlib.sha256(sigString.encode('utf-8')).hexdigest()

    url  = f"https://api.saleslayer.com/?code={code}&time={timeInSeconds}&unique={unique}&key256={hashling}&ver=1.18&pagination=5000"
    data = requests.get(url = url)
    response = json.loads(data.text)
    all_products_ = response.get('data').get('products')

    all_products = []
    for product in all_products_:
        if product:
            try:
                a_product = {
                    'barcode':product[-9] if product[-9] else '',
                    'refrence':product[4] if product[4] else '',
                    'image':product[8][0][-1] if product[8] and product[8][0] else '',
                    'name':product[5] if product[5] else '',
                    'size':product[16] if product[16] else '',
                    'brand_name':product[-10][0] if product[3] and product[-10][0] else '',
                    'classfication':product[14][0] if product[14] and product[14][0] else '',
                    'suplier_item_name':product[5] if product[5] else '',
                    'brand_Subcategory':product[-4] if product[-4] else '',
                    'preferred_Supplier':product[-3] if product[-3] else '',
                    
                }
                all_products.append(a_product)
            except:
                pass
    return all_products






