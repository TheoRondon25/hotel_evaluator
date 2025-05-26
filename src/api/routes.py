from flask import Flask, request, jsonify, render_template
from src.analysis.evaluator import HotelEvaluator
import os

# Configura o caminho correto para os templates
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
evaluator = HotelEvaluator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        data = request.get_json()
        if not data or 'comment' not in data:
            return jsonify({"error": "Comentário não fornecido"}), 400
            
        comment = data.get('comment', '').strip()
        if not comment:
            return jsonify({"error": "O comentário não pode estar vazio"}), 400
            
        result = evaluator.evaluate_comment(comment)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500