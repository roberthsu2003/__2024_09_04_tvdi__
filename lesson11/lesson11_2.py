from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '''
        <ul>
            <li>主題</li>
            <li>產品</li>
        </ul>
    '''
    
@app.route("/name")
def hello_world1():
    return '''
        <ul>
            <li>主題1</li>
            <li>產品1</li>
        </ul>
    '''