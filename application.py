import pymongo
from flask import Flask, jsonify, request, json, make_response
import xmltodict
import dict2xml

app = Flask(__name__)

conn = pymongo.MongoClient('mongodb://rahultalreja:rahulrahul@ds155132.mlab.com:55132/mydatabase')
db = conn.mydatabase


@app.route('/user', methods=['POST'])
def adduser():

    if request.headers['Content-Type'] == 'application/json':
        name = request.json['name']
        a = db.users.find_one({'name': name})
        output = {"message": "User Already Exists!"}
        if a:
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = dict2xml.dict2xml(output)
                return resp

        else:
            db.users.insert({'name': name})
            output = {"Message": "User Added Successfully!"}
            if request.headers['Accept'] == 'application/json':
                    resp = make_response(json.dumps(output))
                    return resp
            elif request.headers['Accept'] == 'application/xml':
                    resp = dict2xml.dict2xml(output)
                    return resp

    elif request.headers['Content-Type'] == 'application/xml':
        info = xmltodict.parse(request.data)
        a = db.users.find_one({'name': info['name']})
        output = {"message": "User Already Exists!"}
        if a:
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = dict2xml.dict2xml(output)
                return resp

        else:
            db.users.insert({'name': info['name']})
            output = {"Message": "User Added Successfully!"}
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = dict2xml.dict2xml(output)
                return resp


@app.route('/user/<name>', methods=['GET'])
def getuser(name):
    a = db.users.find_one({'name': name})
    if a:
        output = {'Status': 'User Found!'}, {'name': a['name']}
        if request.headers['Accept'] == 'application/json':
            resp = make_response(jsonify(output))
            return resp
        elif request.headers['Accept'] == 'application/xml':
            resp = make_response(dict2xml.dict2xml(output))
            return resp
    else:
        output = {'message': 'User not Found!'}
        if request.headers['Accept'] == 'application/json':
            resp = make_response(json.dumps(output))
            return resp

        elif request.headers['Accept'] == 'application/xml':
            resp = make_response(dict2xml.dict2xml(output))
            return resp


@app.route('/user/<name>', methods=['PUT'])
def updateuser(name):
    a = db.users.find_one({"name": name})
    if request.headers['Content-Type'] == 'application/json':
        if a:
            newname = request.json['name']
            db.users.update({}, {'name': newname})
            output = {'message': 'User Updated Successfully!'}
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = make_response(dict2xml.dict2xml(output))
                return resp

        else:
            output = {'message': 'User Not Found!'}
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = make_response(dict2xml.dict2xml(output))
                return resp

    elif request.headers['Content-Type'] == 'application/xml':
        if a:
            info = xmltodict.parse(request.data)
            db.users.update({"name": name}, {'name': info['name']})
            output = {'message': 'User Updated Successfully!'}
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = make_response(dict2xml.dict2xml(output))
                return resp
        else:
            output = {'message': 'User Not Found!'}
            if request.headers['Accept'] == 'application/json':
                resp = make_response(json.dumps(output))
                return resp
            elif request.headers['Accept'] == 'application/xml':
                resp = make_response(dict2xml.dict2xml(output))
                return resp


@app.route('/user/<name>', methods=['DELETE'])
def deleteuser(name):
    a = db.users.find_one({"name": name})
    if a:
        db.users.remove({'name': name})
        output = {'message': 'User Deleted Successfully!'}
        if request.headers['Accept'] == 'application/json':
            resp = make_response(json.dumps(output))
            return resp
        elif request.headers['Accept'] == 'application/xml':
            resp = make_response(dict2xml.dict2xml(output))
            return resp
    else:
        output = {'message': 'User Not Found!'}
        if request.headers['Accept'] == 'application/json':
            resp = make_response(json.dumps(output))
            return resp
        elif request.headers['Accept'] == 'application/xml':
            resp = make_response(dict2xml.dict2xml(output))
            return resp


if __name__ == '__main__':
    app.run(debug=True)
