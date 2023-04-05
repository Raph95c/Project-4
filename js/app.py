from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spotipyxx

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

@app.route("/recommend_songs", methods=['POST'])
def process_input():
    input_data = request.form['input']
    recommended_songs = spotipyxx.recommend_songs(input_data)
    
    return render_template("/modelpage.html", results=recommended_songs)

@app.route("/charts.html")
def charts():
    return render_template("charts.html")

@app.route("/sources.html")
def sources():
    return render_template("sources.html")


if __name__ == '__main__':
    app.run()

