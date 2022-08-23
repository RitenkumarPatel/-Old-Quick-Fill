from typing import Dict, Any, Optional, Union

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/documents']


def _read_structural_elements(elements):

  def read_paragraph_element(element):
    text_run = element.get('textRun')
    if not text_run:
      return ''
    return text_run.get('content')

  text = ''
  for value in elements:
    if 'paragraph' in value:
      elements = value.get('paragraph').get('elements')
      for elem in elements:
        text += read_paragraph_element(elem)
    elif 'table' in value:
      table = value.get('table')
      for row in table.get('tableRows'):
        cells = row.get('tableCells')
        for cell in cells:
          text += _read_structural_elements(cell.get('content'))
    elif 'tableOfContents' in value:
      toc = value.get('tableOfContents')
      text += _read_structural_elements(toc.get('content'))
  return text


def get_service(credentials: Credentials) -> Resource:
  """Gets an instance of a Google Docs service object.

  Args:
    credentials (google.oauth2.credentials.Credentials): The credentials 
        provided by authorization.

  Returns (googleapiclient.discovery.Resource):
    The Google Docs service object.
  """
  try:
    service = build('docs', 'v1', credentials=credentials)
    return service
  except HttpError:
    print(HttpError)


def get_document(service: Resource,
                 document_id: str) -> Union[Dict[str, Any], Dict]:
  """Gets information about a Google Doc.

  Args:
    service (googleapiclient.discovery.Resource): The Google Docs service 
        object.
    document_id (str): An ID that corresponds to a valid Google Doc.

  Returns:
    A dictionary containing the ID, title, and body of the Google Doc. For
    example:
      
    {'id': '<some-44-character-id>',
     'title': 'Testing Document',
     'body': 'This is a testing document.\n'}
  """
  try:
    document = service.documents().get(documentId=document_id).execute()
    return {
        'id': document.get('documentId'),
        'title': document.get('title'),
        'body': _read_structural_elements(document.get('body').get('content'))
    }
  except HttpError:
    return dict()


class DocumentRequests:
  """A class for creating requests sent to the Google Docs Resource.

  Attributes:
    requests (List[Dict[str, Union[Dict[str, Dict[str, int]], str]]]): A list of 
        request objects. For example:
      
        {'insertText': {'location': {'index': 0},
                        'text': 'Hello, World!'}}
  """

  def __init__(self):
    self.requests = []

  def add_insertion_request(self, index: int, text: str):
    """Adds an insertion request to the requests attribute.

    Args:
      index: The index where the text will be inserted.
      text: The text that will be inserted.
    """
    self.requests.append(
        {'insertText': {
            'location': {
                'index': index
            },
            'text': text
        }})

  def add_deletion_request(self):
    pass


def modify_body(service: Resource, document_id: str,
                document_requests: DocumentRequests):
  """Sends text requests to the Google Docs Resource.

  Args:
    service (googleapiclient.discovery.Resource): The Google Docs service 
        object.
    document_id (str): An ID that corresponds to a valid Google Doc.
    document_requests (DocumentRequests): A DocumentRequests object.
  """
  service.documents().batchUpdate(
      documentId=document_id, body={
          'requests': document_requests.requests
      }).execute()
