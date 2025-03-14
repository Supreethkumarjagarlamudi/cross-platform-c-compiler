import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Enable CORS for React frontend
from compiler import compile_c_to_binary

app = Flask(__name__)
CORS(app)  # Allow requests from the React frontend

@app.route("/compile", methods=["POST"])
def compile():
    # Ensure file is uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Create necessary directories
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Save uploaded C file
    input_file = os.path.join(uploads_dir, file.filename)
    file.save(input_file)

    # Compile the C file
    target_arch = request.form.get("arch", "aarch64")  # Default to aarch64
    output_binary = os.path.join(output_dir, f"{file.filename}.out")

    try:
        # Capture logs from the compilation process
        output_file, logs = compile_c_to_binary(input_file, output_binary, target_arch)
        return jsonify({
            "success": True,
            "logs": logs,
            "download_url": f"/download/{os.path.basename(output_file)}"
        })
    except Exception as e:
        return jsonify({"success": False, "logs": str(e)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    output_dir = os.path.join(os.getcwd(), "output")
    output_file = os.path.join(output_dir, filename)
    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)