from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from api_response_builder import *
from openai_completion import openai_completion_wrapper

BLUEPRINT_NAME = 'openai_completion'
openai_completion_blueprint = Blueprint(BLUEPRINT_NAME, __name__)

openai_completion_wrapper.set_openai_api_key(
    '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')


@openai_completion_blueprint.route(
    f'/api/{BLUEPRINT_NAME}/autocomplete', methods=['GET', 'POST'])
def autocomplete():
  content_type = request.headers.get('Content-Type')
  if content_type != 'application/json':
    raise BadRequest()
  content = request.json
  try:
    document = content['document']
  except KeyError:
    raise BadRequest()
  return build_api_response(
      HTTPStatus.OK, content=openai_completion_wrapper.autocomplete(document))
