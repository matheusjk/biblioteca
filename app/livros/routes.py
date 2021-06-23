from app import login_user, render_template, redirect, url_for, login_required, current_user, request, logout_user, login_manager, Mail, Message, generate_password_hash, flash, Blueprint
# from app.livros.forms import LivrosForms
from app.models.tables import db, Livros, Autor


livros = Blueprint("livros", __name__, template_folder="templates", url_prefix="/livros")


@livros.route('/home', methods=["GET"])
@login_required
def home():
    return render_template('logado.html')


@livros.route('/')
@login_required
def index():
    # dados = Livros.query.get(1).autor
    # dados = Livros.query.order_by(Livros.titulo).all()
    # dados = Livros.query.all()
    # dados = Livros.autores
    # dados = Livros.query.get(1)
    # dados = Livros.query.options(joinedload('editora'))
    # for linha in dados:
    #     print(linha)
    # dados = Livros.query.filter_by(anoPublicacao=2014).first()
    # print(dados.titulo)
    # return render_template('livros.html', livros=dados)

    # autor = Autor(nome="Rafael Seabra", profissao='Professor', email='rafael@gmail.com', endereco='Rua teste 123')
    # db.session.add(autor)
    #
    # #
    # l = Livros(titulo="Quero ficar rico", anoPublicacao=2015, numeroPagina=309, isbn='978-85-452-0122-10', escritor=autor)
    # db.session.add(l)
    # db.session.commit()
    # #
    #
    # # editora = Editora(nome='Gente', endereco='Rua da gente como gente', telefone='2093012932', email='gente@gmail.com' , site='gente@gente.com', cep='2039201', editora=l)
    # # db.session.add(editora)
    #
    # db.session.commit()
    # livros = Livros.query.order_by(Livros.id).all()  # trazer todos os registros
    # livros = Livros.query.order_by(Livros.autor).all()
    livros = Livros.query.all()
    # autor = Autor.query.all()
    # autores = Autor.query.all()
    # print(livros.anoPublicacao)
    # print(autor.nome)
    for lista in livros:
        print("{} | {} | {}".format(lista.titulo, lista.id, lista.escritor.email))  # iterar em cima da lista
    # print(livros.numeroPagina)
    autores = Autor.query.all()
    # print(autores[0])
    # for lista in autores:
    #     print("{} | {} | {} | {} | {}".format(lista.autor.titulo, lista.id, lista.nome, lista.autor.anoPublicacao,
    #                                           lista.autor.numeroPagina))

    return render_template('livros.html', livros=livros, autores=autores)

@livros.route('/inserir', methods=["POST"])
@login_required
def inserir():
    if request.method == "POST":
        titulo = request.form["titulo"]
        anoPublicacao = request.form["anoPublicacao"]
        numeroPagina = request.form["numeroPagina"]
        isbn = request.form["isbn"]
        autor = request.form["autor"]
        # editora = request.form["editora"]

        livros = Livros(titulo=titulo, anoPublicacao=anoPublicacao, numeroPagina=numeroPagina, isbn=isbn,
                        autor_id=autor)
        db.session.add(livros)
        db.session.commit()
        flash('Livros adicionados com sucesso')
        return redirect(url_for('livros.index'))


@livros.route('/alterar', methods=["GET", "POST"])
@login_required
def alterar():
    if request.method == "POST":
        livros = Livros.query.get(request.form.get('id'))
        livros.titulo = request.form["titulo"]
        livros.anoPublicacao = request.form["anoPublicacao"]
        livros.numeroPagina = request.form["numeroPagina"]
        livros.isbn = request.form["isbn"]
        livros.autor_id = request.form["autor"]
        # livros.editora = request.method["editora"]

        db.session.commit()
        flash('Livros alterados com sucesso')
        return redirect(url_for('livros.index'))


@livros.route('/deletar/<int:id>', methods=["GET"])
@login_required
def deletar(id):
    livros = Livros.query.get(id)
    # livros = Livros.query.filter_by(id=id).first()
    db.session.delete(livros)
    db.session.commit()
    flash("Livro excluido com sucesso!!!")
    return redirect(url_for('livros.index'))