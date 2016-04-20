import lib
from flask import Flask, jsonify  # , request
app = Flask(__name__)


@app.route('/key/<key>')
def get_key(key):
    pipe = lib.r.pipeline()
    pipe.object("IDLETIME", key)
    pipe.object("REFCOUNT", key)
    pipe.object("ENCODING", key)
    pipe.type(key)
    # pipe.get(key)
    res = pipe.execute()

    if res[3] == "string":
        val = lib.r.get(key)
    elif res[3] == "set":
        val = list(lib.r.smembers(key))

    rtn_dict = {
        "type": res[3],
        "val": val,
        "REFCOUNT": res[1],
        "ENCODING": res[2],
        "IDLETIME": res[0]
    }

    return jsonify(data=rtn_dict)


@app.route('/key64/<key>')
def get_key_64(key):
    key = lib.decode_key(key)
    pipe = lib.r.pipeline()
    pipe.object("IDLETIME", key)
    pipe.object("REFCOUNT", key)
    pipe.object("ENCODING", key)
    pipe.type(key)
    # pipe.get(key)
    res = pipe.execute()

    if res[3] == "string":
        val = lib.r.get(key)
    elif res[3] == "set":
        val = list(lib.r.smembers(key))
    elif res[3] == "hash":
        val = lib.r.hgetall(key)
    else:
        val = None

    rtn_dict = {
        "type": res[3],
        "val": val,
        "REFCOUNT": res[1],
        "ENCODING": res[2],
        "IDLETIME": res[0]
    }

    return jsonify(data=rtn_dict)


@app.route("/keys")
def get_keys():
    keys = lib.get_redis_keys()
    return jsonify(keys=keys)


if __name__ == '__main__':
    app.debug = True
    app.run()
