from wtforms import StringField, SubmitField, SelectMultipleField, Field, SelectField
from wtforms.widgets import TextInput
from flask_wtf import FlaskForm
from backend.db import get_labels
from backend.models.Body import Body

def prepare_labels():
    labels = list()
    for l in get_labels():
        label = '_'.join(l[0].split(' '))
        labels.append((label, label))
    return labels
    
class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ', '.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
            self.data = list(filter(None, self.data))
        else:
            self.data = []

class AddObjectForm(FlaskForm):
    name = StringField("Object name")
    labels = SelectMultipleField("Labels from database")
    custom_labels = TagListField("New labels")
    orbits = SelectField("Orbits")
    submit = SubmitField("Add")

    def set_orbits_choices(self):
        self.orbits.choices = [(b[0]["name"], b[0]["name"]) for b in Body.get_all()]

    def set_labels_choices(self):
        self.labels.choices = prepare_labels()

class ChangeColorForm(FlaskForm):
    color_labels = SelectField("Change color")

    def set_labels_choices(self):
        self.color_labels.choices = prepare_labels()