from flask import Flask, request, jsonify
import test_script

app = Flask(__name__)

@app.route("/recommend_songs", methods=['POST'])
def recommend_songs():
    user_song = request.json['input']
    output_data = test_script(user_song)

    return output_data
