from worker import add_nums

from flask import (
   Flask,
   request,
   jsonify,
   Markup,
   render_template 
)

#app = Flask(__name__, template_folder='./templates',static_folder='./static')
app = Flask(__name__)

@app.route("/")
def index():
    return '<h1>Welcome to the Machine Learning Course.</h1>'

@app.route("/test", methods=['POST', 'GET'])
def accuracy():
    if request.method == 'POST':
        r = add_nums.delay()
        a = r.get()
        return '<h1>Addition result {}</h1>'.format(a)

    return '''<form method="POST">
    <input type="submit">
    </form>'''

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5100,debug=True)
