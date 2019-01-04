
import requests
import json

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)

    movie = req["queryResult"]["parameters"]["movie"]

    url = "http://www.omdbapi.com/?t="+movie+"&apikey=ba240db5"

    response = requests.get(url)

    result = response.json()

    print(result)

    try:

        title = result.get("Title")

        year = result.get("Year")

        actors = result.get("Actors")

        plot = result.get("Plot")

        rating = result.get("Ratings")[1].get("Source") + " " + result.get("Ratings")[1].get("Value")

        details = title + " (" + year + ") \nStarring: " + actors + "\nPlot: "+ plot + "\n" + rating
    
    except:

         details = "I could not get anything for "+movie        
    
    my_result =  {

    "fulfillmentText": details,
     "source": details
    }

    res = json.dumps(my_result, indent=4)

    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'

    return r

if __name__ == '__main__':
    
    app.run(port=5000,host='localhost')

