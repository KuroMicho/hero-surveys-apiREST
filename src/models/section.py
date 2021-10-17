from src import db, ma


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(500), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey(
        'survey.id'), nullable=False)

    survey = db.relationship(
        "Survey", backref='sections')

    def __init__(self, header, survey_id):
        self.header = header
        self.survey_id = survey_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        include_fk = True
