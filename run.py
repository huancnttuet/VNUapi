from flask import Flask, request, abort, jsonify, send_from_directory
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from api.services import daotao
import os

app = Flask(__name__)
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


UPLOAD_DIRECTORY = "/project/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@ns.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@ns.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@ns.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


@ns.route('/getGPA')
class Todo(Resource):

    def get(self, **kwargs):
        data = daotao.getGPAInfo()
        return data  # Some function that queries the db


if __name__ == "__main__":
    app.run(host="0.0.0.0")
