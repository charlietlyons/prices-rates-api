from time import perf_counter, time
from flask import jsonify, Flask, request, Response, render_template, g as context
import json, datetime

def create_app():
    app = Flask(__name__)

    rates = json.load(open('rates.json'))['rates']
    metrics = [
        {
            "endpoint": '/rates',
            "avg_ms": 0.0,
            "calls": 0
        },
        {
            "endpoint": '/price',
            "avg_ms": 0.0,
            "calls": 0
        }
    ]

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

    @app.before_request
    def before_request():
        context.start = perf_counter()

    @app.after_request
    def after_request(response):
        total_time = perf_counter() - context.start

        for metricsInfo in metrics:
            if request.path == metricsInfo['endpoint']:
                metricsInfo['avg_ms'] = round((metricsInfo['avg_ms'] + (total_time*1000))/2, 4)
                metricsInfo['calls'] = metricsInfo['calls'] + 1

        return response

    @app.route('/docs')
    def getSwagger():
        return render_template('swaggerui.html')

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

    @app.route("/metrics/<endpoint>", methods=["GET"])
    def getMetrics(endpoint):
        if endpoint == 'rates':
            return jsonify(metrics[0])
        if endpoint == 'price':
            return jsonify(metrics[1])
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run('0.0.0.0', debug=True)
