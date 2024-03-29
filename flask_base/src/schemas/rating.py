from marshmallow import Schema, fields, validates_schema, ValidationError


#shéma rating de sortie (renvoyé au front)

class RatingSchema(Schema):
    
        comment = fields.String(description="Content")  
        id = fields.String(description="UUID")
        rating = fields.Integer(description="Rating")
        song_id = fields.String(description="Music id")
        user_id = fields.String(description="User id")
        
        @staticmethod
        def is_empty(obj):
            return (not obj.get("id") or obj.get("id") == "") and \
                (not obj.get("user_id") or obj.get("user_id") == "") and \
                (not obj.get("song_id") or obj.get("song_id") == "") and \
                (not obj.get("comment") or obj.get("comment") == "") and \
                (not obj.get("rating_date") or obj.get("rating_date") == "") and \
                (not obj.get("rating") or obj.get("rating") == "")
        
class BaseRatingSchema(Schema):
    user_id = fields.String(description="User id")
    song_id = fields.String(description="Music id")
    comment = fields.String(description="Content")
    rating_date = fields.DateTime(description="Date")
    rating = fields.Integer(description="Rating")

# Schéma rating de modification (content, date, rating)
class RatingUpdateSchema(BaseRatingSchema):
    # permet de définir dans quelles conditions le schéma est validé ou nom
    @validates_schema
    def validates_schemas(self, data, **kwargs):
        if not (("comment" in data and data["comment"] != "") or
                ("rating" in data and data["rating"] != "")):
            raise ValidationError("at least one of ['comment','rating'] must be specified")
        