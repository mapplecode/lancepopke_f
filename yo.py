import requests
import json

url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365266478670/item?minorversion=65"

payload = json.dumps({
  "Name": "cTITRUUR",
  "Description": "llhis isici ic",
  "Active": True,
  "SubItem": True,
  "ParentRef": {
    "value": "46",
    "name": "Testing Category 11122222"
  },
  "Type": "Inventory",
  "IncomeAccountRef": {
    "value": "67",
    "name": "Sales of Product Income"
  },
  "PurchaseDesc": "test for this",
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
  "QtyOnHand": 2,
  "InvStartDate": "2023-01-03",
  "ClassRef": {
    "value": "5100000000000043150",
    "name": "France"
  }
})
headers = {
  'Authorization': 'Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..CzanzQOEImObT4RW76sXPg.oy68qRDnxzLfiU26ehYvugbD1n-lxw_60iLrlbcLFQ0OU4YPxU7dong_yhsnh6iUSuPyJANG3AheIxa7juJDKaUJFt3clN8kaZMocE8GghX7eyAlyWfLi1rM7USBwOoUIVROzU9aIC2BxBvHeLpnSsvgduNG9mQbewvRiTx6qLI2oBEXaLk9ofTmJ7l2Iw3RTYFCcPERz_JR9wlVHNsEPaHU2_pLVFlQlsUSCGoQcGKlY3E2b-r47DEF0pDgOa85jWKV7T8OnnRDy3GVODDdNTHZL_1SzGMYM4pXh-RLa9BXK4mzUEZHgnHCHknyqT8MbmzZCTIbNUZuAvvJvn3e2Pb1bjMdGtljD8E43bJYCUGpSz6bm7Wyl6iGa3eYY7xWV23Fa1S4rezKTudztcT6PLqBzajKCOvWc3JjREO1j4IHzXZl2F3Wp7q6ARabJzzKZ-lhB9dlx4874IWqgdLWWyJmaMSOQJ1yYlLAINJUixdQ6YqFzGnrU7EsSzOVSwogNykzS3lUXL_6qC13cZ5nhjrvhBLpAmzo5LTrYKcR1t7fNBNIq70o9pDGRXLce2xHCLu5Gy0yw9Jqt_ZtTLjEHxGxuhHlmr-5ZV-tC-IwbYtGDjRBtY8AWB-L3_Z5bBhJc4KvWiKvXphOEqtGc26yrjcx1_eDQVPSJ8jAmQe0VwBYEVp2CEuxun4rEJ0pmkb0BCR1z0oveOBHwjQokqH43VYDUVj4d9NC4Uzoq3StyFWUjhMHAMP4mlTslG9YJ8HV-TPig8d5o4IcA5VQlS1QpeCjoolj6_pDwyTl22KZzammB6JyBnj_wRbK0MfGfhLkJ-PusDfI-KejyJrZT0L1xqg4apbcs58kfqWorwo5S4P7qnXYsSKBIWo0cKqPRPMXXzy0xcuZIio0GYelkaOxTg.H8HhucCCdhLQQSLcbUXc3g',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)



