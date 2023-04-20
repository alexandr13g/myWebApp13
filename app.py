from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'host=oleksandr.postgres.database.azure.com port=5432 dbname=oleksandr user=oleksandr password=Gez041121 sslmode=require'
db = SQLAlchemy(app)

class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other columns

    def __init__(self, **kwargs):
        super(MyModel, self).__init__(**kwargs)

    def serialize(self):
        return {
            'id': self.id,
            "ім'я": "рядок",
            "опис": "рядок",
            "ціна": 0,
            " on _offer ": 'true'
        }
class MyModelResource(Resource):
    def get(self, id=None):
        if id:
            my_model = MyModel.query.get(id)
            if my_model:
                return jsonify(my_model.serialize())
            return {'message': 'Not found'}, 404
        else:
            my_models = MyModel.query.all()
            return jsonify([my_model.serialize() for my_model in my_models])

    def post(self):
        data = request.get_json()
        new_model = MyModel(**data)
        db.session.add(new_model)
        db.session.commit()
        return jsonify(new_model.serialize())

    def put(self, id):
        my_model = MyModel.query.get(id)
        if my_model:
            data = request.get_json()
            for key, value in data.items():
                setattr(my_model, key, value)
            db.session.commit()
            return jsonify(my_model.serialize())
        return {'message': 'Not found'}, 404

    def delete(self, id):
        my_model = MyModel.query.get(id)
        if my_model:
            db.session.delete(my_model)
            db.session.commit()
            return {'message': 'Deleted successfully'}
        return {'message': 'Not found'}, 404

api.add_resource(MyModelResource, '/api/my-model', '/api/my-model/<int:id>')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask app
