from flask import Flask

app = Flask(__name__)

@app.route("/rates")
def getRates():
    return "some rates"

if __name__ == "__main__":
    app.run()