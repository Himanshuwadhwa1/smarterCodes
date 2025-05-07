from flask import Flask,request, jsonify
from urllib.parse import urlparse
from flask_cors import CORS
from search import search
app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "http://localhost:3000"}})

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False

@app.route("/search", methods=["POST"])
def searchQuery():
    data = request.get_json()
    query = data.get("query")
    website = data.get("website")
    print(f"website link : {website}")
    print(f"query : {query}")
    # if not is_valid_url(website):
    #     return jsonify({"error": "Invalid URL provided."}), 400
    
    try:
        result,time = search(website,query)
    except Exception as e:
        return jsonify({"error": f"Something happened: {str(e)}"}), 500
    response = {
        "results": result,
        "time": time
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True,port=4000)