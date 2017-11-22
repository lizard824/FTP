# -*- coding: utf-8 -*-

import os,sys,hashlib, time

from flask import Flask, render_template, request, jsonify ,redirect, url_for

reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config['UPLOADED_PATH'] = os.getcwd() + '/upload'
app.config['MAX_CONTENT_LENGTH'] = 100 *1024 *1024
m = hashlib.md5()
# encode1 = []
# name = []
dictList=[]
nameList=[]

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        dict = {}
        for f in request.files.getlist('file'):
            path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
            if os.path.exists(path)==False:
                f.save(path)
                m.update(f.filename)
                encodefile = m.hexdigest()
                # encode1.append(encodefile)
                # name.append(f.filename)
                # dict[f.filename] = encodefile
                dict["name"] = f.filename
                nameList.append(f.filename)
                dict["encode"] = encodefile
                dict["url"] = path
                dict["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                dictList.append(dict)
                print dictList
        # return redirect(url_for('show', name=encode1))
    return render_template('index.html', di=dictList)


@app.route('/')
def reload():

    for f in os.listdir(app.config['UPLOADED_PATH']):
        if f !=".DS_Store" :
            dict = {}
            dict["name"] = f

            m.update(f)
            dict["encode"] = m.hexdigest()
            dict["url"] = app.config['UPLOADED_PATH'] + f
            dict["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if f not in nameList:
                nameList.append(f)
                dictList.append(dict)
    return redirect(url_for('upload_file',di=dictList))
    # return render_template('index.html', di=dictList)

@app.route('/file/<name>')
def show(name):
    print 'name' + name

    return render_template('show.html',  name=name)


@app.route('/api/upload', methods=['POST'])
def api_message():
    file_dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if request.method == 'POST':
        f = request.files['file']
        if f:
            f.save(os.path.join(file_dir, f.filename))
            m.update(f.filename)
            file = m.hexdigest()

            return jsonify({"msg":"success","filename":file})
        else:
            return jsonify({"msg":"failed"})



if __name__ == '__main__':
    app.run(debug=True)