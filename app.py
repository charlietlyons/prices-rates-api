from flask import Flask, request, jsonify

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
        return "Rates PUT"

@app.route("/price")
def getPrices():
    return "some prices"


if __name__ == "__main__":
    app.run()