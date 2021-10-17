from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from src import db
from src.models import Answer, AnswerSchema
from sqlalchemy.exc import IntegrityError
from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

# esquemas

answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)

# CREAR O MOSTRAR TODAS LAS RESPUESTAS


class ManipulateAnswerApi(Resource):
    @jwt_required()
    def post(self):
        try:
            answer = request.json.get("answer", None)  # Input JSONB type data.
            question_id = request.json.get("question_id", None)

            if not answer or not question_id:
                return {
                    "msg": "Answer and question id is required"
                }

            answered = Answer.query.filter(
                Answer.question_id == question_id).first()

            if answered:
                return {
                    "error": "Question already answered"
                }
            elif not answered:
                m_answer = Answer(question_id=question_id, answer=answer)
                m_answer.save_to_db()

            return {
                "status": "Success",
                "data": answer_schema.dump(m_answer)
            }
            # return make_response(jsonify(
            #     {
            #         "id": m_answer.id,
            #         "answer": m_answer.answer,
            #         "question_id": m_answer.question_id,
            #     }
            # ), HTTP_201_CREATED)

        except IntegrityError as e:
            db.session.rollback()
            return {
                "status": "Fail",
                "msg": "Integrity error on creating answer maybe because question key not exist"
            }, HTTP_409_CONFLICT

    @jwt_required()
    def get(self):

        answers = Answer.query.all()

        # data = []

        # for answer in answers:
        #     data.append({
        #         "id": answer.id,
        #         "answer": answer.answer,
        #         "question_id": answer.question_id
        #     })

        return {
            "status": "Success",
            "data": answers_schema.dump(answers)
        }, HTTP_200_OK

        # return make_response(jsonify(
        #     {
        #         "status": "Success",
        #         "data": data,
        #     }
        # ), HTTP_200_OK)


class GetAnswerApi(Resource):
    @jwt_required()
    def get(self, id):

        answer = Answer.query.filter_by(id=id).first()

        if not answer:
            return {
                "msg": "Answer not found"
            }, HTTP_404_NOT_FOUND

        return {
            "status": "Success",
            "data": answer_schema.dump(answer)
        }, HTTP_200_OK
        # return make_response(jsonify({
        #     "status": "Success",
        #     "data": {
        #         "id": answer.id,
        #         "answer": answer.answer,
        #         "question_id": answer.question_id
        #     }
        # }), HTTP_200_OK)


class UpdateAnswerApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            answer = request.json.get('answer', None)
            # question_id = request.json.get("question_id", None)

            # if not answer or not question_id:
            #     return {
            #         "msg": "Answer and question id is required"
            #     }

            q_answer = Answer.query.filter_by(id=id).first()

            q_answer.answer = answer
            # q_answer.question_id = question_id
            db.session.commit()

            return {
                "status": "Success",
                "data": answer_schema.dump(q_answer)
            }, HTTP_200_OK

            # return make_response(jsonify(
            #     {
            #         "status": "Success",
            #         "data": {
            #             "id": q_answer.id,
            #             "answer": q_answer.answer,
            #             "question_id": q_answer.question_id
            #         },
            #     }
            # ), HTTP_200_OK)

        except IntegrityError as e:
            db.session.rollback()
            return {
                "status": "Fail",
                "msg": "Integrity error on updating answer"
            }, HTTP_409_CONFLICT


class DeleteAnswerApi(Resource):
    @jwt_required()
    def delete(self, id):
        try:
            q_answer = Answer.query.filter_by(id=id).first()

            if not q_answer:
                return {
                    "msg": "Answer not found"
                }, HTTP_404_NOT_FOUND

            db.session.delete(q_answer)
            db.session.commit()

            return {"msg": "Successfully deleted that answer"}, HTTP_200_OK

        except IntegrityError as e:
            db.session.rollback()
            return {
                "status": "Fail",
                "msg": "Integrity error on deleting answer"
            }, HTTP_409_CONFLICT
