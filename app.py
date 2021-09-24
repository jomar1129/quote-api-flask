import os
from flask import Flask , render_template , request ,json, url_for , Response
import random
from flask_cors import CORS
from data import quotes
app = Flask(__name__ , static_url_path='')
CORS(app)



## initial route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-quote')
def addQuote():
    return render_template('add-quote.html')


#getRandomElement
def getRandomElement():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "./", "data.json")
    data = json.load(open(json_url))


# get request
# route getting random quote
@app.route('/api/quotes/random' , methods= ['GET'])
def getQuotes():
    data = quotes
    ## get random quote
    randomData = random.choice(data)
    return json.jsonify(randomData)

# get quotest

@app.route('/api/quotes' , methods=['GET' , 'POST'])
def getAllQuotes():
    datas = quotes
    user = request.args.get('person')

    ## check if the method is using get or post
    if request.method == 'GET' :
        print("GET")
        # check if use params is empty then proceed on check 
        # if is included to the list
        if user:
            for data in datas:
                person = data["person"]
                if user.lower() in person.lower():
                    return json.jsonify(data)
        else:
            return json.jsonify(datas)
    elif request.method == 'POST':
        print("POST")
        person = request.args.get('person')
        quote = request.args.get('quote')
        data = quotes
        
        ## check if person and quote is empty
        if not person and not quote:
            return Response(status=400)
        else:
            newData = {"quote" : quote , "person" : person}
            data.append(newData)
            return json.jsonify(newData)


## port for heroku deployment
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port , debug=True)