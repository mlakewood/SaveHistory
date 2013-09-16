
from werkzeug import import_string, cached_property

from history_server import app
from history_server.views.history_views import post_history, get_history, get_history_html, send_text_file, beta_home

def define_urls(app):
    """
    Define the url mapping
    """
    app.add_url_rule('/history', view_func=post_history, methods=['POST'])
    app.add_url_rule('/history', view_func=get_history,methods=['GET'])
    app.add_url_rule('/history_view', view_func=get_history_html,methods=['GET'])
    app.add_url_rule('/index.html', view_func=beta_home, methods=['GET'])
    app.add_url_rule('/<file_name>.txt', view_func=send_text_file)