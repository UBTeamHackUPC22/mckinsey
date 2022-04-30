
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class CSVForm(FlaskForm):
    photo = FileField(
        validators=[ 
            FileRequired(), 
            FileAllowed(['csv', 'Images only!'])
        ])