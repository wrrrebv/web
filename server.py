from flask import Flask, render_template


app = Flask(__name__)



@app.route('/')
def ruwiki():
    return render_template(R'ruwiki.html')

@app.route('/hello')
def hello():
    return "Привет, мир!"
    
@app.route('/sonic')
def sonic_article():
    return render_template('article.html')

@app.route('/base')
def base():
    return render_template('base.html', title="Китайский новый год")

@app.route("/max")
def find_max():
    a = int(request.args["a"])
    b = int(request.args["b"])

    if a > b: 
        return f"<h1>Максимум это число a: {a}</h1>"
    else:
        return f"<h1>Максимум это число b: {b}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
