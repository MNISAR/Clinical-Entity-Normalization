import os, sys
import requests, json
import lxml.html as lh
from lxml.html import fromstring

import json
with open("credentials.json") as f:
    credentials = json.load(f)
UMLS_API_KEY = credentials["UMLS_API_KEY"] # put your UMLS key

def get_tgt(apikey=UMLS_API_KEY):
    """
    given the UMLS key, this method will generate a TGT (Ticket Granting Ticket) which will be used in next step to get a ST (Something tiket).
    The ST will be used to call UMLS API to get information. The TGT expires in 8 hours.

    return: a str url that can be directly used for generating ST
    """
    params = {'apikey': apikey}
    h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
    r = requests.post("https://utslogin.nlm.nih.gov/cas/v1/api-key/",data=params,headers=h)
    response = fromstring(r.text)
    tgt = response.xpath('//form/@action')[0]
    return tgt

def get_st(tgt=get_tgt()):
    """
    This method will use a given TGT, to generate a ST. Automatically generate new TGT if the provided one is expired.

    return: str (just the ST)
    """
    service="http://umlsks.nlm.nih.gov"
    params = {'service': service}
    h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
    r = requests.post(tgt, data=params, headers=h)
    if r.status_code == 403 or r.text=='':
        tgt = get_tgt(UMLS_API_KEY)
        st = get_st(tgt)
    else:        
        st = r.text
    return st

def find_mention_in_UMLS_perfect_name(mention, st = get_st()):
    """
    This method will call the UMLS and search for mention using perfect search and return a list of dictionaries with mention and corresponding CUI

    return: list of dict({mention, CUI})
    """
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

def find_mention_in_UMLS_partial_name(mention, st = get_st()):
    """
    Similar to above method, but the result include partial mane matches as well.

    return: list of dict({mention, CUI})
    """
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