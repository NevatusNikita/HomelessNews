# 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 - токен для github
from flask import Flask, render_template, redirect, request, make_response, session, jsonify
from werkzeug.exceptions import abort
from bs4 import BeautifulSoup
import requests

from api import news_api, jobs_api
from data import db_session
from data.news import News
from data.users import User
from data.economics_news import EconomicNews
from data.politics_news import PoliticsNews
from data.science_news import ScienceNews
from data.culture_news import CultureNews
from data.cis_news import CISNews
from data.foreign_news import ForeignNews
from data.travel_news import TravelNews
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from resources import news_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

# для списка объектов
api.add_resource(news_resources.NewsListResource, '/api/v2/news')

# для одного объекта
api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
economics_lst = []
politics_lst = []
science_lst = []


def search_news(url, class_, teg):
    news_url = []
    titles = []
    news_text = []
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    economics_news = soup.find_all(teg, class_=class_)
    for news in economics_news:
        lst = str(news).split()
        ind = str(news.text)
        titles.append(news.text[:ind.find(':') - 2])
        for el in lst:
            if el[:4] == 'href':
                if el[6] == '/':
                    news_url.append('https://lenta.ru' + el[6:el.rfind('/') + 1])
                else:
                    news_url.append(el[6:el.rfind('/') + 1])
    for elem in news_url:
        request2 = requests.get(elem)
        soup = BeautifulSoup(request2.text, 'html.parser')
        elem_text = soup.find_all('div', class_='topic-body__content')
        if elem_text == list():
            news_text.append(elem)
        else:
            for e in elem_text:
                news_text.append(e.text)
    return titles, news_text


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)

    count = 0
    for item in news:
        count += 1

    return render_template("index.html", news=news, count=count)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/news/economics', methods=['GET', 'POST'])
def economics_news():
    titles_ec, news_text_ec = search_news('https://lenta.ru/rubrics/economics/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_ec[:20]:
        if t not in economics_lst:
            news = EconomicNews()
            news.title = t
            news.content = news_text_ec[titles_ec.index(t)]
            news.is_private = False
            current_user.economics_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
        news = db_sess.query(EconomicNews).filter(EconomicNews.is_private != True)
    return render_template("economics_news.html", news=news)


@app.route('/news/politics', methods=['GET', 'POST'])
def politics_news():
    titles_pol, news_text_pol = search_news('https://lenta.ru/rubrics/world/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_pol[:20]:
        if t not in politics_lst:
            news = PoliticsNews()
            news.title = t
            news.content = news_text_pol[titles_pol.index(t)]
            news.is_private = False
            current_user.politics_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
    return redirect('/')


@app.route('/news/science', methods=['GET', 'POST'])
def science_news():
    titles_sc, news_text_sc = search_news('https://lenta.ru/rubrics/science/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_sc[:20]:
        if t not in science_lst:
            news = ScienceNews()
            news.title = t
            news.content = news_text_sc[titles_sc.index(t)]
            news.is_private = False
            current_user.science_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
    return redirect('/')


@app.route('/news/culture', methods=['GET', 'POST'])
def culture_news():
    titles_cu, news_text_cu = search_news('https://lenta.ru/rubrics/culture/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_cu[:20]:
        if t not in science_lst:
            news = CultureNews()
            news.title = t
            news.content = news_text_cu[titles_cu.index(t)]
            news.is_private = False
            current_user.culture_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
    return redirect('/')


@app.route('/news/foreign_news', methods=['GET', 'POST'])
def foreign_news():
    titles_fr, news_text_fr = search_news('https://lenta.ru/rubrics/world/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_fr[:20]:
        if t not in science_lst:
            news = ForeignNews()
            news.title = t
            news.content = news_text_fr[titles_fr.index(t)]
            news.is_private = False
            current_user.foreign_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
    return redirect('/')

@app.route('/news/CIS_news', methods=['GET', 'POST'])
def cis_news():
    titles_us, news_text_us = search_news('https://lenta.ru/rubrics/ussr/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_us[:20]:
        if t not in science_lst:
            news = CISNews()
            news.title = t
            news.content = news_text_us[titles_us.index(t)]
            news.is_private = False
            current_user.cis_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
    return redirect('/')


@app.route('/news/travel', methods=['GET', 'POST'])
def travel_news():
    titles_tr, news_text_tr = search_news('https://lenta.ru/rubrics/travel/', 'card-mini _longgrid', 'a')
    db_sess = db_session.create_session()
    for t in titles_tr[:20]:
        if t not in science_lst:
            news = CultureNews()
            news.title = t
            news.content = news_text_tr[titles_tr.index(t)]
            news.is_private = False
            current_user.travel_news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news(addCategory=None):
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости', addCategory=addCategory,
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    db_sess.commit()
    app.register_blueprint(news_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
