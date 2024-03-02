from flask import Flask, render_template, url_for, request
import pymongo
import json
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template('search.html')

@app.route('/load', methods=["POST"])
def load():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    client.drop_database('myDatabase')
    db = client.get_database('myDatabase')
    with open('results.json') as f:
        data = json.load(f)
    client['myDatabase']['results'].insert_many(data)
    client.close()

    return render_template('search.html')


@app.route('/search', methods=["GET", "POST"])
def search():
    subject = request.form["subject"]
    
    client= pymongo.MongoClient("127.0.0.1", 27017)
    db = client.get_database("myDatabase")
    coll = db.get_collection("results")

    query = {"grades."+subject:{"$exists":True}}
    fields= {"_id":1, "name":1, "class":1}

    if subject == "":
        result = coll.find()
    else:
        result = coll.find(query, fields)

    print(result)
    client.close()
    result_list = []
    for doc in result:
        temp =[]
        temp += doc.values()
        result_list.append(temp)
    # print(result_list)
    return render_template('display.html', result_list=result_list)

@app.route('/docsearch', methods=["GET", "POST"])
def docsearch():
    f1, f1_con, f2, f2_con, f3, f3_con = \
    request.form["f1"], request.form["f1_con"], \
    request.form["f2"], request.form["f2_con"], \
    request.form["f3"], request.form["f3_con"]

    conditions = [f1, f1_con, f2, f2_con, f3, f3_con]
    query_list =[]

    # creates the list for the $and query later
    while len(conditions) > 1:
        if conditions[0] == "":
            conditions = conditions[2:] 
        else:
            if conditions[0] == "_id":
                temp = {conditions[0]: int(conditions[1])}
            else:
                temp = {conditions[0]: conditions[1]}

            query_list.append(temp)
            conditions = conditions[2:]
        
    

    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client.get_database('myDatabase')
    col = db.get_collection('results')
    results = col.find({"$and":query_list})
    client.close()
    result_list=[]

    #sorting the results 
    for doc in results:
        subjects = ["EL", "CL", "Math", "Phy", "Bio", "Chem"]
        key = list(doc["grades"].keys())
        value = list(doc["grades"].values())
        temp = [doc["_id"], doc["name"], doc["class"]]
        print(key)
        print(value)

        for i in subjects:
            if i in key:
                temp += value[0]
                value = value[1:]
            else: 
                temp += "-"

        result_list.append(temp)

    print(result_list)
    return render_template('docdisplay.html', result_list=result_list)

if __name__ == '__main__':
    app.run()
