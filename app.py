from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import Users
from db import db
import hashlib

app = Flask(__name__)
app.secret_key = 'MoritzZimmerman'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Users).filter_by(id=id).first()
    return usuario


@app.route('/', methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        nome = request.form["nomeForm"]
        senha = request.form["senhaForm"]


        novo_usuario = Users(nome=nome, senha=hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)




        return redirect(url_for("home"))
    

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        user = db.session.query(Users).filter_by(nome=nome, senha=hash(senha)).first()
        if not user:
            return "Usuario não autorizado. Nome ou senha incorretos"
        
        login_user(user)
        return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)