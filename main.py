import json
from google.cloud import firestore
import datetime as dt
import requests
import pytz
import pandas as pd
from pandas.io.json import json_normalize

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def formatter(response, timestamp):
    if (response.status_code == 200) :
        req = flatten_json(json.loads(response.content))
        req["timestamp"] = timestamp
        
    else:
        req = None
    return(req)

def collector(event, context):
    # This function doesnt need to know what to do at the moment.
    # in future I may try and extend is to do different things, but for now it has 1 simple role

    # kraken = "https://api.kraken.com/0/public/Ticker?pair=xbteur"
    # luno = "https://api.mybitx.com/api/1/ticker?pair=XBTZAR"

    kraken = "https://api.cryptowat.ch/markets/kraken/btceur/summary"
    luno = "https://api.cryptowat.ch/markets/luno/btczar/summary"
    exch = "https://api.exchangeratesapi.io/latest?base=ZAR"

    timestamp = dt.datetime.now(pytz.utc)
    resp_exch = requests.get(exch)
    resp_luno = requests.get(luno)
    resp_kraken = requests.get(kraken)

    ex_rate = json.loads(resp_exch.content)["rates"]
    ex_rate["timestamp"] = timestamp

    json_luno = formatter(resp_luno, timestamp)
    json_kraken = formatter(resp_kraken, timestamp)

    db = firestore.Client()
    db.collection(u'kraken').document(str(int(timestamp.timestamp()))).set(json_kraken, merge=True)
    db.collection(u'luno').document(str(int(timestamp.timestamp()))).set(json_luno, merge=True)
    db.collection(u'rates').document(str(int(timestamp.timestamp()))).set(ex_rate, merge=True)

    # If you start using luno api: to match kraken
    # stemp = json.loads(resp_luno.content)
    # dat = {}
    # dat["ask_price"] = float(stemp["ask"])
    # dat["ask_whole_lot_vol"] = None
    # dat["ask_lot_vol"] = None

    # dat["bid_price"] = float(stemp["bid"])
    # dat["bid_whole_lot_vol"] = None
    # dat["bid_lot_vol"] = None

    # dat["close_price"] = float(stemp["last_trade"])
    # dat["close_lot_vol"] = None

    # dat["vol_today"] = None
    # dat["vol_last24"] = float(stemp["rolling_24_hour_volume"])

    # dat["vol_weighted_ave_price_today"] = None
    # dat["vol_weighted_ave_price_last24"] = None

    # dat["n_trades_today"] = None
    # dat["n_trades_last24"] = None

    # dat["l_today"] = None
    # dat["l_last24"] = None

    # dat["h_today"] = None
    # dat["h_last24"] = None

    # dat["opening_price_today"] = None


    # # kraken
    # stemp = json.loads(resp_kraken.content)["result"]["XXBTZEUR"]
    # dat = {}
    # dat["ask_price"] = float(stemp["a"][0])
    # dat["ask_whole_lot_vol"] = float(stemp["a"][1])
    # dat["ask_lot_vol"] = float(stemp["a"][2])

    # dat["bid_price"] = float(stemp["b"][0])
    # dat["bid_whole_lot_vol"] = float(stemp["b"][1])
    # dat["bid_lot_vol"] = float(stemp["b"][2])

    # dat["close_price"] = float(stemp["c"][0])
    # dat["close_lot_vol"] = float(stemp["c"][1])

    # dat["vol_today"] = float(stemp["v"][0])
    # dat["vol_last24"] = float(stemp["v"][0])

    # dat["vol_weighted_ave_price_today"] = float(stemp["p"][0])
    # dat["vol_weighted_ave_price_last24"] = float(stemp["p"][0])

    # dat["n_trades_today"] = float(stemp["t"][0])
    # dat["n_trades_last24"] = float(stemp["t"][0])

    # dat["l_today"] = float(stemp["l"][0])
    # dat["l_last24"] = float(stemp["l"][0])

    # dat["h_today"] = float(stemp["h"][0])
    # dat["h_last24"] = float(stemp["h"][0])

    # dat["opening_price_today"] = float(stemp["o"][0])



    # push to BQ
    # if pdf is not None:
    #     client = bigquery.Client()
    #     dataset_ref = client.dataset("exchange_data")
    #     table_ref = dataset_ref.table("exchange_data")

    #     job = client.load_table_from_dataframe(pdf, table_ref, location="US")

    #     job.result()  # Waits for table load to complete.

    #     assert job.state == "DONE"


    return("success")