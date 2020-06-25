from flask import Flask
from pymongo import MongoClient
from flask import Flask, jsonify,request,make_response,render_template
from flask_cors import CORS, cross_origin
from bson import ObjectId




client = MongoClient()
client = MongoClient('mongodb://sp241930:100rabhh@ds139435.mlab.com:39435/cmc')
db = client['cmc']
marbles = db['marbles']
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/sample_data": {"origins": "http://localhost:port"}})
cors = CORS(app, resources={r"/search/<search_key>": {"origins": "http://localhost:port"}})


@app.route('/', methods = ['GET'])
def render_home():
    return render_template('index.html')


@app.route('/create_client_booking', methods = ['GET'])
def create_client_booking():
    return render_template('checkout.html')



@app.route('/product/<marble_id>', methods = ['GET'])
def render_product(marble_id):
    marble_oid = ObjectId(marble_id)
    marble_data = marbles.find_one({"_id":marble_oid})
    return render_template('product.html',marble_json = marble_data)



@app.route('/sample_data', methods = ['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_sample():
    result = marbles.aggregate([{'$sample':{ 'size':16}}])
    response = list()
    for e in result:
        e["_id"] = str(e["_id"])
        response.append(e)
    return jsonify(response)



@app.route('/search/<search_key>', methods = ['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def search(search_key):
    if request.method == 'GET':
        result = marbles.find({'$text':{'$search':search_key}})
        response = list()
        for e in result:
        	e["_id"] = str(e["_id"])
        	response.append(e)
        return jsonify(response)


if __name__ == '__main__':
    app.debug=True
    app.run(host="0.0.0.0")

