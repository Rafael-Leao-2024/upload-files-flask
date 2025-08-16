from flask import Blueprint, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask import current_app
import os



documentos_bp  = Blueprint('documentos', __name__, template_folder='templates')


ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@documentos_bp.route("/upload/<name>")
def download_file(name):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], name, as_attachment=True)


@documentos_bp.route('/download')
def download():
    # Lista todos os arquivos PDF no diretório de uploads
    files = []
    for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
        if filename.endswith('.pdf'):
            files.append(filename)
    return render_template('documentos/download.html', files=files)


@documentos_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('documentos.download'))
    return render_template("documentos/upload.html")