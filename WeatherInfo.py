from urllib import request
import json


def weather_info():
    api_url = "http://api.jisuapi.com/weather/query?appkey=d73ccd5de0a06acd&citycode=101190101"

    with request.urlopen(api_url) as f:
        data = f.read()
        decode_data = data.decode('utf-8')
        return json.loads(decode_data)
