from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from src import db
from src.models import Section, SectionSchema
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

# ESQUEMAS

section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

# CREAR SECCION


class CreateSectionApi(Resource):
    @jwt_required()
    def post(self, survey_id):

        header = request.json["header"]

        if not header:
            return {
                "message": "Header is required"
            }, HTTP_400_BAD_REQUEST

        section = Section(header=header, survey_id=survey_id)
        section.save_to_db()

        return {
            "status": "Success",
            "data": section_schema.dump(section)
        }, HTTP_201_CREATED


class SectionsApi(Resource):
    @jwt_required()
    def get(self, survey_id):

        sections = Section.query.filter_by(
            survey_id=survey_id).all()

        return {
            "status": "Success",
            "data": sections_schema.dump(sections),
        }, HTTP_200_OK


class SectionApi(Resource):
    @jwt_required()
    def put(self, survey_id, section_id):

        header = request.json["header"]

        # if not header:
        #     return {
        #         "msg": "Header is required"
        #     }, HTTP_400_BAD_REQUEST

        section = Section.query.filter_by(
            id=section_id, survey_id=survey_id).first()

        if not section:
            return {
                "msg": "Item not found"
            }, HTTP_404_NOT_FOUND

        try:

            section.header = header
            db.session.commit()

            return {
                "status": "Success",
                "data": section_schema.dump(section)
            }, HTTP_200_OK

        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg": "Integrity error on update section"
            }, HTTP_409_CONFLICT

    @jwt_required()
    def delete(self, survey_id, section_id):

        section = Section.query.filter_by(
            survey_id=survey_id, id=section_id).first()

        if not section:
            return {
                "msg": "Section not found"
            }, HTTP_404_NOT_FOUND

        try:

            db.session.delete(section)
            db.session.commit()

            return {
                "msg": "Successfully section deleted"
            }, HTTP_200_OK

        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg": "Integrity error on delete section"
            }, HTTP_409_CONFLICT
