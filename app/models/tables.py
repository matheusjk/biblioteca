from app import db, login_manager, generate_password_hash, check_password_hash, func, UserMixin, datetime, backref


class Autor(UserMixin, db.Model):
    # __tablename__ = 'autores'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    profissao = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    livro = db.relationship('Livros', backref=backref('escritor',
                                                      passive_deletes=True))  # passive_deletes=True) #cascade="save-update, merge, delete")

    # def __init__(self, nome, profissao, email, endereco, autor):
    #     self.nome = nome
    #     self.profissao = profissao
    #     self.email = email
    #     self.endereco = endereco
    #     self.autor = autor


# class Editora(db.Model):
#     # __tablename__ = 'editoras'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     endereco = db.Column(db.String(100), nullable=False)
#     telefone = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     site = db.Column(db.String(100), nullable=False)
#     cep = db.Column(db.String(11), nullable=False)
#     editoraTable_id = db.Column(db.Integer, db.ForeignKey('livros.id'))

# def __init__(self, nome, endereco, telefone, email, site, cep, editora):
#     self.nome = nome
#     self.endereco = endereco
#     self.telefone = telefone
#     self.email = email
#     self.site = site
#     self.cep = cep
#     self.editora = editora


class Livros(UserMixin, db.Model):
    # __tablename__ = 'livros'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    anoPublicacao = db.Column(db.Integer, nullable=False)
    numeroPagina = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id', ondelete="NO ACTION", onupdate="CASCADE"),
                         nullable=False)  # , uselist=True)  # nome da chave estrangeira(FK) no banco
    # editora = db.relationship('Editora', backref='editoraTable')  # nome da chave estrangeira(FK) no banco
    emprestimoLivro = db.relationship('Emprestimo', backref='Livros', uselist=False)

    #
    # def __init__(self, titulo, anoPublicacao, numeroPagina, isbn):
    #     self.titulo = titulo
    #     self.anoPublicacao = anoPublicacao
    #     self.numeroPagina = numeroPagina
    #     self.isbn = isbn


class Emprestimo(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    dataEmprestimo = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    dataDevolucao = db.Column(db.DateTime, default=None, onupdate=datetime.now)

    # datetime.strftime(datetime.today())

    def __init__(self, usuario_id, livro_id):
        self.usuario_id = usuario_id
        self.livro_id = livro_id



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    emprestimo = db.relationship('Emprestimo', backref='user', uselist=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)

    def verifica_senha(self, senhaTemp):
        return check_password_hash(self.senha, senhaTemp)

    # @login_manager.unauthorized_handler
    # def redireciona(self):
    #     return redirect(url_for('login'))


# db.drop_all()  # dropa as tabelas
# db.create_all()  # para criar de vez todas as modificações no banco,ou seja espelhar as classes no banco