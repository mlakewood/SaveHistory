"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import json

from flask import Flask, render_template, request, redirect, url_for, jsonify
from dateutil.parser import parse
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


Base = declarative_base()

def get_engine(url):
    return create_engine(url, convert_unicode=True)

def get_db_session(engine):
    return scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
def init_db(engine, Base):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from history_model import HistoryRecord
    Base.metadata.create_all(bind=engine)



###
# Routing for your application.
###

@app.route('/history', methods=['POST'])
def post_history():
    """Render website's home page."""
    from history_model import HistoryRecord
    data = json.loads(request.data)
    command_date = parse(data['Time'])
    utc_comm_date = command_date.astimezone(pytz.utc)
    record = HistoryRecord(data['Command'], utc_comm_date)
    app.config['DB_SESSION'].add(record)
    app.config['DB_SESSION'].commit()
    return "done!"



@app.route('/history', methods=['GET'])
def get_history():
    from history_model import HistoryRecord
    rows = app.config['DB_SESSION'].query(HistoryRecord).all()
    output = []
    for row in rows:
        output.append(row._serialise())
    
    return jsonify(items=output)

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    engine = get_engine('sqlite:///history.sql')
    app.config['DB_SESSION'] = get_db_session(engine)
    app.run(debug=True)
