#!usr/bin/env python

#pip install flask
from flask import Flask, json, render_template, request, send_file
import os
import pytz
from datetime import datetime, timezone


# Create instance of Flask app
app = Flask(__name__)

# decorator
@app.route("/")
def hello():
    utc_dt = datetime.now(timezone.utc)
    CST = pytz.timezone('US/Central')
    return render_template('index.html', timestamp=datetime.now())

@app.route("/all")
def nobel_all():
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))
    
    return render_template('nobel_all.html',data=data_json)

@app.route("/add")
def form_func():
    form_url = os.path.join("templates","form.html")
    return send_file(form_url)

@app.route("/<year>", methods=['GET', 'POST'])
def nobel_year(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))
    
    if request.method == 'GET':
        data = data_json['prizes']
        year = request.view_args['year']
        output_data = [x for x in data if x['year']==year]

        return render_template('nobel_year.html', data=output_data)

    elif request.method == 'POST':
        year = request.form['year']
        category = request.form['category']
        id = request.form['id']
        firstname = request.form['firstname']
        surname = request.form['surname']
        motivation = request.form['motivation']
        share = request.form['share']
        prizes_year =   {"category": category, 
                        "laureates": 
                            [{"firstname":firstname, 
                            "id": id, 
                            "motivation":motivation, 
                            "share":share, 
                            "surname":surname
                            }],
                            'year':year
                        }
        
        with open(json_url, "r+") as file:
            data_append = json.load(file)
            data_append["prizes"].append(prizes_year)
            file.seek(0)
            json.dump(data_append, file)

        text_success = "Data successfully added: " + str(prizes_year)
        return render_template('index.html', data=text_success)

if __name__ == "__main__":
    app.run(debug=True)