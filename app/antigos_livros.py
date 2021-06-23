# https://flask.palletsprojects.com/en/1.1.x/cli/  # para ter acesso ao flask shell precisamos
# passar pra ele qual o nome da aplicação usando o FLASK_APP=nomeaplicacao e depois dar o flask shell para abrir o cli
#
#
# @livros.template_filter('to_date')
# def formataDatetime(value):
#     # if fmt:
#     return value.strftime("%d/%m/%Y")
# else:
#     return datetime.strftime()


@livros.route('/relatorio', methods=['GET'])
def relatorio():
    pdf = canvas.Canvas('teste.pdf')  # nome do documento
    pdf.setTitle('Python Flask Relatorio')  # titulo do documento
    pdf.drawString(270, 770, 'Relatorio Livros')  # titulo escrito na linha no pdf
    pdf.save()  # salvar o arquivo


@livros.route('/listarEmprestimo', methods=['GET'])
@login_required
def listarEmprestimo():
    # emprestimo =
    # print(emprestimo.user.nome)
    livros = Livros.query.all()
    usuario = User.query.all()

    grafico_pizza = pygal.Pie()
    grafico_pizza.title = 'Emprestimo'

    for linhas in Emprestimo.query.all():
        print("{} | {} | {}".format(linhas.Livros.titulo, linhas.user.nome, linhas.user.id))
        # if linhas.user.nome:
        # if
        grafico_pizza.add(linhas.Livros.titulo, linhas.user.id)

    return render_template('emprestimo.html', emprestimo=Emprestimo.query.all(), livro=livros, usuarios=usuario,
                           grafico=grafico_pizza.render_data_uri())


@livros.route('/alterarEmprestimo', methods=["GET", "POST"])
@login_required
def alterarEmprestimo():
    if request.method == "POST":
        emprestimo = Emprestimo.query.get(request.form.get('id'))
        emprestimo.usuario_id = request.form['nomeUsuario']
        emprestimo.livro_id = request.form['titulo']
        emprestimo.dataDevolucao = request.form['dataDevolucao']

        data_formulario = datetime.strftime(
            datetime.strptime(emprestimo.dataDevolucao if emprestimo.dataDevolucao != None else '0000-00-00 00:00:00',
                              '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        data_atual = datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S')

        print(data_atual, data_formulario)

        if data_formulario < data_atual:
            flash("Voce ja fechou o emprestimo")
            return redirect(url_for('listarEmprestimo'))
        elif data_formulario is None:
            db.session.commit()
            flash('Emprestimo alterado com sucesso')
            return redirect(url_for('listarEmprestimo'))
        else:
            db.session.commit()
            flash('Emprestimo alterado com sucesso')
            return redirect(url_for('listarEmprestimo'))


@livros.route('/inserirEmprestimo', methods=["POST"])
@login_required
def inserirEmprestimo():
    if request.method == "POST":
        livro = request.form['titulo']
        usuario = request.form['nomeUsuario']
        emprestimo = Emprestimo(usuario, livro)
        db.session.add(emprestimo)
        db.session.commit()
        flash('Emprestimo inserido com sucesso!!!')
        return redirect(url_for('listarEmprestimo'))


def gera(VideoCamera):
    while True:
        frame = VideoCamera.get_frame()
        # encodeImage, flag = cv2.imencode('.jpg', frame)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@livros.route('/streamHtml', methods=["GET"])
def stream():
    return render_template("testeStream.html")


@livros.route('/transmite')
def transmite():
    return Response(stream_with_context(gera(Camera())), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(gera(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@livros.route("/get_ip", methods=["GET"])
def pegar_ip():
    print("IP {}".format(request.remote_addr))
    return "200 OK"


if __name__ == '__main__':
    # livros.run(debug=True, host='192.168.0.9', port=59000)
    livros.run(debug=True, host='', port=59000)
    # threads = list()
    # for index in range(1000):
    #     # logging.info("Main: criando e iniciando thread {}".format(index))
    #     x = threading.Thread(target=t, args=(index,))
    #     threads.append(x)
    #     x.start()

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://teste:123@mudar@localhost:3306/atividades"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
#
#
# class Pessoa(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(20))
#     animais = db.relationship('Animais', backref='dono')
#
#
# class Animais(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(20))
#     dono_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))
#
#
# db.drop_all()
# db.create_all()
#
# @app.route('/')
# def Index():
#     # joao = Pessoa(nome='Joao')
#     # db.session.add(joao)
#     # db.session.commit()
#     # print(joao)
#     # lucas = Pessoa(nome='Lucas')
#     # db.session.add(lucas)
#     # animais = Animais(nome='Calango', dono=lucas)
#     # db.session.add(animais)
#     # lucasQ = Pessoa.query.filter_by(nome='Lucas').first()
#     # print(lucasQ.animais[0].nome)
#     lucasQ = Pessoa.query.order_by(Pessoa.nome).all()  # trazer todos os registros
#     for lista in lucasQ:
#         print("{} | {} | {} | {}".format(lista.nome, lista.id, lista.animais[0].nome, lista.animais[0].id)) # iterar em cima da lista
#     # db.session.commit()
#
#     # dados = Livros.query.order_by(Livros.titulo).all()
#
#
# if __name__ == '__main__':
#     app.run(debug=True)