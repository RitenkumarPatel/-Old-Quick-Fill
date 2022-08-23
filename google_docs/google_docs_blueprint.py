import os.path
import pathlib

from flask import Blueprint, session, abort, redirect, request
import google
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

from api_response_builder import *
from google_docs import google_docs_wrapper

BLUEPRINT_NAME = 'google_docs'
google_docs_blueprint = Blueprint(BLUEPRINT_NAME, __name__)

GOOGLE_CLIENT_ID = (
    '1026035935263-1o8l4e63v62j31jtteeu6clqne7r7rdu.apps.googleusercontent.com')
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/userinfo.profile'
]

# Bypass https requirement for oauth 2. For development only.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, 'client_secrets.json')
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=SCOPES,
    redirect_uri=f'http://127.0.0.1:5000/api/{BLUEPRINT_NAME}/callback')


def requires_google_authorization(function):

  def wrapper(*args, **kwargs):
    if 'google_id' not in session:
      return build_api_response(
          HTTPStatus.UNAUTHORIZED, error='The user is not logged in.')
    else:
      return function()

  wrapper.__name__ = function.__name__
  return wrapper


@google_docs_blueprint.route(f'/api/{BLUEPRINT_NAME}/login')
def login():
  authorization_url, state = flow.authorization_url()
  session['state'] = state
  return redirect(authorization_url)


@google_docs_blueprint.route(f'/api/{BLUEPRINT_NAME}/logout')
def logout():
  session.clear()
  return build_api_response(HTTPStatus.OK, description='The user logged out.')


@google_docs_blueprint.route(f'/api/{BLUEPRINT_NAME}/callback')
def callback():
  flow.fetch_token(authorization_response=request.url)
  
  if not session['state'] == request.args['state']:
    abort(500)  # Mismatched state
    
  cached_session = cachecontrol.CacheControl(requests.session())
  token_request = google.auth.transport.requests.Request(session=cached_session)
  id_info = id_token.verify_oauth2_token(
      id_token=flow.credentials._id_token,
      request=token_request,
      audience=GOOGLE_CLIENT_ID)
  
  session['google_id'] = id_info.get('sub')
  session['name'] = id_info.get('name')
  return build_api_response(
      HTTPStatus.OK, description='Authorized the user.', content=dict(id_info))


@google_docs_blueprint.route(
    f'/api/{BLUEPRINT_NAME}/get_document', methods=['GET'])
@requires_google_authorization
def get_document(*args):
  document_id = request.args.get('document_id')
  if not document_id:
    return build_api_response(
        HTTPStatus.BAD_REQUEST,
        error='The URL parameter document_id is not found.')
  
  service = google_docs_wrapper.get_service(credentials=flow.credentials)
  document_info = google_docs_wrapper.get_document(service, document_id)
  if document_info:
    return build_api_response(HTTPStatus.OK, content=document_info)
  else:
    return build_api_response(
        HTTPStatus.BAD_REQUEST,
        error=('The URL parameter document_id is either invalid or belongs to a'
               ' document to which the authorized user does not have access.'))


@google_docs_blueprint.route(f'/api/{BLUEPRINT_NAME}/insert_text')
@requires_google_authorization
def insert_text(*args):
  # TODO
  return build_api_response(
      HTTPStatus.OK, description='TODO: Inserted the text.')
