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


@app.route("/charts.html")
def charts():
    return render_template("charts.html")

@app.route("/sources.html")
def sources():
    return render_template("sources.html")


# @app.route("/recommend_songs", methods=['POST'])
# def recommend_songs():
    
#     user_song = request.json['input']
#     print(f"Received input: {user_song}") 

#     output_data = test_script(user_song)
#     print(f"Processed data: {output_data}")

#     return output_data


if __name__ == '__main__':
    app.run()

