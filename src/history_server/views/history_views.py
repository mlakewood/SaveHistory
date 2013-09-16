from flask import Flask, render_template, request, redirect, url_for, jsonify

from history_server import app

###
# Routing for your application.
###

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



def get_history():
    from history_model import HistoryRecord
    
    rows = app.config['DB_SESSION'].query(HistoryRecord).all()
    output = []
    for row in rows:
        output.append(row._serialise())
    
    return jsonify(items=output)

def get_history_html():
    from history_model import HistoryRecord
    rows = app.config['DB_SESSION'].query(HistoryRecord).all()
    print len(rows)
    return render_template('home.html', rows=rows)

###
# The functions below should be applicable to all Flask apps.
###

def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


def beta_home():
    """Send your static text file."""
    return render_template('beta_home.html')