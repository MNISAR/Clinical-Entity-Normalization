import os, sys
import requests, json
import lxml.html as lh
from lxml.html import fromstring
UMLS_API_KEY = "d5b6176c-5c39-474b-90c3-e26ceea67180"

def get_tgt(apikey=UMLS_API_KEY):
    params = {'apikey': apikey}
    h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
    r = requests.post("https://utslogin.nlm.nih.gov/cas/v1/api-key/",data=params,headers=h)
    response = fromstring(r.text)
    tgt = response.xpath('//form/@action')[0]
    return tgt

def get_st(tgt=get_tgt()):
    service="http://umlsks.nlm.nih.gov"
    params = {'service': service}
    h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
    r = requests.post(tgt, data=params, headers=h)
    if r.status_code == 403:
        tgt = get_tgt(UMLS_API_KEY)
        st = get_st(tgt)
    else:        
        st = r.text
    return st

def find_mention_in_UMLS_perfect_name(mention):
    st = get_st()
    version = "current"
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/search/"+version
    pageNumber = 0
    
    results = []
    while True:
        pageNumber += 1
        query = {'string':mention,'ticket':st, 'pageNumber':pageNumber, 'searchType': 'exact'}
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        if "result" not in items:
            break
        jsonData = items["result"]

        for result in jsonData["results"]:
            d = {}
            try:
                d['cui'] = result["ui"]
                d["name"] = result["name"]
            except:
                continue
            finally:
                results.append(d)
    return results

def find_mention_in_UMLS_partial_name(mention):
    st = get_st()
    version = "current"
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/search/"+version
    pageNumber = 0
    
    results = []
    while True:
        pageNumber += 1
        query = {'string':mention,'ticket':st, 'pageNumber':pageNumber}
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        if "result" not in items:
            break
        jsonData = items["result"]

        for result in jsonData["results"]:
            d = {}
            try:
                d['cui'] = result["ui"]
                d["name"] = result["name"]
            except:
                continue
            finally:
                results.append(d)
    return results