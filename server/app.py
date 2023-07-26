from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import API, Resource

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

app=API(app)

@app.route('/messages')
def messages():
    message_list = []
    messages_ordered = Message.query.order_by(Message.created_at).all()

    for message in messages_ordered:
        message_dict = {
            "id": message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at,
            "updated_at": message.updated_at
        }
        message_list.append(message_dict)
    
    response = make_response(message_list, 200)

    return response

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
