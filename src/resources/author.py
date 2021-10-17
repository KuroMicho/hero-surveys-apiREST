from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import InternalError
from src.models import Survey, SurveySchema
from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND
# from werkzeug.utils import secure_filename

# SCHEMAS
survey_schema = SurveySchema()
surveys_schema = SurveySchema(many=True)

# TODAS LAS ENCUESTAS DEL USUARIO


class AuthorSurveysApi(Resource):
    @jwt_required()
    def get(self, author_id):

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        survey = Survey.query.filter_by(author_id=author_id)
        surveys = survey.paginate(page=page, per_page=per_page)

        if not surveys:
            return {
                "message": "Items not found"
            }, HTTP_404_NOT_FOUND

        data = []

        for survey in surveys.items:

            data.append({
                "id": survey.id,
                "title": survey.title,
                "image_name": survey.image_name,
                "image": survey.image,
                "mime_type": survey.mime_type,
                "short_url": survey.short_url,
                "url": survey.url,
                "visits": survey.visits,
                "date_created": survey.date_created,
                "date_updated": survey.date_updated,
                "author_id": survey.author_id,
                "sections": [
                    {
                        "id": section.id,
                        "header": section.header,
                        "survey_id": section.survey_id,
                        "questions": [
                            {
                                "id": question.id,
                                "question": question.question,
                                "date_created": question.date_created,
                                "questionType_id": {
                                    "id": question.question_type.id,
                                    "type": question.question_type.type
                                },
                                "section_id": question.section_id,
                                "answers": [{
                                    "id": answer.id,
                                    "answer": answer.answer,
                                    "date_created": answer.date_created,
                                    "question_id": answer.question_id
                                } for answer in question.answers
                                ],

                            } for question in section.questions
                        ],
                    } for section in survey.sections
                ],
            })

        meta = {
            "page": surveys.page,
            "pages": surveys.pages,
            "total_count": surveys.total,
            "prev_page": surveys.prev_num,
            "next_page": surveys.next_num,
            "has_prev": surveys.has_prev,
            "has_next": surveys.has_next
        }

        return make_response(jsonify({
            "data": data,
            "meta": meta
        }), HTTP_200_OK)

# VER ENCUESTA


class AuthorSurveyApi(Resource):
    @jwt_required()
    def get(self, author_id, survey_id):

        survey = Survey.query.filter_by(author_id=author_id, id=survey_id).first()

        if not survey:
            return {
                "error": "Item not found"
            }, HTTP_404_NOT_FOUND

        return make_response(jsonify({
            "id": survey.id,
            "title": survey.title,
            "image": survey.image,
            "url": survey.url,
            "date_created": survey.date_created,
            "date_updated": survey.date_updated,
            "author_id": survey.author_id,
            "sections": [
                {
                    "id": section.id,
                    "header": section.header,
                    "survey_id": section.survey_id,
                    "questions": [
                        {
                            "id": question.id,
                            "question": question.question,
                            "date_created": question.date_created,
                            "questionType_id": {
                                "id": question.question_type.id,
                                "type": question.question_type.type
                            },
                            "section_id": question.section_id,
                            "answer": [{
                                "id": answer.id,
                                "answer": answer.answer,
                                "date_created": answer.date_created,
                                "question_id": answer.question_id
                            } for answer in question.answers],
                        } for question in section.questions
                    ],
                } for section in survey.sections
            ],
        }), HTTP_200_OK)

# ESTADISTICAS DE LA ENCUESTA


class AuthorSurveyStatsApi(Resource):
    @jwt_required()
    def get(self, author_id, survey_id):
        item = Survey.query.filter_by(author_id=author_id, id=survey_id).first()

        if not item:
            return {
                "message": "Survey without data"
            }, HTTP_404_NOT_FOUND

        try:
            data = []
            sections = []
            questions = []
            answers = []
            for section in item.sections:
                sections.append([{
                    "id": section.id
                }])
                for question in section.questions:
                    questions.append([{
                        "id": question.id
                    }])
                    for answer in question.answers:
                        answers.append([{
                            "id": answer.id
                        }])

            data.append({
                "id": item.id,
                "url": item.url,
                "visits": item.visits,
                "sections_in_survey": len(sections),
                "questions_in_section": len(questions),
                "answers_in_question": len(answers),
                "author_id": item.author_id,
            })

            return make_response(jsonify({"data": data}), HTTP_200_OK)
        except Exception as e:
            raise InternalError
