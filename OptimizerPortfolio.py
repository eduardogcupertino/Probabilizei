# Importar bibliotérica
from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

def BuscarCotacao(portfolio, valor):
    df = pd.DataFrame()

    valor = int(valor)

    print("Portfolio:", portfolio)
    print("VAlor:", valor)

    # Transformar JSON em Dataframe e renomear as colunas
    dfPortifolio = pd.DataFrame.from_dict(portfolio, orient='columns')
    dfPortifolio.columns = ['Ativo', 'Porcentagem']
    # Transformar coluna Ativo e Porcentagem em listas
    assets = dfPortifolio["Ativo"].values.tolist()
    porc = dfPortifolio["Porcentagem"].values.tolist()
    # Converter lista porc em float
    porc = list(map(float, porc))
    weights = np.array(porc)

    # Get the stock / portfolio starting date
    stockStartDate = datetime.now() - timedelta(days=3650)
    # Get the stocks ending date
    today = datetime.today().strftime('%Y-%m-%d')

    # Store the adjusted close price of the stock into the df
    for stock in assets:
        df[stock] = web.DataReader(stock + ".SA", data_source='yahoo', start=stockStartDate, end=today)['Adj Close']

    # Portifolio Optimization

    #Calculate the expected returns and the annualised sample covariance matrix of asset return
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Opt for max sharpe ratio

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    # ef.portfolio_performance(verbose=True)

    # Get the discrete allocation of each share per stock

    latest_price = get_latest_prices(df)
    weights = cleaned_weights
    da = DiscreteAllocation(weights, latest_price, total_portfolio_value=valor)

    (RetornoAnualEsperado, Volatilidade, SharpeRatio) = ef.portfolio_performance(verbose=True)

    # print college name
    print("Retorno anual: ", RetornoAnualEsperado * 100, "Volatilidade Anual: ", Volatilidade * 100, "Sharpe Ratio: ",
          SharpeRatio * 100)

    (NewWeights) = cleaned_weights

    NovosPesos = "<p>Distribuição das ações: " + str(NewWeights) + "</p>"
    RetornoAnualEsperado = "<p>Retorno Anual Esperado: " + str(RetornoAnualEsperado * 100) + "</p>"
    Vol = "<p>Volatilidade Anual: " + str(Volatilidade * 100) + "</p>"
    Sharpe = "<p>Sharpe Ratio: " + str(SharpeRatio) + "</p>"

    allocation, leftover = da.lp_portfolio()
    resp = '<h5>Resultado da otimização do seu portfólio</h5>' + NovosPesos + RetornoAnualEsperado + Vol + Sharpe +\
           '<p>Alocação em cada ação: ' + str(allocation) + '</p>'  \
            '<p> Dinheiro restante: R$ {:.2f}'.format(leftover) + '</p>'

    return resp