from flask import Flask, request, Response, jsonify
import json, datetime

app = Flask(__name__)

rates = [
    {
        "days": "mon,tues,thurs",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 1500
    },
    {
        "days": "fri,sat,sun",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 2000
    },
    {
        "days": "wed",
        "times": "0600-1800",
        "tz": "America/Chicago",
        "price": 1750
    },
    {
        "days": "mon,wed,sat",
        "times": "0100-0500",
        "tz": "America/Chicago",
        "price": 1000
    },
    {
        "days": "sun,tues",
        "times": "0100-0700",
        "tz": "America/Chicago",
        "price": 925
    }
]

@app.route("/rates", methods=['GET', 'PUT'])
def getRates():
    if request.method == 'GET':
        return jsonify(rates)
    if request.method == 'PUT':
        data = json.loads(request.data)
        timeFrame = data['times'].split('-')

        if timeFrame[1] < timeFrame[0]:
            return Response('Cannot add rates. Time ranges must exist within the same day.', 503)
        else:
            rates.append(data)
            return Response('Rate successfully added.', 200)

@app.route("/price")
def getPrices():
    return "some prices"


if __name__ == "__main__":
    app.run(debug=True)