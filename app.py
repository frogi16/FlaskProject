from flask import Flask, render_template, request, flash, redirect, url_for
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

from backend.forms import AddObjectForm, ChangeColorForm
from backend.db import db_query
from backend.models.Body import Body

@app.route('/', methods=['GET', 'POST'])
def add_object():
    def handle_post_object_form(form):
        if not form.is_submitted():
            raise ValueError("Form not submitted")
        if not len(request.form['name']):
            raise ValueError("Please, fill a name!")

        body = Body(request.form['name'],  form.labels.data + form.custom_labels.data, form.orbits.data)
        body.add()
        if body.orbits:
            body.add_orbits_relationship()

        return f"Added {body.name}"

    form = AddObjectForm()
    form.set_labels_choices()
    form.set_orbits_choices()
    change_color_form = ChangeColorForm()
    change_color_form.set_labels_choices()

    if request.method == "POST":
        try:
            flash(handle_post_object_form(form))
            return redirect(url_for('add_object'))
        except Exception as e:
            flash(str(e))

    bodies = []
    for [bod] in Body.get_all():
        labels = {f"{'_'.join(l.split(' '))}" : "true" for l in bod.labels}
        body = {"group": "nodes", "data" : {"id" : bod["name"], **labels}}
        bodies.append(body)
    
    rel = db_query("MATCH (st:Body)<-[:ORBITS]-(orbiting) RETURN orbiting, st")
    relations = [{"group": "edges", "data" : {"id" : st["name"] + orb["name"], "source" : st["name"], "target" : orb["name"]}} for orb, st in rel]

    return render_template('test/add.html', form=form, change_color_form=change_color_form, relations_data=relations, bodies_data=bodies)

if __name__ == '__main__':
    import os
    HOST = '0.0.0.0'
    PORT = os.environ.get('PORT', 17995)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.run(HOST, PORT)
