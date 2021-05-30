"""
Web server that gives users ability to get predictions
"""
from worker import add_nums, get_prediction
from sklearn.ensemble import RandomForestRegressor
from flask import (
   Flask,
   request,
   jsonify,
   Markup,
   render_template 
)
from subprocess import call

#app = Flask(__name__, template_folder='./templates',static_folder='./static')
app = Flask(__name__)

@app.route("/")
def index():
    return '<h1>Welcome to the Machine Learning Course.</h1>'


@app.route("/test", methods=['POST', 'GET'])
def accuracy():
    if request.method == 'POST':
        #r = add_nums.delay()
        #a = r.get()
        prediction = get_prediction.delay(request.form["year"], request.form["forks"], request.form["has_downloads"], request.form["has_issues"], request.form["has_wiki"], request.form["open_issues_count"], request.form["size"], request.form["subscribers_count"])
        a = prediction.get()
        return '<h1>Predicted stars: {}</h1>'.format(a)

    return '''
    <form method="POST">
    <label for="year">Year</label>
    <input type="text" name="year" id="year">
    <label for="forks">Forks</label>
    <input type="text" name="forks" id="forks">
    <label for="has_downloads">Has downloads (0 / 1)</label>
    <input type="text" name="has_downloads" id="has_downloads">
    <label for="has_issues">Has issues (0 / 1)</label>
    <input type="text" name="has_issues" id="has_issues">
    <label for="has_wiki">Has wiki (0 / 1)</label>
    <input type="text" name="has_wiki" id="has_wiki">
    <label for="open_issues_count">Open issues count</label>
    <input type="text" name="open_issues_count" id="open_issues_count">
    <label for="size">Size</label>
    <input type="text" name="size" id="size">
    <label for "subscribers_count">Subscribers count</label>
    <input type="text" name="subscribers_count" id="subscribers_count">
    <input type="submit">
    </form>'''

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5100,debug=True)
