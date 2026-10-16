from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine
from models import Book, User

app = Flask(__name__)
Base.metadata.create_all(engine)


@app.route('/')
def index():
    with Session(engine) as session:
        statement = select(User).order_by(User.nome)
        usuarios = session.scalars(statement).all()
        statement2 = select(Book).order_by(Book.titulo)
        livros = session.scalars(statement2).all()
    return render_template('index.html', usuarios=usuarios, livros=livros)


@app.route('/usuario/novo', methods=['POST', 'GET'])
def form_usuario():
    if request.method == 'POST':
        usuario = User(
            nome=request.form.get('nome'),
            email=request.form.get('email')
        )
        with Session(engine) as session:
            session.add(usuario)
            session.commit()
        return redirect(url_for('index' ))
    return render_template('form_usuario.html')


@app.route('/livros/novo', methods=['GET', 'POST'])
def form_livro():
    if request.method == 'POST':
        livro = Book(
            titulo=request.form.get('titulo'),
            user_id=(request.form.get('id_user'))
        )
        with Session(engine) as session:
            session.add(livro)
            session.commit()
        return redirect(url_for('index'))   
    return render_template('form_livro.html')
        
if __name__ == "__main__":
    app.run(debug=True)