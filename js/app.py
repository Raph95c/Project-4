from flask import Flask, request, jsonify
from flask_cors import CORS
import test_script

app = Flask(__name__)
CORS(app)

@app.route("/recommend_songs", methods=['POST'])
def recommend_songs():
    
    user_song = request.json['input']
    print(f"Received input: {user_song}") 

    output_data = test_script(user_song)
    print(f"Processed data: {output_data}")

    return output_data


if __name__ == '__main__':
    app.run()
