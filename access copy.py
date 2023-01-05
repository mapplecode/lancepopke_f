def getToken():
    try:
        import requests,json
        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        payload='grant_type=refresh_token&refresh_token=AB11681363978NIOQ8mtWb1SPz1ZWFeh6X4iF8FIL9xaz07Gfi'
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic QUJCbEpVc2lXQnQ2VjVRWlpjcTBpVW4zSjlQTElXT0ZBR1hpaDlUaXlycFFKd1Bna0M6WVB5Mml2OWFNQVlZa2RDS3dYSXFNVjIxUHplUkgzOWMxRmR2UHdubw=='
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text).get('access_token')

        return result
    except Exception as e:
        print(e)
getToken()


