from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at).all()
        message_list = [message.to_dict() for message in messages]

        response = make_response(jsonify(message_list), 200)
        return response

    elif request.method == "POST":
        new_message = Message(
            body=request.json.get("body"),
            username=request.json.get("username"),
            # created_at=request.form.get("created_at"),
            # updated_at=request.form.get("updated_at"),
        )
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()
        response = make_response(new_message_dict, 200)
        return response


@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    selected_message = Message.query.filter(Message.id == id).first()

    if request.method == "GET":
        message = selected_message.to_dict()

        response = make_response((message), 200)
        return response

    elif request.method == "PATCH":
        for attr in request.json:
            setattr(selected_message, attr, request.json.get(attr))

        db.session.add(selected_message)
        db.session.commit()

        message_dict = selected_message.to_dict()

        response = make_response(jsonify(message_dict), 200)

        return response

    elif request.method == "DELETE":
        db.session.delete(selected_message)
        db.session.commit()

        response_body = {"delete_successful": True, "message": "Review deleted."}
        response = make_response(response_body, 200)

        return response


if __name__ == "__main__":
    app.run(port=5555)
