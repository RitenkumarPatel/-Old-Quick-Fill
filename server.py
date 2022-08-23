from flask import Flask

import google_docs
import openai_completion

app = Flask(__name__)
app.register_blueprint(google_docs.google_docs_blueprint)
app.register_blueprint(openai_completion.openai_completion_blueprint)
app.secret_key = 'QuickFill App'

if __name__ == '__main__':
  app.run(debug=True)
