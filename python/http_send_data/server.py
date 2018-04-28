from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    print(request.form['foo']) # should display 'bar'
    return 'Received !' # response to your request.


@app.route('/bai', methods=['POST'])
def result1():
    print(request.form['foo']) # should display 'bar'
    return 'Received !' # response to your request.

if __name__ == '__main__':
    app.run('127.0.0.1', port=12345,debug=True)
