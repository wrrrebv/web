from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    abort
)
from article import Article
import os
from database import Database


app = Flask(__name__)
app.config["SECRET_KEY"] = "jlk1235352"
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

Database.create_table()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    user_email = request.form.get("user_email")
    user_phone = request.form.get("user_phone")
    user_password = request.form.get("user_password")
    user_password_repeat = request.form.get("user_password_repeat")

    if not user_email:
        flash("электронная почта не может быть пустой!")
        return redirect(request.url)
    
    if not user_phone:
        flash("номер телефона не может быть пустым!")
        return redirect(request.url)
    
    if not user_password:
        flash("пароль не может быть пустым!")
        return redirect(request.url)
    
    if not user_password_repeat or user_password != user_password_repeat:
        flash("пароли не совпадают!")
        return redirect(request.url)

    return redirect(url_for("index"))
    

@app.route("/")
@app.route("/index")
def index():
    articles = Database.get_all_articles()

    groups = []
    k = 3
    for i in range(0, len(articles), k):
        groups.append(articles[i : i+k])

    return render_template("ruwiki.html", groups=groups)


@app.route("/article/<name>")
def article(name):
    article = Database.find_article_by_title(name)
    if article is None:
        return f"<h1>Статьи '{name}' не существует!</h1>"
    
    return render_template('article.html', article=article)

@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

@app.route('/delete_article/<int:id>', methods=['POST'])
def delete_article(id):
    deleted = Database.delete_article_by_id(id)
    if not deleted:
        abort(404, f"Article with id '{id}' doesn't exist")
    return redirect(url_for('index'))

@app.route('/edit_article/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    article = Database.find_article_by_id(id)

    if request.method == "GET":
        
        if article is None:
            abort(404, f"Article with id '{id}' doesn't exist")

        return render_template('edit_article.html', article=article)
    
    title = request.form.get("title")    
    if title is None:
        title = article.title

    content = request.form.get("content")
    if content is None:
        content = article.content

    photo = request.files.get("photo")
    if photo is None or not photo.filename:
        filename = article.photo
    else:
        photo.save(app.config["UPLOAD_FOLDER"] + photo.filename)
        filename = photo.filename

    Database.update_article(id, title, content, filename)
    return redirect(url_for('article', name=title))

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'GET':
        return render_template('add_article.html')
    
    # POST-запрос далее
    title = request.form.get("title")
    if title is None:
        flash("Для статьи необходимо название")
        redirect(request.url)
        return

    content = request.form.get("content")
    if content is None:
        flash("Для статьи необходим текст")
        redirect(request.url)
        return

    photo = request.files.get("photo")
    if photo is None or not photo.filename:
        flash("Для статьи нужна фотография")
        redirect(request.url)
        return

    photo.save(app.config["UPLOAD_FOLDER"] + photo.filename)
    article = Article(title, content, photo.filename)
    Database.save(article)

    return redirect(url_for('index'))

@app.route("/articles")
def show_articles():
    articles = Database.get_all_articles()

    groups = []
    k = 3
    for i in range(0, len(articles), k):
        groups.append(articles[i : i+k])

    return render_template('articles.html', groups = groups)

if __name__ == '__main__':
    app.run(debug=True)