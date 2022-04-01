from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.news import News
from data.users import User


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('created_date', required=True)
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'about', 'about', 'created_date'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'about', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
        )
        user.set_password(args["password"])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})