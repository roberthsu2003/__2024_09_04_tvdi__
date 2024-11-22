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