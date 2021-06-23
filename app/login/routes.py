from app import login_user, render_template, redirect, url_for, login_required, current_user, request, logout_user, login_manager, Mail, Message, generate_password_hash, flash, Blueprint
from app.login.forms import LoginForm, Usuario, CadastroUsuario, Recuperar
from app.models.tables import db, User
import random
import string

login = Blueprint('login', __name__, template_folder='templates', url_prefix='/login')

login_manager.login_view = "login.verificaLogin"
login_manager.login_message = "Por favor se autenticar antes de acessar o sistema!!!"
login_manager.login_message_category = "info"
login_manager.refresh_view = "login.index"
login_manager.needs_refresh_message = (u"Para proteger sua conta, por favor reautentique para acessar a pagina")
login_manager.needs_refresh_message_category = "info"


@login.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    forms = Recuperar()
    if forms.validate_on_submit():
        print(forms.email.data)
        email = Usuario.query.filter_by(email=forms.email.data).first()
        

@login.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = User(nome, email, senha)
        db.session.add(user)
        db.session.commit()
        # return redirect(url_for('register'))
    return render_template('register.html')


@login.route('/login', methods=["GET", "POST"])
def verificaLogin():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verifica_senha(
                senha):  # verificando se o usuario nao existir e nao tiver senha redireciona para a tela de login senao efetua o login
            flash('Verifique email ou senha!!!')
            return redirect(url_for('login.verificaLogin'))

        # if current_user.is_authenticated:
        #     login_user(user, remember=True)
        #     return redirect(url_for('listar'))
        # else:
        #     login_user(None)
        login_user(user, remember=True)
        return redirect(url_for('livros.index'))

    return render_template('login.html')


@login.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.verificaLogin'))