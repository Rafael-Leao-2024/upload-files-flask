from flask import Blueprint, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask import current_app
import os


documentos_bp  = Blueprint('documentos', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

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
        if 'file' not in request.files:
            flash('Selecione um arquivos', category='info')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Selecione um arquivos', category='info')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('documentos.download'))
    return render_template("documentos/upload.html")

@documentos_bp.route('/upload-ajax', methods=['GET', 'POST'])
def upload_ajax():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Selecione um ou mais arquivos', category='info')
            return redirect(url_for('documentos.upload_ajax'))        
        files = request.files.getlist('file')
        if files[0].filename == '':
            flash('Selecione um ou mais arquivos', category='info')
            return redirect(request.url)   
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        flash(message="arquivos armazenados com sucesso", category='success')
        return redirect(url_for('documentos.download'))           
    return render_template('documentos/muitos_file.html')