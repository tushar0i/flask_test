from flask import Flask , request

app = Flask(__name__)

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
        return 'this is a get request\n' , 201 # returning status code
    elif request.method == 'POST':
        return 'this is a post request\n' , 
    elif request.method == 'DELETE':
        return 'this is a delete request\n'
    else:
        return 'you will never be able to see me\n'
    
if __name__  == '__main__':
    app.run(host='127.0.0.1',port=9892,debug=True)