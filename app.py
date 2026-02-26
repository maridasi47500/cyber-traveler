from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>&#127908; &#127928; hey je suis la cyber star! voila mon identite numerique</p><form>ajouter 1 donnee<textarea></textarea></form>"
