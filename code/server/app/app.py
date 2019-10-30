#coding: utf-8

from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import json
app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return render_template('index.html')

class Customer_Profile(Resource):
    def get(self, customer_id):
        result = {}
        with open(str(customer_id)+'/config.json') as json_data:
            result = json.load(json_data)
        return jsonify(result)

api.add_resource(Customer_Profile, '/customer/<customer_id>') # Route_1

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')