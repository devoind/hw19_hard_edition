from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from service.decorators import *

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_requered
    def get(self):
        """
        Функция для запроса списка директоров

        :return: возвращает список директоров
        """
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @auth_requered
    @admin_requered
    def post(self):
        """
        Функция добавления директора

        :return: возвращает добавленного директора
        """
        req_json = request.json
        new_director = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{new_director.id}"}


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_requered
    def get(self, did):
        """
        Функция для запроса did-го директора

        :param did: получение  did директора
        :return: возвращает did-го директора
        """
        r = director_service.get_one(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_requered
    def put(self, did):
        """
        Функция для обновления did-го директора

        :param did:получение  did директора
        :return: возвращает обновленного did-го директора
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = did
        director_service.update(req_json)
        return "", 204

    @admin_requered
    def delete(self, did):
        """
        Функция для удаления did-го директора

        :param did:получение did директора
        :return: ничего не возвращает
        """
        director_service.delete(did)
        return "", 204
