import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.secret_key = 'supersecretkey'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist('pdfs')
    if not files or all(f.filename == '' for f in files):
        return 'No PDF files selected.', 400

    merger = PdfMerger()
    valid = False

    for file in files:
        if file and allowed_file(file.filename):
            merger.append(file.stream)
            valid = True

    if not valid:
        return 'No valid PDF files uploaded.', 400

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.pdf')
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True, download_name='merged.pdf')

if __name__ == '__main__':
    app.run(debug=True)