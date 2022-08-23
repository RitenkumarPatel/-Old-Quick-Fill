import re

import openai
from transformers import pipeline


def _create_prompt(document: str) -> str:
  summarizer = pipeline('summarization')
  sentences = [
      sentence.strip()
      for sentence in re.split('[.!?\n]', document)
      if sentence != ''
  ]

  summary = summarizer(
      document, max_length=130, min_length=30,
      do_sample=False)[0]['summary_text']
      
  if sentences:
    prompt = ('Finish the below sentence:\n\n'
              'Example: > The mitochondria\n'
              'Output: are the powerhouse of the cell.\n\n'
              f'Here is some context:\n{summary}\n\n'
              f'> {sentences[-1]}')
    return prompt


def _get_response(prompt: str) -> str:
  response = openai.Completion.create(
      model='text-davinci-002',
      prompt=prompt,
      temperature=0.05,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)
  return response['choices'][0]['text']


def set_openai_api_key(api_key: str):
  """Sets the OpenAi API Key to enable access to OpenAi APIs.
  
  Args:
    api_key: An OpenAi API Key.
  """
  openai.api_key = api_key


def autocomplete(document: str) -> str:
  """Prompts the OpenAi Completion API.
  
  Creates an OpenAi Completion API prompt and then sends a request with the
  prompt to the OpenAi Completion API.

  Args:
    document: The document inputted to create the OpenAi Completion API prompt.

  Returns:
    A response sent by the OpenAi Completion API.
  """
  prompt = _create_prompt(document)
  response = _get_response(prompt)
  return response
