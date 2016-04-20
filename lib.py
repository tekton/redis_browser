import base64
from simple_redis_conn import r
import json
# from simple_redis_conn import w
# connect to redis

# scan for all the things to create an in-memory DB of things

# go through all the keys and get their types

# for a key, check its type- don't have it? get it!
# # based on the type get the stuff...
# # if we can send the type, even better!

# /keys/:key(?type=<type>) && other information

# get hash
# ...try to convert all the things inside to json objects if possible


def recursive_redis_scan(scan_val, rtn_dict={}):
    print scan_val[0]
    if len(scan_val) > 1:
        for k in scan_val[1]:
            rtn_dict[base64.urlsafe_b64encode(k)] = k
    if scan_val[0] > 0:
        rtn_dict = recursive_redis_scan(r.scan(scan_val[0]), rtn_dict)
    return rtn_dict


def get_redis_keys():
    rtn_dict = recursive_redis_scan(r.scan())  # just send the first scan that goes on
    return json.dumps(rtn_dict)


def decode_key(key):
    key = base64.b64decode(key)
    return key


def get_redis_key_data(k, start=None, end=None):
    key = base64.b64decode(k)
    key_type = r.type(key)
    state_dict = {
        "hash": {"function": r.hgetall},
        "list": {"function": r.llen},
        "string": {"function": r.get},
        "set": {"function": r.smembers},
    }
    if key_type == "set":
        rtn_dict = {}
        rtn_dict["set_vals"] = list(state_dict[key_type]["function"](key))
    else:
        rtn_dict = state_dict[key_type]["function"](key)
    rtn_dict["redis_key"] = key
    return json.dumps(rtn_dict)
