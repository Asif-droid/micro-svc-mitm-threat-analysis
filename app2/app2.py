from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/compute")
def compute():
    return jsonify({"result": 42})  # dummy computation

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
