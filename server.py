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
    title_article = "Ёж соник"
    text_article = """Соник — синий антропоморфный ёж, созданный художником Наото Осимой,
                    программистом Юдзи Накой и дизайнером Хирокадзу Ясухарой. Во время
                    разработки было предложено множество образов главного героя будущей
                    игры, но разработчики остановились на ёжике синего цвета. Своё имя
                    Соник получил за способность бегать на сверхзвуковых скоростях
                    (англ. sonic — «звуковой; со скоростью звука»)."""
    article_image_title = "Соник"
    article_image_path = "static/sonic.png"

    return render_template('article.html',
                            title_article=title_article,
                            text_article=text_article,
                            article_image_titlew=article_image_title,
                            article_image_path=article_image_path)

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
