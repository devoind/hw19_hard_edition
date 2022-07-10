from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        """
        Функция для запроса списка пользователей

        :return: возвращает список пользователей
        """
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        """
        Функция добавления пользователя

        :return: возвращает добавленного пользователя
        """
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        """
        Функция для запроса uid-го пользователя
        :param uid: получение uid-го пользователя
        :return: возвращает uid-го пользователя
        """
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def put(self, uid):
        """
        Функция для обновления uid-го пользователя

        :param uid:получение uid-го пользователя
        :return: возвращает обновленного uid-го пользователя
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    def delete(self, uid):
        """
        Функция для удаления uid-го пользователя

        :param uid:получение uid-го пользователя
        return: ничего не возвращает
        """
        user_service.delete(uid)
        return "", 204
