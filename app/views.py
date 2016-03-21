import ast

from app import app
from app import interface
from flask import render_template, request, redirect,url_for,make_response


@app.route('/<location>/<int:page>', defaults={'area': None}, methods=['GET', 'POST'])
@app.route('/<location>/<area>', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/<location>/', defaults={'page': 1,'area':None}, methods=['GET', 'POST'])
@app.route('/', defaults={'page': 1, 'location': 'Bangalore','area':None}, methods=['GET', 'POST'])
@app.route('/<location>/<area>/<int:page>', methods=['GET', 'POST'])
def jd(location, page,area):
    result = interface.get_restra(location,area,page)
    if len(result) == 0:
        return render_template('404.html')
    if result:
        return render_template('test.html', data=result, page=page, location=location,area=area)
    return 'nothing found'


@app.route('/loc', methods=['GET', 'POST'])
def myloc():
    if request.method == 'POST':
        location = None
        area = None
        if 'location' in request.form.keys():
            location = request.form['location']
        if 'area' in request.form.keys():
            area = request.form['area']
        return redirect (url_for('jd', location=location,area=area))






@app.route('/nis', methods=['GET', 'POST'])
def nis():
    a = request.form['data']
    a = ast.literal_eval(a)
    csv ="NAME,RATING,ADDRESS,CONTACT"
    b = ""
    for item in a:
        name = item['name']
        rating = item['rating']
        address = item['address']
        contact = item['contact']
        b = str(b)+'\n'+'"'+name+'","'+rating+'","'+address+'","'+contact+'"'
    # We need to modify the response, so the first thing we
    # need to do is create a response out of the CSV string
    csv = csv + b
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response