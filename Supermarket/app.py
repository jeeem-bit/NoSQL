from flask import Flask, render_template, request, url_for
import pymongo

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        type = request.form['type']
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client.get_database('Supermarket')
        col = db.get_collection('supermarket')
        
        query = {"item_type":type}
        fields = {"_id":0, "item_name":1, "price":1, "discount_in_percent":1}

        result = col.find(query,fields)
        client.close()
        
        items = []
        for item in result:
            temp=[]
            temp += item.values()
            items.append(temp)

        return render_template('display.html', items=items)
    
if __name__ == '__main__':
    app.run(debug=False)
