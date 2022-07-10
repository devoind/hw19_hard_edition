from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from service.decorators import *

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_requered
    def get(self):
        """
        Функция для запроса списка жанров

        :return: возвращает список жанров
        """
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_requered
    def post(self):
        """
        Функция добавления жанра

        :return: возвращает добавленный жанр
        """
        req_json = request.json
        new_genre = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{new_genre.id}"}


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_requered
    def get(self, gid):
        """
        Функция для запроса gid-го жанра

        :param gid: получение  gid жанра
        :return: возвращает gid-й жанр
        """
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_requered
    def put(self, gid):
        """
        Функция для обновления gid-го жанра

        :param gid:получение gid жанра
        :return: возвращает обновленный gid-й жанр
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = gid
        genre_service.update(req_json)
        return "", 204

    @admin_requered
    def delete(self, gid):
        """
        Функция для удаления gid-го жанра

        :param gid:получение gid жанра
        :return: ничего не возвращает
        """
        genre_service.delete(gid)
        return "", 204
