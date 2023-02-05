from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show

@app.route ('/create')
def create():
    return render_template('create.html')

@app.route ('/user/create', methods = ['POST'])
def user_create():
    if not Show.validate_register(request.form):
        return redirect ('/create')

    data={
        'title': request.form ['title'],
        'network': request.form ['network'],
        'description': request.form ['description'],
        'release_date': request.form['release_date'],
        'user_id':session ['user_id']
    }
    Show.create(data)
    return redirect ('/dashboard')

@app.route('/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Show.destroy(data)
    return redirect('/dashboard')

@app.route('/details/<int:id>')
def details(id):
    data ={
        'id': id
    }
    return render_template ('details.html', show=Show.get_description(data))

@app.route('/edit/<int:id>')
def update(id):
    data={
        'id': id
    }
    return render_template ('edit.html', show=Show.get_one(data))

@app.route('/update/<int:id>', methods=['POST'])
def edit(id):
    if not Show.validate_register(request.form):
        return redirect (f'/edit/{id}')
    data={
        'id': id,
        'title': request.form ['title'],
        'network': request.form ['network'],
        'description': request.form ['description'],
        'release_date': request.form['release_date']
    }
    Show.update(data)
    return redirect ('/dashboard')