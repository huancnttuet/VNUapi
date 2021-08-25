from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from api.utils.run import getGPAInfo


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


@ns.route('/getGPA')
class Todo(Resource):

    def get(self, **kwargs):
        data = getGPAInfo()
        return data  # Some function that queries the db


if __name__ == "__main__":
    app.run(host="0.0.0.0")
