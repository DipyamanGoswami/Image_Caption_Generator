from flask import Flask,render_template,request,redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import generatecap
import augment
import os
from wtforms.validators import InputRequired

app= Flask(__name__)
app.config['SECRET_KEY']= 'topsecret'
app.config['UPLOAD_FOLDER']='Static/files'

class UploadFileForm(FlaskForm):
    file= FileField("File", validators=[InputRequired()])
    submit= SubmitField("Upload File")

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])

def home():
    form= UploadFileForm()
    if form.validate_on_submit():
        file= form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return redirect(request.url)
    return render_template('index.html',form=form)

@app.route('/re' , methods=['get','post'])
def captions():
    form = UploadFileForm()
    if form.validate_on_submit():
        file=form.file.data
        filename=secure_filename(file.filename)
        filename='Static/files/'+filename
        caplist= generatecap.predict_step([filename])

        return_sequence=10
        for context in caplist:
            result=augment.get_response(context,return_sequence)

            return render_template('gen.html', result=result, filename=filename)

if __name__=='__main__':
    app.run(debug=True)