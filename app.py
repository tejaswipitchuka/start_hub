from msilib.schema import File
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from datetime import date
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, FileField,SelectField,validators
from passlib.hash import sha256_crypt
from functools import wraps
import os
from twilio.rest import Client

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

class Admin(Form):
    username=StringField('username',[validators.Length(min=5)])
    password=PasswordField('password',[validators.Length(min=5)])


#https://f2ec-103-2-235-146.ngrok.io/bot

@app.route('/adminlogin',methods=['POST','GET'])
def admin():
    form=Login(request.form)
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        session['role']='admin'
        session['logged_in']=True
        if(username=='admin' and password=='admin'):
            return redirect(url_for('dashboard'))
        else:
            return 'not admin'
    return render_template('adminlogin.html')

@app.route('/dashboard')
def dashboard():
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM investor WHERE status='no'")
    projects=cur.fetchall()
    if res>0:
        return render_template('dashboard.html',projects=projects)
    else:
        msg='No pending registrations'
        return render_template('dashboard.html',msg=msg)

@app.route('/accepted/<string:email_id>')
def accepted(email_id):
    cur=mysql.connection.cursor()
    res=cur.execute("UPDATE investor SET status='yes' WHERE email_id='{email_id}' ".format(email_id=email_id))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))

@app.route('/rejected/<string:email_id>')
def rejected(email_id):
    cur=mysql.connection.cursor()
    res=cur.execute("UPDATE investor SET status='invalid' WHERE email_id='{email_id}' ".format(email_id=email_id))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))


@app.route('/idea_post',methods=['POST','GET'])
def ideaPost():
    print(request.form)
    form=IdeaPostForm(request.form)
    if request.method=='POST':
        title=form.title.data
        subtitle=dict(request.form)['subtitle']
        description=dict(request.form)['description']
        author=session['name']
        cur_date=str(date.today())
        #create cursor
        cur=mysql.connection.cursor()
        #execute
        cur.execute("INSERT INTO idea_post(title,subtitle,description,author,date) VALUES(%s,%s,%s,%s,%s)",(title,subtitle,description,author,cur_date))
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

#problemstatements
class PSForm(Form):
    title=StringField("title",[validators.Length(min=1)])
    description=StringField("description",[validators.Length(min=1)])

@app.route('/postps',methods=['POST','GET'])
def PS():
    print(request.form)
    form=PSForm(request.form)
    if request.method=='POST':
        title=form.title.data
        description=dict(request.form)['description']
        author=session['comp']
        cur_date=str(date.today())
        #create cursor
        cur=mysql.connection.cursor()
        #execute
        cur.execute("INSERT INTO ps(stmt,description,author,date) VALUES(%s,%s,%s,%s)",(title,description,author,cur_date))
        print("inserted into ps")
        #commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flash('Your request has been submitted','success')
    else:
        flash('Please fill the form correctly','danger')
    return render_template('postps.html')


#blogs
@app.route('/blog',methods=['POST','GET'])
def blogpost():
    print(request.form)
    form=BlogPostForm(request.form)
    if request.method=='POST':
        title=form.title.data
        author=dict(request.form)['author']
        description=dict(request.form)['description']
        cur_date=str(date.today())
        
        #create cursor
        cur=mysql.connection.cursor()
        #execute
        cur.execute("INSERT INTO blogs(title,author,description,date) VALUES(%s,%s,%s,%s)",(title,author,description,cur_date))
        
        #commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        
    else:
        flash('Please fill the form correctly','danger')
    return render_template('blog.html')

class BlogPostForm(Form):
    title=StringField("title",[validators.Length(min=1)])
    author=StringField("subtitle",[validators.Length(min=1)])
    description=StringField("description",[validators.Length(min=1)])
    time=StringField("time",[validators.Length(min=1)])


class RegisterRole(Form):
    role=StringField('role')

#user registration
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterRole(request.form)
    if request.method=='POST':
        role=dict(request.form)['role']
        role_url='register'+role
        print(role_url)
        return redirect(role_url)
    return render_template('register.html',form=form)

class InnovatorRegister(Form):
    firstname=StringField("firstname",[validators.Length(min=1,max=200)])
    lastname=StringField("lastname",[validators.Length(min=1,max=10)])
    email=StringField("email",[validators.Length(min=1,max=200)])
    qualification=StringField("qualification",[validators.Length(min=1,max=200)])
    mobileno=StringField("mobileno",[validators.Length(min=1,max=200)])
    linkedin=StringField("linkedin",[validators.Length(min=1,max=200)])
    password=PasswordField("password",[validators.DataRequired(),validators.Length(min=1,max=200)])

@app.route('/registerinnovator',methods=['GET','POST'])
def innovatorRegister():
    form=InnovatorRegister(request.form)
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        qualification=request.form['qualification']
        mobileno=request.form['mobileno']
        linkedin=request.form['linkedin']
        password=sha256_crypt.encrypt(str(request.form['password']))
        cur=mysql.connection.cursor()
        print(firstname,lastname,email,qualification,mobileno,linkedin,password)
        cur.execute("INSERT INTO innovator(first_name,last_name,email_id,qualification,mobile_no,linkedin,password) VALUES(%s,%s,%s,%s,%s,%s,%s)",(firstname,lastname,email,qualification,mobileno,linkedin,password))
        #commit to DB
        mysql.connection.commit()
        #close connection 
        cur.close()
        msg = 'Details Submitted'
        return render_template('registerinnovator.html', msg=msg)
    return render_template('registerinnovator.html',form=form)

class InvestorRegister(Form):
    firstname=StringField("firstname",[validators.Length(min=1,max=200)])
    lastname=StringField("lastname",[validators.Length(min=1,max=10)])
    email=StringField("email",[validators.Length(min=1,max=200)])
    mobileno=StringField("mobileno",[validators.Length(min=1,max=200)])
    linkedin=StringField("linkedin",[validators.Length(min=1,max=200)])
    company=StringField("company",[validators.Length(min=1,max=200)])
    pancard=StringField("pancard",[validators.Length(min=1,max=200)])
    password=PasswordField("password",[validators.DataRequired(),validators.Length(min=1,max=200)])

@app.route('/registerinvestor',methods=['GET','POST'])
def investorRegister():
    form=InvestorRegister(request.form)
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        mobileno=request.form['mobileno']
        linkedin=request.form['linkedin']
        company=request.form['company']
        pancard=request.form['pancard']
        status='no'
        password=sha256_crypt.encrypt(str(request.form['password']))
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO investor(first_name,last_name,email_id,mobile_no,linkedin,company,pancard,password,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(firstname,lastname,email,mobileno,linkedin,company,pancard,password,status))
        #commit to DB
        mysql.connection.commit()
        #close connection 
        cur.close()
        msg = 'Details Submitted'
        return render_template('registerinvestor.html', msg=msg)
    return render_template('registerinvestor.html',form=form)

class MentorRegister(Form):
    firstname=StringField("firstname",[validators.Length(min=1,max=200)])
    lastname=StringField("lastname",[validators.Length(min=1,max=10)])
    email=StringField("email",[validators.Length(min=1,max=200)])
    company=StringField("company",[validators.Length(min=1,max=200)])
    mobileno=StringField("mobileno",[validators.Length(min=1,max=200)])
    linkedin=StringField("linkedin",[validators.Length(min=1,max=200)])
    pancard=StringField("pancard",[validators.Length(min=1,max=200)])
    specialization=StringField("specialization",[validators.Length(min=1,max=200)])
    password=PasswordField("password",[validators.DataRequired(),validators.Length(min=1,max=200)])

@app.route('/registermentor',methods=['GET','POST'])
def mentorRegister():
    form=MentorRegister(request.form)
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        company=request.form['company']
        mobileno=request.form['mobileno']
        linkedin=request.form['linkedin']
        qualification=request.form['qualification']
        specialization=request.form['specialization']
        password=sha256_crypt.encrypt(str(request.form['password']))
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO mentor(first_name,last_name,email_id,company,mobile_no,linkedin,qualification,specialization,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(firstname,lastname,email,company,mobileno,linkedin,qualification,specialization,password))
        #commit to DB
        mysql.connection.commit()
        #close connection 
        cur.close()
        msg = 'Details Submitted'
        return render_template('registermentor.html', msg=msg)
    return render_template('registermentor.html',form=form)

class OrgRegister(Form):
    email=StringField("email",[validators.Length(min=1,max=200)])
    company=StringField("company",[validators.Length(min=1,max=200)])
    mobileno=StringField("mobileno",[validators.Length(min=1,max=200)])
    linkedin=StringField("linkedin",[validators.Length(min=1,max=200)])
    pancard=StringField("pancard",[validators.Length(min=1,max=200)])
    password=PasswordField("password",[validators.DataRequired(),validators.Length(min=1,max=200)])

@app.route('/registerorganization',methods=['GET','POST'])
def organizationRegister():
    form=OrgRegister(request.form)
    if request.method=='POST':
        email=request.form['email']
        company=request.form['company']
        mobileno=request.form['mobileno']
        linkedin=request.form['linkedin']
        pancard=request.form['pancard']
        password=sha256_crypt.encrypt(str(request.form['password']))
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO organization(email_id,company,mobile_no,linkedin,pancard,password) VALUES(%s,%s,%s,%s,%s,%s)",(email,company,mobileno,linkedin,pancard,password))
        #commit to DB
        mysql.connection.commit()
        #close connection 
        cur.close()
        msg = 'Details Submitted'
        return render_template('registerorganization.html', msg=msg)
    return render_template('registerorganization.html',form=form)


    
class Login(Form):
    email=StringField('email',[validators.Length(min=5)])
    password=PasswordField('password',[validators.Length(min=5)])
    role=StringField('role')


#user login
@app.route('/login',methods=['POST','GET'])
def login():    
    form=Login(request.form)
    if request.method=='POST':
        email=request.form['email']
        password_input=request.form['password'] 
        role=request.form['role'] 
        cur=mysql.connection.cursor()
        result=cur.execute("SELECT * FROM {dbname} WHERE email_id='{emailid}'".format(dbname=role,emailid=email))
        print(result)
        if result>0:
            #get stored hash
            data=cur.fetchone()
            password=data['password']
            #compare passwords
            if sha256_crypt.verify(password_input,password):
                #passed
                print('in if')
                session['logged_in']=True
                cur.execute("SELECT * FROM {dbname} WHERE email_id='{emailid}'".format(dbname=role,emailid=email))
                data=cur.fetchone()
                session['role']=role
                if(role=='investor' and data['status']=='no'):
                    error="Registration not confirmed"
                    return render_template('login.html',error=error)
                if(role=='investor' and data['status']=='invalid'):
                    error="You are not authorized user"
                    return render_template('login.html',error=error)
                if(role!='organization'):
                    session['name']=data['first_name']
                if(role=='organization'):
                    session['comp']=data['company']
                session['title']=''
                # app.logger.info('PASSWORD MATCHED ')
                print('registered')
                if(role!='organization'):
                    print(session['name'])
                return redirect(url_for('index'))
            else:
                error="Invalid Login"
                # app.logger.info('PASSWORD NOT MATCHED')
                # flash('Invalid login','danger')
                return render_template('login.html',error=error)
        else:
            #app.logger.info('no user')   
            error="Username not found"
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
    return redirect(url_for('index'))


@app.route('/viewhalfideas')
@is_logged_in
def viewIdeas():
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM idea_post")
    projects=cur.fetchall()
    if res>0:
        return render_template('viewhalfideas.html',projects=projects)
    else:
        msg='No Idea posts Available'
        return render_template('viewhalfideas.html',msg=msg)

@app.route('/viewideas/<string:title>')
@is_logged_in
def ideaPosts(title):
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM idea_post WHERE title=%s",[title])
    projects=cur.fetchone()
    res=cur.execute("SELECT * FROM comments WHERE title=%s",[title])
    comments=cur.fetchall()
    print(comments)
    session['ptitle']=title
    return render_template('viewideas.html',projects=projects,comments=comments)

#ps for innovators
@app.route('/viewhalfps')
@is_logged_in
def viewhalfps():
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM ps")
    projects=cur.fetchall()
    if res>0:
        return render_template('viewhalfps.html',projects=projects)
    else:
        msg='No Problem Statements Available'
        return render_template('viewhalfps.html',msg=msg)
        
@app.route('/viewhalfps/<string:stmt>')
@is_logged_in
def viewps(stmt):
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM ps WHERE stmt=%s",[stmt])
    projects=cur.fetchone()
    session['psname']=stmt
    session['company']=projects['author']
    print(projects)
    if res>0:
        return render_template('viewps.html',projects=projects)
    else:
        msg='No Problem Statements  Available'
        return render_template('viewps.html',msg=msg)

@app.route('/viewblog')
@is_logged_in
def viewblog():
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM blogs")
    projects=cur.fetchall()
    if res>0:
        return render_template('viewblog.html',projects=projects)
    else:
        msg='No blogs Available'
        return render_template('viewblog.html',msg=msg)
        
@app.route('/showblog/<string:title>')
@is_logged_in
def showblog(title):
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM blogs WHERE title=%s",[title])
    projects=cur.fetchall()
    if res>0:
        return render_template('showblog.html',projects=projects)
    else:
        msg='No blogs Available'
        return render_template('showblog.html',msg=msg)
           
@app.route('/increasecount/<string:title>')
@is_logged_in
def increase(title):
    cur=mysql.connection.cursor()
    print(title)
    session[title]=True
    res=cur.execute("SELECT upvotes FROM idea_post where title=%s",[title])
    projects=cur.fetchone()
    print(projects)
    count=projects['upvotes']
    if(count==None):
        count=0
    count+=1
    res=cur.execute("UPDATE idea_post SET upvotes={count} WHERE title='{title}' ".format(count=count,title=title))
    #commit to DB
    mysql.connection.commit()
    #close connection 
    cur.close()
    if res>0:
        return redirect(url_for('viewIdeas'))
    else:
        msg='No Idea posts Available'
        return redirect(url_for('viewIdeas'))


@app.route('/blogcount/<string:title>')
@is_logged_in
def increase1(title):
    cur=mysql.connection.cursor()
    print(title)
    session[title]=True
    res=cur.execute("SELECT likes FROM blogs where title=%s",[title])
    projects=cur.fetchone()
    print(projects)
    count=projects['likes']
    if(count==None):
        count=0
    count+=1
    res=cur.execute("UPDATE blogs SET likes={count} WHERE title='{title}' ".format(count=count,title=title))
    #commit to DB
    mysql.connection.commit()
    #close connection 
    cur.close()
    if res>0:
        return redirect(url_for('viewblog'))
    else:
        msg='No Idea posts Available'
        return redirect(url_for('viewblog'))

@app.route('/sort')
def sort():
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM idea_post ORDER BY UPVOTES DESC")
    projects=cur.fetchall()
    print(projects)
    if res>0:
        return render_template('viewhalfideas.html',projects=projects)
    else:
        msg='No Idea posts Available'
        return render_template('viewhalfideas.html',msg=msg)

class Comment(Form):
    comment=TextAreaField('comment')

@app.route('/comments',methods=['POST'])
@is_logged_in
def comment():
    form=Comment(request.form)
    print('in comm*****')
    cur=mysql.connection.cursor()
    title=session['ptitle']
    res=cur.execute("SELECT * FROM idea_post WHERE title=%s",[title])
    projects=cur.fetchone()
    res=cur.execute("SELECT * FROM comments WHERE title=%s",[title])
    comments=cur.fetchall()
    if request.method=='POST':
        print('hiii*******')
        c=request.form['comment']
        print(c) 
        print(type(c))      
        res=cur.execute("INSERT INTO comments(title,author,comment) VALUES(%s,%s,%s)",(session['ptitle'],session['name'],c))
        mysql.connection.commit()        
        cur.close()
        return render_template('viewideas.html',projects=projects,comments=comments)
    return render_template('viewideas.html',form=form,projects=projects,comments=comments)


UPLOAD_FOLDER = 'C:/Users/tejasaswi/Desktop/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/fileupload', methods = ['GET', 'POST'])
def upload_file():
    print("fbfbfgf")
    if request.method == 'POST':
        f = request.files['uploadedfile']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        path=str(app.config['UPLOAD_FOLDER'])+'/'+str(f.filename)
        print(path)
        cur=mysql.connection.cursor()
        res=cur.execute("UPDATE ps SET solution='{path}' WHERE stmt='{name}' ".format(path=path,name=session['psname']))
        res=cur.execute("INSERT INTO solutions(stmt,author,solution,org) VALUES(%s,%s,%s,%s)",(session['psname'],session['name'],path,session['company']))
        res=cur.execute("SELECT * FROM ps")
        projects=cur.fetchall()
        mysql.connection.commit() 
        msg='Solution submitted successfully!'
        return render_template('viewps.html',msg=msg,projects=projects)

@app.route('/solutions')
@is_logged_in
def solutions():
    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM solutions")
    projects=cur.fetchall()
    print(projects)
    if res>0:
        return render_template('solutions.html',projects=projects)
    else:
        msg='No solutions Available'
        return render_template('solutions.html',msg=msg)

@app.route('/sms/<string:name>')
def sms(name):
    account_sid = 'AC1c8f2e49cf4e0851203887cdcf744c36'
    auth_token = '13f1ca28947f365282e0c0e71f48f598'


    cur=mysql.connection.cursor()
    res=cur.execute("SELECT * FROM innovator WHERE first_name=%s",[name])
    projects=cur.fetchone()
    print(projects['mobile_no'])
    number='+91'+str(projects['mobile_no'])
    print(number)
    client = Client(account_sid, auth_token)
    res=cur.execute("SELECT * FROM investor WHERE first_name=%s",[session['name']])
    projects=cur.fetchone()
    body='\nHello there, '+str(session['name'])+' here. I am interested in knowing more about your idea. Lets connect here\n Contact no: '+str(projects['mobile_no'])
    message = client.messages.create(
                                from_='+18646607895',
                                body =body,
                                to =number
                            )
    return 'Message sent successfully!'

if __name__=='__main__':
    app.secret_key='123456'
    app.run(debug=True)