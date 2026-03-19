from flask import Flask , request , make_response , render_template , redirect , url_for , session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os 

app = Flask(__name__,template_folder='templates', static_folder='static',static_url_path='/')
CORS(app)

# folder setup to store files 
app.secret_key = 'ALLTHESTARS'

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__),'static','uploads','pdf')
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024 

os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS  

# ----------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return "<div> this is the thing </div>"

@app.route('/greet/<name>')
def name(name):
    return f'<div> hi {name} </div>'

@app.route('/sum/<int:num1>/<int:num2>')
def sum(num1,num2):
    return f'<div> {num1} + {num2} = {num1 + num2} </div>'

@app.route('/handel_url_param')
def handel_param():
    return str(request.args)

@app.route('/handel_url_param2')
def handel_param2():
    email = request.args.get('email')
    name = request.args['name']
    return f'{name},{email}'

# http://127.0.0.1:9892/handel_url_param2?name=1&email=something@one.com&soem=thing this will work 
# http://127.0.0.1:9892/handel_url_param2?name=1  output will contian email:None,name:'i'
# http://127.0.0.1:9892/handel_url_param2?email=something@one.com this will give bad key error 

@app.route('/handel_url_param3')
def handel_param3():
    if 'email' in request.args.keys() and 'name' in request.args.keys():
        email = request.args['email']
        name = request.args['name']
        return f'HI {name} your email is {email}'
    else:
        return 'some params are missing fix the code first'

@app.route('/reqt', methods=['GET','[POST]','[DELETE]'])
def some():
    if request.method == 'GET':
        return 'this is a get request\n' , 200 # returning status code
    elif request.method == 'POST':
        return 'this is a post request\n' , 201 # created 
    elif request.method == 'DELETE':
        return 'this is a delete request\n'
    else:
        return 'you will never be able to see me\n'
    

# status codes
''' 
2xx success
200 OK
201 created 
202 accepted
204 no content
206 partial content 

3xx redirection 
301 moves permanently 
302 found(previously move temporarily)
304 not modified 

4xx client error 
400 bad request 
401 unauthorized 
403 forbidden
404 not found 
408 request timeout
429 too many request

5xx server errors 
500 Internal Server error 
501 not implimented 
502 bad gateway
503 service unavailable
504 gateway timeout
'''
@app.route('/hello',methods=['GET','[POST]'])
def another():
    if request.method == 'GET':
        if 'name' in request.args.keys():
            name = request.args['name']
            respones =  make_response(f'hello {name} this is a get request')
            respones.status_code = 200
            respones.headers['content-type'] = 'text/plain'
            return respones
    elif request.method == 'POST':
        return 'nothing to post here'


@app.route('/index')
def index():
    myname = 'random person'
    mybalance = 200+980
    itemlist = ['one','two','three','four','five','six']
    return render_template('index.html',name=myname ,balance=mybalance,items=itemlist)

@app.route('/filters')
def filter():
    text = 'Hello Flask!'
    return render_template('filters.html',some_text=text)

# custom filters 
@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]

@app.template_filter('repate')
def repate(s , times=2):
    return s*times

@app.template_filter('alternate_case')
def alternate_case(s):
    out = ''.join([c.upper() if i % 2 == 0 else c.lower() for i,c in enumerate(s)])
    return out

@app.route('/a_dynamic_url')
def other():
    return render_template('other.html')

@app.route('/redirect_endpoint')
def redirect_endpoint():
    return redirect(url_for('other'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #do this
        if 'email' and 'password' in request.form.keys(): 
            email = request.form.get('email')
            password = request.form['password']
            if email == 'some@one.com' and password == 'someone':
                return "SUCCESS"
            else:
                return "FAILURE"
        else:
            return 'INVALID FORM'
    elif request.method == 'GET':
        #do this 
        return render_template('login.html')


@app.route('/fileupload',methods=['GET','POST'])
def fileupload():
    if request.method == 'GET':
        return render_template('fileupload.html')
    elif request.method == 'POST':

        file = request.files['file']

        if not file or file.filename == '':
            return render_template('fileupload.html', error='No file selected') 

        if file.content_type == "application/pdf" and allowed_file(file.filename):
            filename = secure_filename(f'something_{file.filename}') # just for one file only 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for("viewfile",filename=filename))
        else:
            return render_template("fileupload.html", error='Only pdf file allowed')


@app.route('/viewfile/<filename>')
def viewfile(filename):
    return render_template("viewfile.html",filename=filename)

@app.route('/viewimage')
def viewimage():
    return render_template("viewimage.html")


# -------------------Session server side  -------------------- 


@app.route('/sessiontest')
def sessiontest():
    return render_template('sessiontest.html', message='something')

@app.route('/setdata')
def setdata():
    session['name'] = 'someone'
    session['text'] = 'just a random thing I want to say'
    session['temp'] = 'we will delete this later'
    return render_template('sessiontest.html', message='session data set successfully' )

@app.route('/getdata')
def getdata():
    if 'name' in session.keys() and 'text' in session.keys() and 'temp' in session.keys():
        name = session['name']
        text = session['text']
        temp = session['temp']
        return render_template('sessiontest.html',message=f'Name:{name} , Text:{text} , Temp:{temp}')
    else:
        return render_template('sessiontest.html', message=f'No session found')

@app.route('/cleartempdata')
def cleartemp():
    if 'temp' in session.keys():
        session.pop('temp')
        return render_template('sessiontest.html',message=f'temp cleared')
    else:
        return render_template('sessiontest.html', message=f'No temp found')


@app.route('/cleardata')
def cleardata():
    session.clear()
    return render_template('sessiontest.html',message=f'session data cleared successfully')


if __name__  == '__main__':
    app.run(host='127.0.0.1',port=9892,debug=True)