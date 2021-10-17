from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSON
from src import db, ma


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(JSON)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    questionType_id = db.Column(db.Integer, db.ForeignKey(
        "question_type.id"), nullable=False)

    section_id = db.Column(db.Integer, db.ForeignKey(
        "section.id"), nullable=False)

    section = db.relationship("Section", backref="questions")

    def check_multiple(self, options, questionType_id):
        if not options and questionType_id == 1:
            return False
        if questionType_id == 2 or questionType_id == 3:
            return options

    def __init__(self, question, questionType_id, options, section_id) -> None:
        self.question = question
        self.options = self.check_multiple(options, questionType_id)
        self.questionType_id = questionType_id
        self.section_id = section_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        include_fk = True
