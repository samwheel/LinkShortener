from redis import Redis
from flask import Flask, jsonify, request
from flask_cors import CORS

redis = Redis(decode_responses=True)
current_index: int = 0
if redis.exists('current_index'):
    current_index = int(redis.get('current_index')) # type: ignore
else:
    redis.set('current_index', 0)

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def home() -> str:
    return "Link Shortener API"

@app.get("/link")
def get_single_link():
    index = str(request.args.get('index'))
    return jsonify(redis.hget('links', index))

@app.get("/links")
def get_links():
    return jsonify(redis.hgetall('links'))

@app.post("/links")
def post_link():
    global current_index
    url = request.get_json().get('url')
    link_values = list(jsonify(redis.hgetall('links')).get_json().values())
    link_already_exists = link_values.count(url) > 0
    if not link_already_exists:
        print(f"Link does not exist.")
        redis.hset('links', hex(current_index), url)
        current_index = int(redis.incr('current_index')) # type: ignore
    return hex(current_index - 1)