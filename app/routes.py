# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request, session, url_for, redirect
import requests
from app.forms import LoginForm
from config import GET_BOOKS_URL, AUTH_URL
from http import HTTPStatus


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
        if response.status_code == HTTPStatus.OK:
            session['session'] = response.cookies.get('session')
            return redirect(url_for('index'))
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            return str(response.json())
        else:
            print(response)
            return 'Oops!'
    return render_template('index.html', title='Mybook test page', form=form)


def get_books(cookies):
    api_response = requests.get(
        GET_BOOKS_URL,
        cookies=cookies,
        headers={'Accept': 'application/json; version=5'},
    )
    if api_response.status_code == HTTPStatus.UNAUTHORIZED:
        session.delete('session')
        return redirect(url_for('index'))
    if api_response.status_code != HTTPStatus.OK:
        return 'Something went wrong. Please try later.'
    return api_response


def get_personal_library(books):
    lib = [
        {
            'book_name': book.get('book').get('name'),
            'book_cover': book.get('book').get('default_cover'),
            'author': book.get('book').get('main_author').get('cover_name'),
        }
        for book in books if book.get('book') is not None
    ]
    return lib
