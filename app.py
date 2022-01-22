from flask import Flask, request, Response, jsonify
import json, datetime

def create_app():
    app = Flask(__name__)

    rates = json.load(open('rates.json'))['rates']
    def isActiveWeekday(weekday, rate):
        daysOfTheWeek = {
            'mon': 0,
            'tues': 1,
            'wed': 2,
            'thurs': 3,
            'fri': 4,
            'sat': 5,
            'sun': 6, 
        }
        for day in rate['days'].split(','):
            if daysOfTheWeek[day] == weekday:
                return True
        return False

    @app.route("/rates", methods=['GET', 'PUT'])
    def getRates():
        try:
            if request.method == 'GET':
                return jsonify(rates)
            elif request.method == 'PUT':
                data = json.loads(request.data)
                timeFrame = data['times'].split('-')
                if timeFrame[1] < timeFrame[0]:
                    return Response('unavailable', 503)
                else:
                    rates.append(data)
                    return Response('Rate successfully added.', 200)
        except:
            return Response('unavailable', 503)

    @app.route("/price", methods=['GET'])
    def getPrices():
        try:
            requestStart = datetime.datetime.fromisoformat(request.args['start'].replace(' ', '+'))
            requestEnd = datetime.datetime.fromisoformat(request.args['end'].replace(' ', '+'))
            if requestStart > requestEnd or not requestStart.date() == requestEnd.date():
                return Response('unavailable', 503)
            else:
                for rate in rates:
                    rateStart = datetime.datetime.strptime(rate['times'].split('-')[0], '%H%M')            
                    rateEnd = datetime.datetime.strptime(rate['times'].split('-')[1], '%H%M')
                    isWithinTimeFrame = requestStart.time() >= rateStart.time() and requestEnd.time() <= rateEnd.time()
                    if isWithinTimeFrame and isActiveWeekday(requestStart.weekday(), rate):
                        return jsonify({'price': rate['price']})
                raise Exception('No available rates')
        except:
            return Response('unavailable', 503)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run('0.0.0.0', debug=True)
