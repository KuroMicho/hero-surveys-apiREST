import os
from src.models.section import Section
from src.models.question import Question
from src.models.answer import Answer, AnswerSchema
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import redirect
from src import db
from src.models import Survey, SurveySchema
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND
# from werkzeug.utils import secure_filename

# SCHEMAS
survey_schema = SurveySchema()
surveys_schema = SurveySchema(many=True)

answer_schema = AnswerSchema()

# CRUD SURVEY


class CreateSurveyApi(Resource):
    @jwt_required()
    def post(self):
        current_author = get_jwt_identity()

        title = request.json.get("title", None)
        image = request.json.get("image", None)
        url = request.json.get("url", None)

        if not title:
            return {
                "msg": "Title is required"
            }, HTTP_400_BAD_REQUEST

        if not image:
            return {
                "msg": "Image is required"
            },

        # filename = secure_filename(image.filename)
        # mimetype = image.mimetype
        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://rest-surveys.herokuapp.com/s/")
        public_url = base_url + url

        q_url = Survey.query.filter_by(url=public_url).first()
        if (q_url):
            return {
                "msg": "Url is already taken"
            }

        survey = Survey(title=title, image=image,
                        url=public_url, author_id=current_author)
        survey.save_to_db()

        return {
            "status": "Success",
            "data": survey_schema.dump(survey)
        }, HTTP_201_CREATED


class SurveyApi(Resource):
    @jwt_required()
    def put(self, survey_id):
        survey = Survey.query.filter_by(id=survey_id).first()

        if not survey:
            return {
                "msg": "Item not found"
            }, HTTP_404_NOT_FOUND

        title = request.json.get('title')
        image = request.json.get('image')
        url = request.json.get('url')

        if not title:
            return {
                "msg": "Title is required"
            }, HTTP_400_BAD_REQUEST

        if not image:
            return {
                "msg": "Image is required"
            }, HTTP_400_BAD_REQUEST

        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://rest-surveys.herokuapp.com/s/")
        public_url = base_url + url

        q_url = Survey.query.filter_by(id=survey_id, url=public_url).first()
        if (q_url):
            return {
                "msg": "Url is already taken"
            }

        survey.title = title
        survey.image = image
        survey.url = public_url

        db.session.commit()

        return {
            "status": "Success",
            "data": survey_schema.dumps(survey)
        }, HTTP_200_OK

    @jwt_required()
    def delete(self, survey_id):

        try:
            survey = Survey.query.filter_by(id=survey_id).first()

            if not survey:
                return {
                    "msg": "Item not found"
                }, HTTP_404_NOT_FOUND

            db.session.delete(survey)
            db.session.commit()

            return {"msg": "Successfully deleted that survey"}, HTTP_200_OK
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status": "Fail",
                "msg": "Integrity error on deleting answer"
            }, HTTP_409_CONFLICT


# URL PUBLICA DE UNA ENCUESTA

class PublicUrlApi(Resource):
    @jwt_required(optional=True)
    def get(self, url):

        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://rest-surveys.herokuapp.com/s/")
        public_url = base_url + url

        survey = Survey.query.filter_by(url=public_url).first_or_404()
        if not survey:
            return {
                "error": "Item not found"
            }, HTTP_404_NOT_FOUND

        return make_response(jsonify({
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
                            "options": question.options,
                            "date_created": question.date_created,
                            "questionType_id": {
                                "id": question.question_type.id,
                                "type": question.question_type.type
                            },
                            "section_id": question.section_id,
                            # "answers": [{
                            #     "id": answer.id,
                            #     "answer": answer.answer,
                            #     "date_created": answer.date_created,
                            #     "question_id": answer.question_id
                            # } for answer in question.answers
                            # ],
                        } for question in section.questions
                    ],
                } for section in survey.sections
            ],
        }), HTTP_200_OK)

    @jwt_required(optional=True)
    def post(self, url):

        answer = request.json.get("answer", None)
        question_id = request.json.get("question_id", None)

        if not answer or not question_id:
            return {
                "msg": "Answer and question_id is required"
            }

        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://rest-surveys.herokuapp.com/s/")
        public_url = base_url + url

        survey = Survey.query.filter_by(url=public_url).first_or_404()

        if not survey:
            return {
                "msg": "Item not found"
            }, HTTP_404_NOT_FOUND

        q_question = Question.query.filter(Question.section_id ==
                                           Section.id, Section.survey_id == Survey.id, Survey.url == public_url).filter_by(id=question_id).first()

        m_answer = Answer(answer=answer, question_id=q_question.id)
        m_answer.save_to_db()

        return {
            "status": "Success",
            "data": answer_schema.dumps(m_answer)
        }, HTTP_200_OK


class PublicRedirectApi(Resource):
    def get(self, short_url):
        survey = Survey.query.filter_by(short_url=short_url).first_or_404()
        if survey:
            survey.visits = survey.visits+1
            db.session.commit()
            return redirect(survey.url)
