from flask import Blueprint, request, jsonify
from dataset_loader import load_pdf, load_word
from summarizer import summarize_text

routes = Blueprint('routes', __name__)

@routes.route('/summarize/pdf', methods=['POST'])
def summarize_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Extract text from the uploaded PDF file
        text = load_pdf(file)
        summary = summarize_text(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/summarize/word', methods=['POST'])
def summarize_word():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Extract text from the uploaded Word file
        text = load_word(file)
        summary = summarize_text(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
