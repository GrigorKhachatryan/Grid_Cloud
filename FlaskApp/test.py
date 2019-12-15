import requests
def numbercar(img_base64):
    SECRET_KEY = 'sk_3a6ba5f2a666745e0cd8df50'
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=rus&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data=img_base64)

    result_json = r.json()
    result = result_json['results'][0]['plate'] if result_json['results'] else 'i dont help you'
    return result
