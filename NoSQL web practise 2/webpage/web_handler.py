from flask import Flask, render_template, url_for, request
import pymongo 
import json 
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/load', methods=["POST"])
def load():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    client.drop_database('myDatabase')
    db = client.get_database('myDatabase')

    with open('crimes.json') as f:
        data = json.load(f)
    
    client['myDatabase']['crimes'].insert_many(data)
    client.close()

    return render_template('home.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    Type = request.form['Type']

    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.get_database('myDatabase')
    coll = db.get_collection('crimes')

    query = {"records.type":Type}
    fields = {"_id":1, "accused":1, "age":1}

    if Type == "":
        result = coll.find()
    else:
        result = coll.find(query, fields)
    client.close()
    
    result_list = []

    for doc in result:
        temp = []
        temp += doc.values()
        result_list.append(temp)

    return render_template('display.html', result_list=result_list)
        

if __name__ == '__main__':
    app.run(debug=True)