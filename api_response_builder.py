from typing import Optional, Any, Dict, Union
from http import HTTPStatus


def build_api_response(
    status: int,  # HTTPStatus
    description: Optional[str] = '',
    error: Optional[str] = '',
    content: Optional[Any] = None) -> Dict[str, Union[str, Any]]:
  api_response = {'status': status}
  if description:
    api_response['description'] = description
  if error:
    api_response['error'] = error
  if content:
    api_response['content'] = content
  return api_response
