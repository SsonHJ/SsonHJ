# -*- coding: utf-8 -*-
from flask import request, redirect, url_for,\
    render_template
from apps import app
from models import Article
#from models import Comment
from apps import db

from flask import flash
from sqlalchemy import desc


@app.route('/', methods=['GET'])
def article_list():
    context = {}

    context['article_list'] = Article.query.order_by(
        desc(Article.date_created)).all()
    return render_template('home.html', context=context, active_tab='timeline')


#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# @article controller

@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if request.method == 'GET':
        return render_template('article/create.html', active_tab='article_create')
    elif request.method == 'POST':
        article_data = request.form

        article = Article(
            title=article_data['title'],
            author=article_data['author'],
            category=article_data['category'],
            content=article_data['content']
        )

        db.session.add(article)

        db.session.commit()

        flash(u'게시글을 작성하였습니다.', 'success')
        return redirect(url_for('article_list'))


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    return render_template('article/detail.html')


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    if request.method == 'GET':
        return render_template('article/update.html')
    elif request.method == 'POST':
        return redirect(url_for('article_detail', id=id))


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/delete.html')
    elif request.method == 'POST':
        return redirect(url_for('article_list'))


@app.route('/comment/create/<int:article_id>', methods=['POST'])
def comment_create(article_id):
    if request.method == 'GET':
        return render_template('comment/create.html')
    elif request.method == 'POST':
        return redirect(url_for('article_detail', id=article_id))
