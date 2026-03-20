from flask import Flask, request, jsonify, render_template, send_file
from extractor import process_folder
from exporter import export_to_excel

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    data = request.json
    folder_path = data.get("folder_path", "").strip()
    fields = data.get("fields", [])
    if not folder_path:
        return jsonify({"error": "No folder path"}), 400
    if not fields:
        return jsonify({"error": "No fields"}), 400
    results = process_folder(folder_path, fields)
    return jsonify(results)

@app.route("/export", methods=["POST"])
def export():
    data = request.json
    rows = data.get("data", [])
    fields = data.get("fields", [])
    path = export_to_excel(rows, fields, output_path="output.xlsx")
    return send_file(path, as_attachment=True, download_name="extracted_data.xlsx")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)