from flask import Flask, request, jsonify, render_template, send_file
from Extractor import process_folder
from Exporter import export_to_excel, export_to_csv, export_to_google_sheets

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

@app.route("/export_csv", methods=["POST"])
def export_csv():
    """Export extracted data to CSV format for Google Sheets."""
    data = request.json
    rows = data.get("data", [])
    fields = data.get("fields", [])
    path = export_to_csv(rows, fields, output_path="sheets_export.csv")
    if path:
        return send_file(path, as_attachment=True, download_name="extracted_data.csv", mimetype="text/csv")
    return jsonify({"error": "Failed to create CSV"}), 500

@app.route("/export_sheets", methods=["POST"])
def export_sheets():
    """Prepare data for Google Sheets import and return CSV blob."""
    data = request.json
    rows = data.get("data", [])
    fields = data.get("fields", [])

    csv_path = export_to_google_sheets(rows, fields)

    if csv_path:
        # Return the CSV file for download
        return send_file(csv_path, as_attachment=True, download_name="extracted_data.csv", mimetype="text/csv")

    return jsonify({"error": "Failed to create Google Sheets export"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)