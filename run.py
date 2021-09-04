import os
from flask import Flask, flash, request, redirect, url_for, render_template, make_response, send_from_directory
from werkzeug.utils import secure_filename


from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from api.services import daotao

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png',
                      'jpg', 'jpeg', 'gif', 'exe', 'zip', 'rar'}

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = ROOT_DIR + UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.2', title='VNU TOOL API',
          description='A simple connect daotao.vnu.edu.vn API by Huaan ^^',
          )

ns = api.namespace('crawler', description='CRAWLER operations')

model = api.model('Model', {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ns.route('/file', methods=['GET', 'POST'])
class UploadFile(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('upload.html'), 200, headers)

    def post(self):
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))


@ns.route('/uploads/<string:name>')
class DownloadFile(Resource):
    def get(self, name):
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@ns.route('/getGPA')
class Todo(Resource):

    def get(self, **kwargs):
        data = daotao.getGPAInfo()
        return data  # Some function that queries the db


if __name__ == "__main__":
    app.run(host="0.0.0.0")
