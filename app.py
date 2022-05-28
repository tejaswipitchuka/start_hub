from email.headerregistry import Address
from logging import error
from msilib.schema import File
from pydoc import Doc, describe
from turtle import title
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request

from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, FileField,SelectField,validators
from passlib.hash import sha256_crypt
from functools import wraps



app=Flask(__name__)

#config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='start_hub'
app.config['MYSQL_CURSORCLASS']='DictCursor'

#init MySQL
mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/idea_post',methods=['POST','GET'])
def ideaPost():
    print(request.form)
    form=IdeaPostForm(request.form)
    if request.method=='POST':
        title=form.title.data
        subtitle=dict(request.form)['subtitle']
        description=dict(request.form)['description']
        #create cursor
        cur=mysql.connection.cursor()
        #execute
        cur.execute("INSERT INTO idea_post(title,subtitle,description) VALUES(%s,%s,%s)",(title,subtitle,description))
        print("inserted into idea_post")
        #commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flash('Your request has been submitted','success')
    else:
        flash('Please fill the form correctly','danger')
    return render_template('idea_post.html')

class IdeaPostForm(Form):
    title=StringField("title",[validators.Length(min=1)])
    subtitle=StringField("subtitle",[validators.Length(min=1)])
    description=StringField("description",[validators.Length(min=1)])

class RegisterRole(Form):
    role=StringField('role')

#user registration
@app.route('/register1',methods=['GET','POST'])
def register():
    form=RegisterRole(request.form)
    if request.method=='POST':
        role=dict(request.form)['role']
        print(role)
    return render_template('register1.html',form=form)


#user registration
@app.route('/register',methods=['GET','POST'])
def registergjgh():
    print(request.method,'register def')
    form=RegisterRole(request.form)
    if request.method=='POST':
        print('hello')
        username=request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password'])) 
        print(username,' ',password)
        cur=mysql.connection.cursor()
        r=cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)",(username,password))
        print(r)
        mysql.connection.commit()
        #result=cur.execute("SELECT * FROM users WHERE username=%s",[username])
        cur.close()
        return redirect(url_for('home'))
    return render_template('register1.html',form=form)
    
class Login(Form):
    username=StringField('Username',[validators.Length(min=5)])
    password=PasswordField('Password',[validators.Length(min=5)])
#user login
@app.route('/login',methods=['POST','GET'])
def login():    
    #form=Login(request.form)
    if request.method=='POST':
        username=request.form['username']
        password_candidate=request.form['password'] 
        cur=mysql.connection.cursor()
        result=cur.execute("SELECT * FROM users WHERE username=%s",[username])
        if result>0:
            #get stored hash
            data=cur.fetchone()
            password=data['password']
          
            #compare passwords
            if sha256_crypt.verify(password_candidate,password):
                #passed
                session['logged_in']=True
                session['username']=username
                # app.logger.info('PASSWORD MATCHED ')
                print('registered')
                return redirect(url_for('home'))
            else:
                error="invalid Login"
                # app.logger.info('PASSWORD NOT MATCHED')
                # flash('Invalid login','danger')
                return render_template('login.html',error=error)
        else:
            app.logger.info('no user')   
            error="username not found"
            return render_template('login.html',error=error)
    return render_template('login.html')
    



def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            #flash('Unauthorized, Please login','danger')
            return redirect(url_for('login')) 
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))


@app.route('/home')
@is_logged_in
def home():
    return render_template('home.html')


if __name__=='__main__':
    app.secret_key='raja'
    app.run(debug=True)