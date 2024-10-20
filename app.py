from flask import Flask, render_template ,redirect ,url_for , session , request
import os
from json import dumps
# from werkzeug.utils import secure_filename
from database.database import insert_data , reterieve_username , create_interest_database_for_user , new_interest , find_interests ,delete_interest
from api_testing import test_api
import string
import random
from scraping.scrap2 import generate_image
from flask_cors import CORS, cross_origin
from explore_api import scrape_wikipedia_intro

# file handling code 
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'thisIsASecurityKey'

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
#####################################################

online_users = []

#different routes 
@app.route("/home")
def home_page():
    if "user" in session:
        listOfInterests = find_interests(session['user'])
        images = []
        for i in listOfInterests:
            images.append(generate_image(i))
        return render_template("index.html",
                               data=listOfInterests,username=session['user']
                               ,assigned_image=reterieve_username(session['user'])[0][-1]
                               ,email=reterieve_username(session['user'])[0][3]
                               ,script_to_run=''
                               ,images=images
                               ,key=reterieve_username(session['user'])[0][5])
    else: 
        return redirect(url_for('log_in'))


@app.route("/signup",methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        OpenAi_key = request.form['OpenAI']

        # print(username,password,email,OpenAi_key)
        
                # check if the post request has the file part
        if 'filey' not in request.files:
            print("file not found")

        res = ''.join(random.choices(string.ascii_letters,
                            k=7)) # initializing size of string
        # storing data in database

        scripts = ['','api key is not working','username already exist']
        if reterieve_username(username)!=[]:
            return render_template('signup.html',script_to_run=scripts[2])
        elif test_api(OpenAi_key)!=1:
            return render_template('signup.html',script_to_run=scripts[1])
        else:
            try:
                file = request.files['filey']
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':
                    insert_data(username.lower,password,email,OpenAi_key,"")
                    create_interest_database_for_user(username.lower())
                if file and allowed_file(file.filename):
                    # filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(res)+'.jpg'))
                    insert_data(username,password,email,OpenAi_key,os.path.join(app.config['UPLOAD_FOLDER'], '/'+str(res)+'.jpg'))
                    create_interest_database_for_user(username.lower())

            except Exception as e:
                print("some error occured",e)

        return redirect(url_for('log_in'))
    else:
        return render_template('signup.html',script_to_run='')

@app.route("/login",methods=['POST','GET'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if reterieve_username(username) and reterieve_username(username)[0][2]==password:
            if username.lower() not in online_users:
                session['user'] = username
                online_users.append(str(session['user']).lower()) 
                print(online_users)
            else:
                return render_template('login.html',mesg='user is already online')
            # session["email"] = reterieve_username(username)[0][3]
            # session["assigned_image"] = 
            return redirect(url_for('gate_keeper'))
        else:
            print('user not found and alert is not showing for some reson')
            return render_template("login.html",mesg='username or password is not correct')
    else:
        print('get request')
        return render_template("login.html",mesg='')

@app.route('/')
def gate_keeper():
    if "user" in session:
        return redirect(url_for('home_page'))
    else: 
        return redirect(url_for('log_in'))
  
@app.route('/signout/<username>',methods=['GET','POST'])
def sign_out(username):
    session.pop('user')
    try:
        online_users.pop(online_users.index(str(username).lower()))
    except:
        print('user not in list')
    return redirect(url_for('log_in'))

@app.route('/deleteInterest',methods=['POST','GET'])
def delete_interests():
    if request.method == 'POST':
        usernames = request.json['username']
        interests = request.json['interest']
        delete_interest(usernames,interests)
        return redirect(url_for('home_page')) 
    else:
        return 'no  no no no , no post requests shall be entertained.'

@app.route('/addInterest',methods=['POST','GET'])
def add_interest():
    if request.method=='POST':
        if 'user' in session:
            username = request.form['username']
            interest = request.form['interest']
            try:
                new_interest(username,interest.replace(' ','_'))
                return redirect(url_for('home_page'))
            except:
                return redirect(url_for('home_page')) 
             
    else:
        return 'no no no no , GET requests are not allowed , how on the earth you did that'


@app.route("/<key>/<topic>",methods=['GET'])
@cross_origin(['http://127.0.0.1:5000','https://127.0.0.1:5000'])
def generate(key,topic):
    if "user" in session:
        data = scrape_wikipedia_intro(key,topic)
        data = {'returned':data}
        return data
    else: 
        return redirect(url_for('log_in'))

LAN_HOST = '192.168.100.3'
LOCAL_HOST = ''

if __name__ == "__main__":
    app.run(debug=True,host=LOCAL_HOST) 
