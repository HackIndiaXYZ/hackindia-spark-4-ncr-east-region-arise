from flask import Flask, request, jsonify, render_template, send_file
from Extractor import process_folder
from Exporter import export_to_excel
import os
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    try:
        data = request.json
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid JSON request"
            }), 400
        
        folder_path = data.get("folder_path", "").strip()
        fields = data.get("fields", [])
        
        # Validation
        if not folder_path:
            return jsonify({
                "success": False,
                "error": "Folder path is required"
            }), 400
        
        if not isinstance(fields, list) or len(fields) == 0:
            return jsonify({
                "success": False,
                "error": "Please specify at least one field to extract"
            }), 400
        
        # Check folder exists
        if not os.path.isdir(folder_path):
            return jsonify({
                "success": False,
                "error": f"Folder not found: {folder_path}"
            }), 404
        
        # Count DOCX files
        docx_files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]
        if not docx_files:
            return jsonify({
                "success": False,
                "error": f"No .docx files found in {folder_path}"
            }), 400
        
        # Process extraction
        results = process_folder(folder_path, fields)
        
        # Calculate stats
        total = len(results)
        perfect = sum(1 for r in results if r.get("confidence", 0) == 1.0)
        partial = sum(1 for r in results if 0 < r.get("confidence", 0) < 1.0)
        failed = sum(1 for r in results if r.get("confidence", 0) == 0.0)
        
        return jsonify({
            "success": True,
            "data": results,
            "stats": {
                "total_files": total,
                "fully_extracted": perfect,
                "partially_extracted": partial,
                "extraction_failed": failed,
                "average_confidence": round(sum(r.get("confidence", 0) for r in results) / total, 2) if total > 0 else 0
            }
        }), 200
    
    except Exception as e:
        app.logger.error(f"Extraction error: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": f"Extraction failed: {str(e)}"
        }), 500

@app.route("/export", methods=["POST"])
def export():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON request"}), 400
        
        rows = data.get("data", [])
        fields = data.get("fields", [])
        
        if not rows:
            return jsonify({"error": "No data to export"}), 400
        if not fields:
            return jsonify({"error": "No fields specified"}), 400
        
        path = export_to_excel(rows, fields, output_path="output.xlsx")
        return send_file(path, as_attachment=True, download_name="extracted_data.xlsx"), 200
    
    except Exception as e:
        app.logger.error(f"Export error: {traceback.format_exc()}")
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)