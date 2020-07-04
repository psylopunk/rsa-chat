from flask import Flask, request
import json
import sys

config = {
    "PORT": "9200"
}

arg_name = False
for argument in sys.argv[1:]:
    if "-" in argument:
        arg_name = argument.split("-")[-1]
        continue
    if arg_name == "p":
        config["PORT"] = argument
    arg_name = False

app = Flask(__name__)
boxes = {}

@app.route("/status", methods=["GET", "POST"])
def fid_status():
    return json.dumps({"success": True, "message": "All systems operational", "err": ""})

@app.route("/join", methods=["POST"])
def fid_join():
    data = request.get_json()


@app.errorhandler(404)
def fid_404(e):
    return json.dumps({"success": False, "message": "Method not found", "err": ""}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config["PORT"])
    print("Server started")
