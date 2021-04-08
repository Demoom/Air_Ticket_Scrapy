from bs4 import BeautifulSoup
import requests
import csv
import json
import re
import random
import pandas as pd
import os
import datetime
import numpy as np

def GetUserAgent():
    userAgent = ["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
             "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"]
    _cookie = '_RF1=112.10.210.14; _RSG=PiaSAx3GPXDcbcX60rYBp8; _RDG=28b719f5eb3eb7213c1cb76be71f61a741; _RGUID=d859403e-ca72-4b19-8ccb-8b5006866966; _ga=GA1.2.492188649.1615812936; _gid=GA1.2.1338698748.1615812936; Session=smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4899&SID=135371&OUID=&createtime=1615812937&Expires=1616417736526; MKT_Pagesource=PC; appFloatCnt=1; MKT_CKID=1615812936834.55n6s.54o4; _abtest_userid=39c8b6c3-8b6a-483d-acc4-9b4156e758e6; MKT_CKID_LMT=1615949946521; ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; Customer=HAL=ctrip_cn; _ctm_t=ctrip; ibu_wws_c=1618542340930%7Czh-cn; FD_SearchHistorty={"type":"S","data":"S%24%u676D%u5DDE%28HGH%29%24HGH%242021-03-20%24%u6D77%u53E3%28HAK%29%24HAK%24%24%24"}; GUID=09031112112497482302; nfes_isSupportWebP=1; FlightIntl=Search=[%22HGH|%E6%9D%AD%E5%B7%9E(HGH)|17|HGH|480%22%2C%22HAK|%E6%B5%B7%E5%8F%A3(HAK)|42|HAK|480%22%2C%222021-03-20%22]; _jzqco=%7C%7C%7C%7C1615949947112%7C1.590642836.1615812936813.1615951914506.1615952268271.1615951914506.1615952268271.undefined.0.0.41.41; __zpspc=9.4.1615949946.1615952268.27%233%7Cwww.google.com%7C%7C%7C%7C%23; _bfa=1.1615812933239.1b1zhn.1.1615885718010.1615949943036.4.46; _bfi=p1%3D600001375%26p2%3D600001375%26v1%3D46%26v2%3D45'
    
    _headers = {}
    _headers.update({"User-Agent": userAgent[random.randint(0,8)]})
    _headers.update({"Cookie": _cookie})
    _headers.update({'accept': 'application/json',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'referer': 'https://flights.ctrip.com/international/search/oneway-hgh-hak?depdate=2021-03-20&cabin=Y_S_C_F',
                    'scope': 'd', # 一定要有
                    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"', # 一定要有
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin'})
    return _headers

def Get_Query_String_Parameters(origin, destination, v):
    Query_String_Parameters = {'departCityCode': str.upper(origin),
                            'arrivalCityCode': str.upper(destination),
                            'cabin': 'Y_S_C_F',
                            'v': v}
    return Query_String_Parameters

def CreateDir(originlist, destinationlist):
    for i in originlist:
        for j in destinationlist:
            origin = i
            destination = j
            if not os.path.exists('./%s2%s' %(origin, destination)):
                os.makedirs('./%s2%s' %(origin, destination))

def main():
    originlist = ['hgh', 'sha']
    destinationlist = ['syx', 'ctu', 'ckg', 'bjs']
    check4oneday = [False]*24
    CreateDir(originlist, destinationlist)
    
    while True:
        checktime = (datetime.datetime.utcnow() + datetime.timedelta(hours = 8)).strftime("%Y-%m-%d %H:%M:%S")
        checkhour = (datetime.datetime.utcnow() + datetime.timedelta(hours = 8)).hour
        checkdate = checktime.split()[0]
        if not check4oneday[checkhour]:
            # 状态重置
            if checkhour == 0:
                check4oneday = [False]*24
            for i in originlist:
                for j in destinationlist:
                    origin = i
                    destination = j
                    v = str(random.random())
                    _headers = GetUserAgent()
                    Query_String_Parameters = Get_Query_String_Parameters(origin, destination, v)
                    lowPriceurl = 'https://flights.ctrip.com/international/search/api/lowprice/calendar/getOwCalendarPrices?departCityCode=' + str.upper(origin) + '&arrivalCityCode=' + str.upper(destination) + '&cabin=Y_S_C_F&v=' + v
                    lowPriceResponse = requests.get(lowPriceurl, headers = _headers, data = json.dumps(Query_String_Parameters))
                    newlowPriceData = pd.DataFrame(json.loads(lowPriceResponse.text)['data'], index = [0]).T
                    newlowPriceData.sort_index(inplace = True)
                    newlowPriceData.columns = ['Price_%s' %(checktime)]
                    if os.path.exists('./%s2%s/lowPrice90Days%s.csv' %(origin, destination, checkdate)):
                        lowPriceData = pd.read_csv('./%s2%s/lowPrice90Days%s.csv' %(origin, destination, checkdate), index_col = 0)
                        pd.concat([lowPriceData, newlowPriceData], axis=1, sort=False).to_csv('./%s2%s/lowPrice90Days%s.csv' %(origin, destination, checkdate))
                    else:
                        newlowPriceData.to_csv('./%s2%s/lowPrice90Days%s.csv' %(origin, destination, checkdate))
            check4oneday[checkhour] = True

if __name__ == "__main__":
    main()