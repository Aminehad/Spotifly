import json
from flask import Blueprint, request
from flask_login import login_required
from marshmallow import ValidationError

from src.models.http_exceptions import *
from src.schemas.song import  SongUpdateSchema
from src.schemas.errors import *
import src.services.songs as songs_service

# from routes import songs  
songs = Blueprint(name="songs", import_name=__name__)

@songs.route('/<id>', methods=['GET'])
#@login_required
def get_song(id):
    """
    ---
    get:
      description: Getting a song
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of song id
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '404':
          description: Not found
          content:
            application/json:
              schema: NotFound
            application/yaml:
              schema: NotFound
      tags:
          - songs
    """
    print("id a get song",id)
    return songs_service.get_song(id)


@songs.route('/', methods=['GET'])
#@login_required
def get_songs():
    """
    ---
    get:
      description: Getting all songs
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: Songs
            application/yaml:
              schema: Songs
        '401':

          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
    """
    return songs_service.get_songs()

@songs.route('/', methods=['POST'])
#@login_required
def post_song():
    """
    ---
    post:
      description: Creating a song
      requestBody:
        required: true
        content:
            application/json:
                schema: SongCreate
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '422':
          description: Unprocessable entity
          content:
            application/json:
              schema: UnprocessableEntity
            application/yaml:
              schema: UnprocessableEntity
      tags:
          - songs
    """
    print(request.json, "this is from route")
    return songs_service.create_song(request.json)

@songs.route('/<id>', methods=['PUT'])
#@login_required
def put_song(id):
    """
    ---
    put:
      description: Updating a song
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of song id
      requestBody:
        required: true
        content:
            application/json:
                schema: SongUpdate
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '404':
          description: Not found
          content:
            application/json:
              schema: NotFound
            application/yaml:
              schema: NotFound
        '422':
          description: Unprocessable entity
          content:
            application/json:
              schema: UnprocessableEntity
            application/yaml:
              schema: UnprocessableEntity
      tags:
          - songs
    """
    return songs_service.update_song(id, request.json)

