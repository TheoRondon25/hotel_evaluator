from flask import Flask , request , jsonify
from src.analysis.evaluator import HotelEvaluator

app = Flask(__name__)
evaluator = HotelEvaluator()

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    comment = data.get('comment', '')
    result = evaluator.evaluete_comment(comment)
    return jsonify(result)