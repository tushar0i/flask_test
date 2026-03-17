from flask import Flask , request , make_response , render_template

app = Flask(__name__,template_folder='templates')

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

if __name__  == '__main__':
    app.run(host='127.0.0.1',port=9892,debug=True)