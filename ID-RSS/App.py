from flask import Flask, request, jsonify, render_template, send_file
from Extractor import process_folder
from Exporter import export_to_excel
import os
import traceback
import re
from docx import Document

app = Flask(__name__, template_folder='Templates')

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

@app.route("/view-docx", methods=["POST"])
def view_docx():
    try:
        data = request.json
        if not data:
            return "Invalid request", 400
        
        filename = data.get("filename", "").strip()
        highlight_values = data.get("highlight", [])
        
        # Find the file in demo_files
        demo_path = os.path.join("demo_files", filename)
        if not os.path.exists(demo_path):
            return f"<p style='color:red;'>File not found: {filename}</p>", 404
        
        file_ext = filename.lower().split('.')[-1]
        full_text = ""
        
        # Read based on file type - SHOW ALL CONTENT
        if file_ext == 'docx':
            doc = Document(demo_path)
            # Get ALL paragraphs, don't filter empty ones
            full_text = "\n".join([p.text for p in doc.paragraphs])
        elif file_ext == 'txt':
            with open(demo_path, 'r', encoding='utf-8') as f:
                full_text = f.read()
        else:
            return f"<p style='color:orange;'>Unsupported file type: .{file_ext}</p>", 400
        
        # If file is empty, show message
        if not full_text.strip():
            return "<p style='color:#999;font-style:italic;'>File is empty or contains no readable text</p>", 200
        
        # Escape HTML
        html_content = full_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # Highlight extracted values with case-insensitive matching
        for value in highlight_values:
            if value and value != "—":
                escaped_val = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                # Create highlight HTML with strong visual indicator
                highlight_html = f'<mark style="background:#FFF9E6;color:#B8840A;font-weight:700;padding:3px 5px;border-radius:3px;box-shadow:0 0 0 2px #B8840A;border:1px solid #B8840A;">{escaped_val}</mark>'
                # Replace all occurrences (case-insensitive)
                html_content = re.sub(
                    rf'{re.escape(escaped_val)}',
                    highlight_html,
                    html_content,
                    flags=re.IGNORECASE
                )
        
        # Convert to formatted HTML with line breaks and padding
        para_count = full_text.count('\n') + 1
        char_count = len(full_text)
        extracted_count = sum(1 for v in highlight_values if v and v != '—')
        
        # Build info box for file metadata
        info_box = f"""
        <div style="background:#E8F5EF;border-left:4px solid #1B6B53;padding:12px 16px;margin-bottom:20px;border-radius:4px;font-size:13px;color:#155E39;">
            <strong>📋 File Info:</strong> {para_count} section{'s' if para_count != 1 else ''} • {char_count} characters
            {f'<br><strong style="color:#B8840A;">✓ Extracted:</strong> {extracted_count} value(s) highlighted' if extracted_count > 0 else '<br><strong style="color:#999;">⚠️ No data extracted from this file</strong>'}
        </div>
        """
        
        html_output = f"""
        <div style="font-size:15px;line-height:1.8;color:#333;white-space:pre-wrap;word-wrap:break-word;font-family:'Segoe UI',Tahoma,sans-serif;">
            {info_box}
            <div style="padding:16px;background:white;border-radius:4px;border:1px solid #E2DAD0;">
                {html_content.replace(chr(10), '<br>')}
            </div>
        </div>
        """
        
        return html_output, 200
    
    except Exception as e:
        app.logger.error(f"Viewer error: {traceback.format_exc()}")
        return f"<p style='color:red;'>Error loading file: {str(e)}</p>", 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
