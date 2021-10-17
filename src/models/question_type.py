from sqlalchemy import event, DDL
from src import db, ma


class QuestionType(db.Model):
    __tablename__ = "question_type"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), unique=True, nullable=False)
    question = db.relationship("Question", backref="question_type")

    def __init__(self, type) -> None:
        self.type = type


# @event.listens_for(QuestionType.__table__, 'after_create')
# def create_question_types(*args, **kwargs):
#     db.session.add(QuestionType(type='Abierta'))
#     db.session.add(QuestionType(type='Cerrada'))
#     db.session.add(QuestionType(type='Multiple'))
#     db.session.commit()
event.listen(QuestionType.__table__, 'after_create',
             DDL(""" INSERT INTO question_type (id, type) VALUES (1, 'Abierta'), (2, 'Multiple con unica opcion'), (3, 'Multiple con varias opciones') """))


class QuestionTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuestionType
        include_fk = True
