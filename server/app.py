from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.compact = False  # Corrected the attribute name

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "Hello"

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()  # Corrected the function call
    serialized_messages = [message.serialize() for message in messages]
    return jsonify(serialized_messages)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize())

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify(message.serialize())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully"})

if __name__ == '__main__':
    app.run(debug=False,port=5555)