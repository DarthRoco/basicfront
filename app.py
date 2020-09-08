from flask import Flask, redirect, url_for, request, render_template
#from model import model_predict
import os
from werkzeug.utils import secure_filename
import requests
import base64

app = Flask(__name__, static_url_path='/C:/Users/Shreyas Bhat/Desktop/basicfront/')


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the file from post request
        #f = request.files['file']
        f1 = request.files['file']
        f2 = request.form.get('scale')
        f3 = request.form.get('image_type')
        
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f1.filename))
        f1.save(file_path)

       
        
        output_path = os.path.join(basepath, 'static', secure_filename(f1.filename))
        
        
        r = requests.post("http://ec2-18-191-233-204.us-east-2.compute.amazonaws.com:8080/predictions/super_res",files={'data':open(file_path,'rb')})
        #print(r.content,"HEioowhd---------------------------")
        imgdata = base64.b64decode(r.content)
        with open(output_path, 'wb') as f:
        	f.write(imgdata)
        #r.content.save(output_path)
        
        return render_template('index.html', HR_output = url_for('static', filename = secure_filename(f1.filename))) #https://stackoverflow.com/questions/46785507/python-flask-display-image-on-a-html-page
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True)