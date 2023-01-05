def token():
    import requests
    import json

    url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

    payload='grant_type=refresh_token&refresh_token=AB11681555183tzu0f0Hcl33JA56abbIwQ24XIfRQuY1GGjGpa'
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic QUJCbEpVc2lXQnQ2VjVRWlpjcTBpVW4zSjlQTElXT0ZBR1hpaDlUaXlycFFKd1Bna0M6WVB5Mml2OWFNQVlZa2RDS3dYSXFNVjIxUHplUkgzOWMxRmR2UHdubw=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    js = json.loads(response.text).get('access_token')
    return js

# data = token()
# print(data,'------------------------------------')
