from src.models.section import Section
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from src import db
from src.models import Question, QuestionSchema
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

# ESQUEMAS

question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

# CREAR PREGUNTAS O TRAER TODAS LAS PREGUNTAS


class CreateQuestionApi(Resource):
    @jwt_required()
    def post(self, survey_id, section_id):

        q_section = Section.query.filter_by(
            survey_id=survey_id, id=section_id).first()

        if q_section is not None:

            question = request.json.get("question", None)
            questionType_id = int(request.json.get("questionType_id", None))
            options = request.json.get("options", None)

            if questionType_id == 3 or questionType_id == 2:
                if not options:
                    return {
                        "msg": "Options are required"
                    }, HTTP_400_BAD_REQUEST

            if not question or not questionType_id:
                return {
                    "msg": "Question, type question and is required"
                }, HTTP_400_BAD_REQUEST

            try:
                m_question = Question(question=question,
                                      questionType_id=questionType_id, options=options, section_id=section_id)
                m_question.save_to_db()

                return {
                    "status": "Success",
                    "data": question_schema.dump(m_question)
                }, HTTP_201_CREATED
            except IntegrityError as e:
                db.session.rollback()
                return {
                    "status": "Error",
                    "msg": "Error on creating question",
                }, HTTP_409_CONFLICT
        else:
            return {
                "status": "Fail",
                "msg": "Resource not found"
            }, HTTP_404_NOT_FOUND


class QuestionsApi(Resource):
    @jwt_required()
    def get(self, survey_id, section_id):

        q_section = Section.query.filter_by(
            survey_id=survey_id, id=section_id).first()

        if q_section is not None:

            questions = Question.query.filter_by(section_id=q_section.id).all()

            if len(questions) == 0:
                return {
                    "msg": "Questions not found"
                }, HTTP_404_NOT_FOUND

            return {"status": "Success", "data": questions_schema.dump(questions)}
        else:
            return {
                "status": "Fail",
                "msg": "Resource not found"
            }


class QuestionApi(Resource):
    @jwt_required()
    def put(self, survey_id, section_id, question_id):

        q_section = Section.query.filter_by(
            survey_id=survey_id, id=section_id).first()

        if q_section is not None:
            try:
                question = request.json.get("question", None)
                questionType_id = int(
                    request.json.get("questionType_id", None))
                options = request.json.get("options", None)

                q_question = Question.query.filter_by(
                    id=question_id, section_id=q_section.id).first()

                if not q_question:
                    return {
                        "message": "Item not found"
                    }, HTTP_404_NOT_FOUND

                if questionType_id == 3 or questionType_id == 2:
                    if not options:
                        return {
                            "message": "Options are required"
                        }, HTTP_400_BAD_REQUEST
                    else:
                        q_question.options = options
                else:
                    q_question.options = False

                q_question.question = question
                q_question.questionType_id = questionType_id
                db.session.commit()

                return {"status": "Success", "data": question_schema.dump(q_question)}, HTTP_200_OK

            except IntegrityError as e:
                db.session.rollback()
                return {
                    "status": "Error",
                    "msg": "Integrity error on updating question"
                }, HTTP_409_CONFLICT
        else:
            return {
                "status": "Fail",
                "msg": "Resource not found"
            }, HTTP_404_NOT_FOUND

    @jwt_required()
    def delete(self, survey_id, section_id, question_id):

        q_section = Section.query.filter_by(
            survey_id=survey_id, id=section_id).first()

        if q_section is not None:

            question = Question.query.filter_by(
                id=question_id, section_id=q_section.id).first()

            if not question:
                return {
                    "msg": "Item not found"
                }, HTTP_404_NOT_FOUND

            try:

                db.session.delete(question)
                db.session.commit()

                return {"msg": "Successfully deleted that question"}, HTTP_200_OK
            except IntegrityError as e:
                db.session.rollback()
                return {
                    "status": "Fail",
                    "msg": "Integrity error on deleting question"
                }, HTTP_409_CONFLICT
        else:
            return {
                "status": "Fail",
                "msg": "Resource not found"
            }, HTTP_404_NOT_FOUND
