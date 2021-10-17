# src/models/routes.py
def init_api(api):
    from .auth import MeApi, RegisterApi, LoginApi, RefreshApi, LogoutApi
    from .author import AuthorSurveyApi, AuthorSurveysApi, AuthorSurveyStatsApi
    from .survey import CreateSurveyApi, SurveyApi, PublicUrlApi, PublicRedirectApi
    from .section import CreateSectionApi, SectionApi, SectionsApi
    from .question import CreateQuestionApi, QuestionApi, QuestionsApi
    # from .answer import ManipulateAnswerApi, GetAnswerApi
    from .feedback import FeedbackApi
    # auth
    api.add_resource(MeApi, '/auth/me')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(RegisterApi, '/auth/register')
    api.add_resource(RefreshApi, '/auth/refresh')
    api.add_resource(LogoutApi, '/auth/logout')
    # author
    api.add_resource(
        AuthorSurveyApi, '/author/<int:author_id>/survey/<int:survey_id>')
    api.add_resource(AuthorSurveysApi, '/author/<int:author_id>/surveys')
    api.add_resource(AuthorSurveyStatsApi,
                     '/author/<int:author_id>/survey/<int:survey_id>/stats')
    # survey
    api.add_resource(CreateSurveyApi, '/survey')
    api.add_resource(SurveyApi, '/survey/<int:survey_id>')
    # section
    api.add_resource(CreateSectionApi, '/survey/<int:survey_id>/section')
    api.add_resource(SectionsApi, '/survey/<int:survey_id>/section')
    api.add_resource(
        SectionApi, '/survey/<int:survey_id>/section/<int:section_id>')
    # question
    api.add_resource(
        CreateQuestionApi, '/survey/<int:survey_id>/section/<int:section_id>/question')
    api.add_resource(
        QuestionsApi, '/survey/<int:survey_id>/section/<int:section_id>/question')
    api.add_resource(
        QuestionApi, '/survey/<int:survey_id>/section/<int:section_id>/question/<int:question_id>')
    # answer
    # api.add_resource(ManipulateAnswerApi, '/answer')
    # public
    api.add_resource(PublicUrlApi, '/s/<string:url>')
    api.add_resource(PublicRedirectApi, '/<string:short_url>')
    # feedback
    api.add_resource(FeedbackApi, '/feedback/submit')
