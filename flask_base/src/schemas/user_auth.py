from marshmallow import Schema, fields, validates_schema, ValidationError
from src.schemas.user import BaseUserSchema


# Schéma utilisateur de connexion
class UserLoginSchema(Schema):
    email = fields.String(description="email", required=True)
    password = fields.String(description="Password", required=True)


# Schéma utilisateur d'enregistrement
class UserRegisterSchema(BaseUserSchema):
    # permet de définir dans quelles conditions le schéma est validé ou nom
    @validates_schema
    def validates_schemas(self, data, **kwargs):
        if "name" not in data or data["name"] == "" or \
                "email" not in data or data["email"] == "" or \
                "password" not in data or data["password"] == "":
            raise ValidationError("['name','email','password'] must all be specified")
