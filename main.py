from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime, timedelta
import pandas as pd
from pandas_datareader import data as web
import numpy as np
from OptimizerPortfolio import BuscarCotacao
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "1234abcd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

dfAssets = pd.read_csv("C:/Users/gamac/Desktop/Projects/static/acoes.csv")

ativosList = dfAssets["Ativo"].values.tolist()

@app.route('/')
def home():
    return render_template("index.html", dfAtivos=ativosList)

@app.route('/sobre')
def sobre():
    return render_template("sobre.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            print(found_user.name)
        else:
            usr = users(user, "test@test.com")
            db.session.add(usr)
            db.session.commit()

        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Você foi desconectado, {user}", "info")
        session.pop("user", None)
        return redirect(url_for("login"))

@app.route('/viewAllUsers')
def viewAllUsers():
    return render_template("viewusers.html", values=users.query.all())

@app.route('/ConsultarAtivos', methods=['POST'])
def ConsultarAtivos():

    print("Consultando ativos")
    # Recuperar request JSON
    portfolio = request.json['data']
    #portfolio = request.get_json()

    # Transformar JSON em Dataframe e renomear as colunas
    dfPortifolio = pd.DataFrame.from_dict(portfolio, orient='columns')
    dfPortifolio.columns = ['Ativo', 'Porcentagem']
    # Transformar coluna Ativo e Porcentagem em listas
    assets = dfPortifolio["Ativo"].values.tolist()
    porc = dfPortifolio["Porcentagem"].values.tolist()
    #Converter lista porc em float
    porc = list(map(float, porc))
    weights = np.array(porc)

    # Get the stock / portfolio starting date
    stockStartDate = datetime.now() - timedelta(days=365)
    # Get the stocks ending date
    today = datetime.today().strftime('%Y-%m-%d')

    # Create a dataframe to store the adjusted close price of the stock
    df = pd.DataFrame()

    # Store the adjusted close price of the stock into the df
    for stock in assets:
        df[stock] = web.DataReader(stock+".SA", data_source='yahoo', start=stockStartDate, end=today)['Adj Close']

    # Show the daily sample return
    returns = df.pct_change()

    # Create and show the annualized covariance matrix
    cov_matrix_annual = returns.cov() * 252

    # Calculate the portfolio variance
    port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))

    # Calculate the portfolio volatility also know as standard deviation
    port_volatility = np.sqrt(port_variance)

    # Calculate the annual portfolio return
    portfolioSimpleAnnualReturn = np.sum(returns.mean() * weights) * 252

    # Show the expected annual return, volatility (risk) and variance
    percent_var = str(round(port_variance, 2) * 100) + '%'
    percent_vols = str(round(port_volatility, 2) * 100) + '%'
    percent_ret = str(round(portfolioSimpleAnnualReturn, 2) * 100) + '%'

    #utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    resp = "<h3>Avaliação do seu portfólio</h1><p>Retorno Anual Esperado: "+percent_ret+"</p>" + "<p>Volatilidade Anual: "+percent_vols+"</p>" + "<p>Variância Anual: "+percent_var+"</p>"

    return resp

@app.route('/Otimizacao', methods=['POST'])
def Otimizacao():

    print("Otimizando Portfolio")
    # Recuperar request JSON
    portfolio = request.json['data']
    valor = request.json['valor']
    resp = BuscarCotacao(portfolio, valor)
    return resp


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)