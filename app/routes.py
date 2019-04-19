# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request, jsonify
import requests
from app.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        print("Posted data : {}".format(request.form))
        response = requests.post('https://mybook.ru/api/auth/', json={'email': request.form.get('email'), 'password': request.form.get('password')})
        print(response)
        return 'Logging in!'
    return render_template('index.html', title='Mybook mirror', form=form)
