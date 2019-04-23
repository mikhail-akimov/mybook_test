# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request, session, url_for, redirect
import requests
from app.forms import LoginForm

GET_BOOKS_URL = 'https://mybook.ru/api/bookuserlist/'
AUTH_URL = 'https://mybook.ru/api/auth/'


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('session'):
        cookies = {'session': session['session']}
        books = get_books(cookies).json()['objects']
        lib = get_personal_library(books)
        return render_template(
            'index.html',
            title='My books from Mybook',
            books=lib,
        )
    form = LoginForm()
    if form.validate_on_submit():
        response = requests.post(AUTH_URL,
                                 json={
                                     'email': request.form.get('email'),
                                     'password': request.form.get('password'),
                                 }
                                 )
        if response.status_code == 200:
            session['session'] = response.cookies.get('session')
            print(session['session'])
            return redirect(url_for('index'))
        elif response.status_code == 400:
            return str(response.json())
        else:
            print(response)
            return 'Oops!'
    return render_template('index.html', title='Mybook test page', form=form)


def get_books(cookies):
    headers = {'Accept': 'application/json; version=5'}
    api_response = requests.get(
        GET_BOOKS_URL,
        cookies=cookies,
        headers=headers,
    )
    return api_response


def get_personal_library(books):
    lib = []
    for book in books:
        item = {
            'book_name': book['book']['name'],
            'book_cover': book['book']['default_cover'],
            'author': book['book']['main_author']['cover_name'],
        }
        lib.append(item)
    return lib