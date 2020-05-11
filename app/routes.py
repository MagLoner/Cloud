# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for,request
from app.forms import LoginForm,RegistrationForm
from app import app,db,cors
from werkzeug.urls import url_parse
from flask_login import current_user, login_user,logout_user, login_required
from app.models import User
from flask_cors import cross_origin
@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template("index.html", title='Home Page')

@app.route('/deepArt')
@cross_origin(origin='*',headers=['Access-Control-Allow-Origin: *'])
def deepArt():
    return render_template("deepArt.html", title='Filters')

'''methods -сообщения для Flask, что эта функция просмотра принимает запросы GET и POST,
переопределяя значение по умолчанию, которое должно принимать только запросы GET.
form.validate_on_submit() выполняет всю обработку формы
edirect() - указывает веб-браузеру клиента автоматически перейти на другую страницу, указанную в качестве аргумента
 flash(), Flask сохраняет сообщение, но на веб-страницах не будут появляться магические сообщения.
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Добро пожаловать, вы успешно зарегестрировались. Войдите в систему')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Замечательный сайт!'},
        {'author': user, 'body': '???Но я не отправлял данные сообщения...???'},
        {'author': user, 'body': 'Кажется моими данными управляют...'}
    ]
    return render_template('user.html', user=user, posts=posts)