from flask import Flask
from render_static_template_blueprint import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
