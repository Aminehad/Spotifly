import json
import requests
from sqlalchemy import exc
from marshmallow import EXCLUDE
from flask_login import current_user, logout_user

from src.schemas.user import UserSchema
from src.models.user import User as UserModel
from src.models.http_exceptions import *
import src.repositories.users as users_repository


users_url = "http://localhost:8080/Users/"  # URL de l'API users (golang)



def get_user(id):
   
    response = requests.request(method="GET", url=users_url+id)
    return response.json(), response.status_code

def get_users():
    response = requests.request(method="GET", url=users_url)
    return response.json(), response.status_code

def create_user(user_register):

    email = user_register.get("email")
    #print(email)

    # on récupère le modèle utilisateur pour la BDD
    user_model = UserModel.from_dict_with_clear_password(user_register)
    # on récupère le schéma utilisateur pour la requête vers l'API users
    user_schema = UserSchema().loads(json.dumps(user_register), unknown=EXCLUDE)
    #print(user_schema)#pour voir ce qui il exclu 
    user_schema["email"] = email
 
    #print(user_schema)#pour voir est ce quil a remplit l'email pour lapi  
    #print(user_model.id,user_model.email)#pour voir ce que va etre insere dans la base de donnee de flask 
    
    # on crée l'utilisateur côté API users
    response = requests.request(method="POST", url=users_url, json=user_schema)
    if response.status_code != 201: #si != 201 alors il y a eu un probleme mais si je la fais, la creation de l'utilisateur dans la bd dans le try ne sera pas faite
        return response.json(), response.status_code
    # on ajoute l'utilisateur dans la base de données
    # pour que les données entre API et BDD correspondent
    try:
        user_model.id = response.json()["id"]
        users_repository.add_user(user_model)
    except Exception:
        raise SomethingWentWrong

    return response.json(), response.status_code

def modify_user(id, user_update):
    # on vérifie que l'utilisateur se modifie lui-même
    if id != current_user.id:
        raise Forbidden

    # s'il y a quelque chose à changer côté API (email, name)
    user_schema = UserSchema().loads(json.dumps(user_update), unknown=EXCLUDE)
    print(user_schema)
    response = None
    if not UserSchema.is_empty(user_schema):
        # on lance la requête de modification
        response = requests.request(method="PUT", url=users_url+id, json=user_schema)
        if response.status_code != 200:
            return response.json(), response.status_code

    # s'il y a quelque chose à changer côté BDD
    user_model = UserModel.from_dict_with_clear_password(user_update)
    if not user_model.is_empty():
        user_model.id = id
        found_user = users_repository.get_user_from_id(id)
        if not user_model.email:
            user_model.email = found_user.email
        if not user_model.encrypted_password:
            user_model.encrypted_password = found_user.encrypted_password
        try:
            users_repository.update_user(user_model)
        except exc.IntegrityError as e:
            if "NOT NULL" in e.orig.args[0]:
                raise UnprocessableEntity
            raise Conflict

    return ("Modified succesfully", response.status_code) if response else get_user(id)


def delete_user(id):
    # on vérifie que l'utilisateur se supprime lui-même
    print("id a delete user",id)
    if id != current_user.id:
        raise Forbidden

    # on lance la requête de suppression
    response = requests.request(method="DELETE", url=users_url+id)
    if response.status_code == 200: 
        # on supprime l'utilisateur de la base de données   
        users_repository.delete_user(id)
        #logout_user()
        return "Deleted succesfully",200
    return  response.status_code,response.json()
    
def get_user_from_db(email):
    return users_repository.get_user(email)


def user_exists(email):
    return get_user_from_db(email) is not None
