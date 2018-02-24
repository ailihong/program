#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://flask.pocoo.org/docs/patterns/fileuploads/
"""
备注:通过http接收文件
如果在云服务器上运行该程序，需要指定ip为0.0.0.0
"""
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='kill pid by task')
    parser.add_argument('--ip','-i', dest='ip', help='ipv4',default=None)
    parser.add_argument('--port','-p', dest='port', help='port',default=None)
    parser.add_argument('--path','-pa', dest='path', help='save path',default=None)
    args = parser.parse_args()
    return args

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print '**found file', file.filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # for browser, add 'redirect' function on top of 'url_for'
            return url_for('uploaded_file',
                                    filename=filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def main(args):
    global UPLOAD_FOLDER
    UPLOAD_FOLDER=args.path
    app.run(host=args.ip, port=int(args.port),debug=True)

if __name__ == '__main__':
    args = parse_args()
    if args.ip == None or args.port == None or args.path == None:
        print 'please enter option'
    else:
        main(args)
