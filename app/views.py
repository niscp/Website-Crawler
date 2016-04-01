async_mode = None

if async_mode is None:
    try:
        import eventlet

        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey

            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)
import ast
import time
from threading import Thread

from app import app
from app import interface
from flask import render_template, request, redirect,url_for,make_response
from bs4 import BeautifulSoup
import urllib2
from flask_socketio import SocketIO, emit
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

website = "http://www.justdial.com/"




@app.route('/loctest', methods=['GET', 'POST'])
def myloctest():
    if request.method == 'POST':
        location = None
        area = None
        if 'location' in request.form.keys():
            location = request.form['location']
        if 'area' in request.form.keys():
            area = request.form['area']
        return redirect (url_for('testme', location=location,area=area))




flag = True

def background_thread(location,area):
    count = 1
    global flag
    while flag:
        count += 1
        page = count
        a = interface.get_restra(location,area,page)
        if len(a) == 0:
            flag = False

        data = str(a)
        socketio.emit('my response',
                      {'data': data, 'count': count},
                      namespace='/test')



@socketio.on('connect', namespace='/test')
def test_connect():
    pass
    #emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)



@app.route('/<location>/<area>', methods=['GET', 'POST'])
@app.route('/<location>/', defaults={'area':None}, methods=['GET', 'POST'])
@app.route('/', defaults={'location': 'Bangalore','area':None}, methods=['GET', 'POST'])
def testme(location,area):
    page = 1
    result = interface.get_restra(location,area,page)
    global thread
    if thread is None:
        thread = Thread(target=background_thread,args=(location,area,))
        thread.daemon = True
        thread.start()
    return render_template('new_test.html',msg=None,data=result)



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
    return csv