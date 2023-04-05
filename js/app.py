from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import test_script

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/KMeans.html")
def Kmeans():
    return render_template("KMeans.html")

@app.route("/modelpage.html", methods=["POST", "GET"])
def modelpage():
    return render_template("modelpage.html")

@app.route("/process_input", methods=['POST'])
def process_input():
    input_data = request.form['input']
    output_data = test_script.input_plus_hello(input_data)
    print(output_data)
    
    return render_template("/modelpage.html", results=output_data)

@app.route("/charts.html")
def charts():
    return render_template("charts.html")

@app.route("/sources.html")
def sources():
    return render_template("sources.html")


if __name__ == '__main__':
    app.run()

