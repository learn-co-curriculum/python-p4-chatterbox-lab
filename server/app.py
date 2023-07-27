from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Messages(Resource):
    def get(self):
        # message_list = []
        # messages_ordered = Message.query.order_by(Message.created_at).all()
        # for message in messages_ordered:
        #     message_dict = {
        #         "id": message.id,
        #         "body": message.body,
        #         "username": message.username,
        #         "created_at": message.created_at,
        #         "updated_at": message.updated_at
        #     }
        #     message_list.append(message_dict)
        message_dict_list = [m.to_dict() for m in Message.query.order_by(Message.created_at).all()]
        response = make_response(jsonify(message_dict_list), 200)
        return response

    def post(self):
        data = request.get_json()
        new_message = Message(
            body = data["body"],
            username = data["username"]
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(jsonify(message_dict), 201)
        return response

api.add_resource(Messages, '/messages')

class MessagesByID(Resource):
    def patch(self,id):
        message = Message.query.filter(Message.id == id).first()
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(jsonify(message_dict), 200)
        return response

    def delete(self,id):
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }
        response = make_response(jsonify(response_body), 200)
        return response

api.add_resource(MessagesByID, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
