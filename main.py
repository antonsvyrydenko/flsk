# -*- coding: utf-8 -*-

import os
from flask import Flask
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, send_from_directory, url_for
app = Flask(__name__)

li=[]

ALLOWED_EXTENSIONS = set(['json','txt'])
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))+'/uploads/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
		   
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
	
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
	if request.method == 'POST':
		if 'print' in request.form:
			text = request.form['text']
			global li
			li.append(text)
			return render_template('value.html', data=li)
		if 'about' in request.form:
			url = url_for('static', filename='about.txt')
			with open('static/about.txt', "r") as f:
				content = f.read()
			return render_template('about.html',about_text=content)
		if 'send' in request.form:
			file = request.files['file']
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				if not os.path.exists(UPLOAD_FOLDER):
					os.makedirs(UPLOAD_FOLDER)
				file.save(os.path.join(UPLOAD_FOLDER, filename))
			return render_template('index.html')

@app.route('/clean', methods=['POST'])
def clean_list():
	if request.method == 'POST':
		if 'cln' in request.form:
			global li
			del li[:]
	return redirect("/")
	
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')