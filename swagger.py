template = {
    "info": {
        "title": "Hero Surveys API",
        "description": "API for surveys",
        "contact": {
            "responsibleOrganization": "SanJK Tech",
            "email": "rainbook2000@gmail.com",
        },
        "termsOfService": "www.twitter.com/riascosdev",
        "version": "1.0",
    },
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
    "components": {
        #-------------------------------
        # Reusable schemas (data models)
        #-------------------------------
        "securitySchemes": {
            "user_auth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
        },
        "schemas": {
            "user_log_in": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "example": "eyJ0dasd1g3V1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTk1Njc0MTMsImlhdCI6MTU5OTQ4MTAxMywic3ViIjoxfQ"
                    },
                    "user": {
                        "type": "object",
                        "$ref": "#/components/schemas/user"
                    }
                }
            },
            "register_user": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "example": "SongKi"
                    },
                    "email": {
                        "type": "string",
                        "example": "SongKi2021@gmail.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "123456"
                    }
                }
            },
            "user": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "username": {
                        "type": "string",
                        "example": "kuromicho"
                    },
                    "email": {
                        "type": "string",
                        "example": "sanjktech@gmail.com"
                    },
                }
            },
            "login_user": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "jajoydev@gmail.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "123456"
                    }
                }
            },
            "create_survey": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Cute Pets"
                    },
                    "image": {
                        "type": "string",
                        "example": "banner.png"
                    },
                    "url": {
                        "type": "string",
                        "example": "abc123"
                    },
                }
            },
            "survey": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "title": {
                        "type": "string",
                        "example": "Cute Pets"
                    },
                    "image": {
                        "type": "string",
                        "example": "banner.png"
                    },
                    "image_name": {
                        "type": "string",
                        "example": "banner"
                    },
                    "mime_type": {
                        "type": "string",
                        "example": "image/png"
                    },
                    "url": {
                        "type": "string",
                        "example": "abc123"
                    },
                    "short_url": {
                        "type": "string",
                        "example": "9cbvd"
                    },
                    "visits": {
                        "type": "string",
                        "example": "0"
                    },
                    "date_created": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "date_updated": {
                        "type": "string",
                        "example": "2021-08-15T16:28:39"
                    },
                    "author_id": {
                        "type": "string",
                        "example": "1"
                    },
                }
            },
            "stats": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "visits": {
                        "type": "string",
                        "example": "99"
                    },
                    "url": {
                        "type": "string",
                        "example": "http://..."
                    },
                    "author_id": {
                        "type": "string",
                        "example": "1"
                    },
                    "sections": {
                        "type": "object",
                        "example": "[]"
                    },
                }
            },
            "create_section": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "header": {
                        "type": "string",
                        "example": "section_turtles"
                    },
                }
            },
            "section": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "header": {
                        "type": "string",
                        "example": "Mascotas"
                    },
                    "survey_id": {
                        "type": "string",
                        "example": "99"
                    },
                    "questions": {
                        "type": "string",
                        "example": "[]"
                    }
                }
            },
            "question": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "date_created": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "question_text": {
                        "type": "string",
                        "example": "Do you like...?"
                    },
                    "questionType_id": {
                        "type": "string",
                        "example": "2"
                    },
                    "section_id": {
                        "type": "string",
                        "example": "55"
                    },
                    "answers": {
                        "type": "string",
                        "example": "[]"
                    }
                }
            },
            "create_question": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "question_text": {
                        "type": "string",
                        "example": "How old are you?"
                    },
                    "questionType_id": {
                        "type": "string",
                        "example": "2"
                    },
                }
            },
            "share_feedback": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Borre"
                    },
                    "email": {
                        "type": "string",
                        "example": "yisus_kun@gmail.com"
                    },
                    "comment": {
                        "type": "string",
                        "example": "So so"
                    }
                }
            },
            "api_response": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Success to ~~~"
                    }
                }
            },
            "api_fail_response": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Fail to ~~~"
                    }
                }
            },
        }
    },
    "security": {
        "user_auth": [],
    }
}


swagger_config = {
    "title": "Surveys API",
    "uiversion": 3,
    "openapi": "3.0.0",
    "doc_dir": './src/docs/',
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
