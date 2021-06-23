from app import login_user, render_template, redirect, url_for, login_required, current_user, request, logout_user, login_manager, Mail, Message, generate_password_hash, flash, Blueprint
# from app.autor.forms import AutoresForm
from app.models.tables import db, Autor, Livros

autor = Blueprint("autor", __name__, template_folder="templates", url_prefix="/autor")


@autor.route('/listarAutores', methods=['GET'])
@login_required
def listar():
    if current_user.is_authenticated:
        autores = Autor.query.all()
        return render_template('autores.html', autores=autores)
    return redirect(url_for('login.logout'))


@autor.route('/inserirAutor', methods=["POST"])
@login_required
def inserirAutor():
    if request.method == "POST":
        nome = request.form["nome"]
        profissao = request.form["profissao"]
        email = request.form["email"]
        endereco = request.form["endereco"]
        autor = Autor(nome=nome, profissao=profissao, email=email, endereco=endereco)
        db.session.add(autor)
        db.session.commit()
        flash("Autor adicionado com sucesso!!!")
        return redirect(url_for('autor.listar'))


@autor.route('excluirAutor/<int:id>', methods=["GET"])
@login_required
def deletarAutor(id):
    if request.method == "GET":
        livrosChecar = Livros.query.all()
        # print(livrosChecar, livrosChecar[0].autor_id)
        for livros in livrosChecar:
            if livros.autor_id == id:
                flash('Desculpe mas esse autor tem publicacoes em livros', category="info")
                return redirect(url_for("autor.listar"))
            
        autor = Autor.query.get(id)
        db.session.delete(autor)
        db.session.commit()
        flash("Autor deletado com sucesso", category="success")
        return redirect(url_for('autor.listar'))
    else:
        flash("Desculpe erro ao excluir autor", category="warning")
        return redirect(url_for('autor.listar'))


@autor.route('/alterarAutor', methods=['GET', 'POST'])
@login_required
def alterarAutor():
    if request.method == 'POST':
        autores = Autor.query.get(request.form.get('id'))
        autores.nome = request.form['nome']
        autores.profissao = request.form['profissao']
        autores.email = request.form['email']
        autores.endereco = request.form['endereco']

        db.session.commit()
        flash('Autor alterado com sucesso!!!')
        return redirect(url_for('autor.listar'))
