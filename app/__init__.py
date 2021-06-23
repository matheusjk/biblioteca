from flask import Flask, render_template, redirect, request, url_for, flash, Response, stream_with_context, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from reportlab.pdfgen import canvas
from datetime import datetime
from sqlalchemy.sql import func
from flask_mail import Mail, Message
# import pygal
# import cv2
# import base64
# from VideoCamera import Camera

# from flas
import time
import threading

app = Flask(__name__)

app.config.from_object("config")


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


mail = Mail(app)

from app.livros.routes import livros
from app.autor.routes import autor
from app.login.routes import login

app.register_blueprint(livros)
app.register_blueprint(autor)
app.register_blueprint(login)


from app.models.tables import User

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

# ele irá até o endpoint do login a partir dai será redirecionado p/ page de login

