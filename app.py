from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='VNU API',
    description='A simple connect daotao.vnu.edu.vn API',
)

ns = api.namespace('crawler', description='CRAWLER operations')

model = api.model('Model', {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
})

@ns.route('/todo')
class Todo(Resource):
    @ns.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return "hello"  # Some function that queries the db

