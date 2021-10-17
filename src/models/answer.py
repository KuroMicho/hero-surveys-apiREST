from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSON
from src import db, ma


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(JSON)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    question_id = db.Column(db.Integer, db.ForeignKey(
        "question.id"), nullable=False, unique=True)

    question = db.relationship("Question", backref="answers")

    def __init__(self, answer, question_id):
        self.answer = answer
        self.question_id = question_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()


class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        include_fk = True
