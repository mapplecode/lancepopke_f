def token():
    import requests
    import json

    url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

    payload='grant_type=refresh_token&refresh_token=AB11684927586gxf9PI1vPhk5wB78sSm8QCfKuVgf1AOQC8JYm'
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic QUJ4QzNaUFZCMDBhOEtmYTdGQ3dzYmdjMlp3aUFyVzFFMkNuUWZZZmdPOGRrOU15cUI6dlFES1FwRzhZV2VONkZWdmRvNE5vRm95Y2JMMTZ3RXI0UWtBRU5oVw=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    js = json.loads(response.text).get('access_token')
    return js

