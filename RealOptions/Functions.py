import matplotlib
matplotlib.use('Agg')
import pandas as pd # 1.1.3
import numpy as np  # 1.19.2
import matplotlib.pyplot as plt # 3.3.2
import networkx as nx # 2.5
import sys # 3.8.5
import random #
from scipy.stats import norm # 1.5.2
from tkinter import * #8.6
from tkinter import messagebox
import sys
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
except ImportError:
    import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

def GBM(daily_drift,daily_volatility,initial_stock, periodo):
    # Agora, com o componente aleatório
    variavel_z=[]
    log_return=[]
    preco=[]
    variavel_z.append(norm.ppf(random.random()))
    log_return.append(np.round(daily_drift+(daily_volatility*norm.ppf(random.random()))*100,2)) #porcentage
    preco.append(initial_stock*np.exp(daily_drift+(daily_volatility*norm.ppf(random.random()))))
    for i in periodo[1:]:
        variavel_z.append(norm.ppf(random.random()))
        log_return.append(np.round(daily_drift+(daily_volatility*norm.ppf(random.random()))*100,2)) #porcentage
        preco.append(preco[-1]*np.exp(daily_drift+(daily_volatility*norm.ppf(random.random()))))
    return preco

def Volatilidade(fluxodecaixa):
    if type(fluxodecaixa)!=list:
        print("Você precisa definir uma lista com o fluxo de caixa")
        return 0
    fluxodecaixa=pd.DataFrame(fluxodecaixa)
    retornos=np.log(fluxodecaixa.pct_change().fillna(0)+1).values[1:]
    media_dos_retornos=retornos.mean()
    media_dos_retornos_quadrado=pow(retornos-media_dos_retornos,2)
    soma_do_quadrados=sum(media_dos_retornos_quadrado)
    amostra=len(retornos)-1
    return np.sqrt(soma_do_quadrados/amostra)

def MonteCarloSimulation(annual_drift=0,annual_volatility=0,initial_stock=0, periodo=0,quantidade_simulacao=1000,
                         alpha=0.05, imagem=False, tkWindow=None):
    newWindow = Toplevel(tkWindow)
    newWindow.title("Simulação de Monte Carlo Volatilidade")
    newWindow.geometry("600x700")
    simulations=[]
    periodo=range(1,periodo)
    daily_drift=annual_drift/252
    daily_volatility=annual_volatility/np.sqrt(252)
    mean_drift=daily_drift-pow((0.5*daily_volatility),2) # retorno
    figura = plt.figure(figsize=(10,10))
    for _ in range(quantidade_simulacao):
        valor=GBM(daily_drift,daily_volatility,initial_stock, periodo)
        for i in valor:
            simulations.append(i)
        if imagem:
            plt.plot(periodo,valor)
            plt.xlabel("Período")
            plt.ylabel("Preços")
    canvas =  FigureCanvasTkAgg(figura, newWindow)  # A tk.DrawingArea.
    canvas.draw() 
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
    toolbar = NavigationToolbar2Tk(canvas, newWindow)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
    #canvas.mpl_connect("key_press_event", on_key_press)
    #plt.show()
    alpha=alpha/2
    text = Label(newWindow,bg="white", text="Preço "+str((alpha+0)*100)+"% quartil ="+str(np.round(np.percentile(simulations,(alpha+0)*100),2)))
    text.place(x=0,y=1)
    text = Label(newWindow,bg="white", text="Preço "+str((1-alpha)*100)+"% quartil ="+str(np.round(np.percentile(simulations,(1-alpha)*100))))
    text.place(x=0,y=20)
    text = Label(newWindow,bg="white", text="Valor Esperado ="+str(np.round(np.mean(simulations),2)))
    text.place(x=0,y=40)
    text = Label(newWindow,bg="white", text="Volatilidade ="+str(np.round(np.std(simulations),2)))
    text.place(x=0,y=60)
    text = Label(newWindow,bg="white", text="Intervalo de Confiança:"+str(((1-alpha)*100)-((alpha+0)*100)))
    text.place(x=0,y=80)
    #return simulations
    
def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)
    
def PlotBinomialValue(tab,tkWindow, nome, dimensao,T):
    newWindow = Toplevel(tkWindow)
    newWindow.title(nome)
    newWindow.geometry(dimensao)
    figura = plt.figure(figsize=(12,12))
    G=nx.Graph() 
    n=T
    for i in range(0,n+1):     
        for j in range(1,i+2):         
            if i<n:
                G.add_edge((i,j),(i+1,j))
                G.add_edge((i,j),(i+1,j+1)) 
    posG={}    #dictionary with nodes position 
    for node in G.nodes():    
        posG[node]=(node[0],n+2+node[0]-2*node[1]) 
    nx.draw(G,pos=posG, with_labels = False)
    # some math labels
    referencia=[]
    for i in G.nodes():
        referencia.append(i)
    posicao=0
    labels={}
    for i in range(n+1):
        for j in range(n+1):
            if i>=j:
                labels[referencia[posicao]] = tab.iloc[j,i]
                posicao+=1
    nx.draw_networkx_labels(G, posG, labels, font_size=12, font_color="black")
    plt.axis("off")
    #plt.savefig(nome+'.png', dpi=dpi)
    #plt.show()
    canvas = FigureCanvasTkAgg(figura, newWindow)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, newWindow)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect("key_press_event", on_key_press)
    
def binomial_model_abandono(T, S0, sigma, rf, K, nome="teste", dpi=600, imagem=False, tkWindow=None):
    global df
    global df1
    """
    T = number of binomial iterations
    S0 = initial stock price
    sigma = factor change of upstate
    rf = risk free interest rate per annum
    K = exercise price
    """
    dt=1
    u=np.exp(sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    d = np.exp(-sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    p = (np.exp(rf*dt)-d) / (u - d)
    q = 1 - p
    # make asset price tree
    asset=np.zeros([T + 1, T + 1])
    for i in range(T + 1):
        for j in range(i + 1):
            if i==j:
                asset[j, i] = np.round(S0*pow(u,0)*pow(d,i),2)
            if j==0:
                asset[j, i] = np.round(S0*pow(u,i)*pow(d,j),2)
            else:
                asset[j, i] = np.round(S0*pow(u,i-j)*pow(d,j),2)
    # calcular o preço da opção, baseado no artigo original
    option = np.zeros([T + 1, T + 1])
    # artigo original
    #option[:, T] = np.maximum(np.zeros(T + 1), (asset[:, T] - K))
    # livro de real options - opções americanas
    #option[:, T] = np.maximum(K, (asset[:, T]))
    option[:, T] = np.maximum(K, (asset[:, T]))
    # artigo original
    #p=(rf-d)/(u-d)
    #print(p)
    #livro de real options - opções americanas
    p=((np.exp(rf*dt))-d)/(u-d)
    #print(p)
    for i in range(T,0,-1):
        for j in range(i):
            #artigo original
            #option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))/rf
            #livro
            valcalculado=((p*option[j,i])+((1-p)*option[j+1,i]))*np.exp(-rf*dt)
            option[j,i-1]=np.max([valcalculado,K])
    if imagem:
        df1=pd.DataFrame(np.round(option,2))
        df=pd.DataFrame(np.round(asset,2))
        PlotBinomialValue(df,tkWindow, "Árvore Bimonial - Valores", "600x600",T)
        PlotBinomialValue(df1,tkWindow, "Árvore Bimonial - Opções", "600x600",T)
        
def binomial_model_expansion(T, S0, sigma, rf, nome="teste", dpi=600, imagem=True, fator_expansao=0, 
                             custo_expansao=0, tkWindow=None):
    """
    T = number of binomial iterations
    S0 = initial stock price
    sigma = factor change of upstate
    rf = risk free interest rate per annum
    K = exercise price
    """
    global df
    global df1
    dt=1
    u=np.exp(sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    d = np.exp(-sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    p = (np.exp(rf*dt)-d) / (u - d)
    q = 1 - p
    # make asset price tree
    asset=np.zeros([T + 1, T + 1])
    for i in range(T + 1):
        for j in range(i + 1):
            if i==j:
                asset[j, i] = np.round(S0*pow(u,0)*pow(d,i),2)
            if j==0:
                asset[j, i] = np.round(S0*pow(u,i)*pow(d,j),2)
            else:
                asset[j, i] = np.round(S0*pow(u,i-j)*pow(d,j),2)
    # calcular o preço da opção, baseado no artigo original
    option = np.zeros([T + 1, T + 1])
    vetor_expansao=(asset[:,-1]*fator_expansao)-custo_expansao
    option = np.zeros([T + 1, T + 1])
    option[:, T] = np.maximum(vetor_expansao, (asset[:, T]))
    # artigo original
    #p=(rf-d)/(u-d)
    #print(p)
    #livro de real options - opções americanas
    p=((np.exp(rf*dt))-d)/(u-d)
    #print(p)
    for i in range(T,0,-1):
        for j in range(i):
            #artigo original
            #option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))/rf
            #livro
            option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))*np.exp(-rf*dt)
    if imagem:
        df1=pd.DataFrame(np.round(option,2))
        df=pd.DataFrame(np.round(asset,2))
        PlotBinomialValue(df,tkWindow, "Árvore Bimonial - Valores", "600x600",T)
        PlotBinomialValue(df1,tkWindow, "Árvore Bimonial - Opções", "600x600",T)

def binomial_model_contraction(T, S0, sigma, rf, nome="teste", dpi=600, imagem=True, fator_contracao=0, 
                               economia_contracao=0, tkWindow=None):
    """
    T = number of binomial iterations
    S0 = initial stock price
    sigma = factor change of upstate
    rf = risk free interest rate per annum
    K = exercise price
    """
    global df
    global df1
    dt=1
    u=np.exp(sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    d = np.exp(-sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    p = (np.exp(rf*dt)-d) / (u - d)
    q = 1 - p
    # make asset price tree
    asset=np.zeros([T + 1, T + 1])
    for i in range(T + 1):
        for j in range(i + 1):
            if i==j:
                asset[j, i] = np.round(S0*pow(u,0)*pow(d,i),2)
            if j==0:
                asset[j, i] = np.round(S0*pow(u,i)*pow(d,j),2)
            else:
                asset[j, i] = np.round(S0*pow(u,i-j)*pow(d,j),2)
    # calcular o preço da opção, baseado no artigo original
    option = np.zeros([T + 1, T + 1])
    vetor_expansao=(asset[:,-1]*fator_contracao)+economia_contracao
    option = np.zeros([T + 1, T + 1])
    option[:, T] = np.maximum(vetor_expansao, (asset[:, T]))
    # artigo original
    #p=(rf-d)/(u-d)
    #print(p)
    #livro de real options - opções americanas
    p=((np.exp(rf*dt))-d)/(u-d)
    #print(p)
    for i in range(T,0,-1):
        for j in range(i):
            #artigo original
            #option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))/rf
            #livro
            option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))*np.exp(-rf*dt)
    if imagem:
        df1=pd.DataFrame(np.round(option,2))
        df=pd.DataFrame(np.round(asset,2))
        PlotBinomialValue(df,tkWindow, "Árvore Bimonial - Valores", "600x600",T)
        PlotBinomialValue(df1,tkWindow, "Árvore Bimonial - Opções", "600x600",T)

def binomial_model_compounds(T, S0, sigma, rf, custos, nome="teste", dpi=600, imagem=False, tkWindow=None):
    """
    T = number of binomial iterations
    S0 = initial stock price
    sigma = factor change of upstate
    rf = risk free interest rate per annum
    K = exercise price
    """
    global df
    global df1
    dt=1
    u=np.exp(sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    d = np.exp(-sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    p = (np.exp(rf*dt)-d) / (u - d)
    q = 1 - p
    # make asset price tree
    asset=np.zeros([T + 1, T + 1])
    for i in range(T + 1):
        for j in range(i + 1):
            if i==j:
                asset[j, i] = np.round(S0*pow(u,0)*pow(d,i),2)
            if j==0:
                asset[j, i] = np.round(S0*pow(u,i)*pow(d,j),2)
            else:
                asset[j, i] = np.round(S0*pow(u,i-j)*pow(d,j),2)
    # calcular o preço da opção, baseado no artigo original
    option = np.zeros([T + 1, T + 1])
    # artigo original
    tamanho=len(custos)
    for i in range(tamanho):
        if i==0:
            option[:, T] = np.maximum(np.zeros(T + 1), (asset[:, T] - custos[i]))
        else:
            option[:, T] = np.maximum(np.zeros(T + 1), (option[:, T] - custos[i]))
    # livro de real options - opções americanas
    #option[:, T] = np.maximum(K, (asset[:, T]))
    # artigo original
    #p=(rf-d)/(u-d)
    #print(p)
    #livro de real options - opções americanas
    p=((np.exp(rf*dt))-d)/(u-d)
    #print(p)
    for i in range(T,0,-1):
        for j in range(i):
            #artigo original
            #option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))/rf
            #livro
            option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))*np.exp(-rf*dt)
    if imagem:
        df1=pd.DataFrame(np.round(option,2))
        df=pd.DataFrame(np.round(asset,2))
        PlotBinomialValue(df,tkWindow, "Árvore Bimonial - Valores", "600x600",T)
        PlotBinomialValue(df1,tkWindow, "Árvore Bimonial - Opções", "600x600",T)

def binomial_model_dynamicstrikes(T, S0, sigma, rf, custos, nome="teste", dpi=600, imagem=False, tkWindow=None):
    """
    T = number of binomial iterations
    S0 = initial stock price
    sigma = factor change of upstate
    rf = risk free interest rate per annum
    K = exercise price
    """
    global df
    global df1
    dt=1
    u=np.exp(sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    d = np.exp(-sigma*np.sqrt(dt))# deltat aqui será um tempo por vez
    p = (np.exp(rf*dt)-d) / (u - d)
    q = 1 - p
    # make asset price tree
    asset=np.zeros([T + 1, T + 1])
    for i in range(T + 1):
        for j in range(i + 1):
            if i==j:
                asset[j, i] = np.round(S0*pow(u,0)*pow(d,i),2)
            if j==0:
                asset[j, i] = np.round(S0*pow(u,i)*pow(d,j),2)
            else:
                asset[j, i] = np.round(S0*pow(u,i-j)*pow(d,j),2)
    # calcular o preço da opção, baseado no artigo original
    # Cria os preços originais das opções
    option = np.zeros([T + 1, T + 1])
    # artigo original
    option[:, T] = np.maximum(np.zeros(T + 1), (asset[:, T]))
    # livro de real options - opções americanas
    #option[:, T] = np.maximum(K, (asset[:, T]))
    # artigo original
    #p=(rf-d)/(u-d)
    #print(p)
    #livro de real options - opções americanas
    p=((np.exp(rf*dt))-d)/(u-d)
    #print(p)
    for i in range(T,0,-1):
        for j in range(i):
            #artigo original
            #option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))/rf
            #livro
            option[j,i-1]=((p*option[j,i])+((1-p)*option[j+1,i]))*np.exp(-rf*dt)
    # Vamos deduzir os custos do último ano primeiro, todos os outros virão depois
    tamanho=len(custos)
    if tamanho!=T:
        print("Você precisa colocar um custo para cada período apurado, mesmo que em algum ele seja zero")
        return 0,0
    option[:, T] = np.maximum(np.zeros(T + 1), (option[:, T]-custos[-1]))
    # vamor copiar a array original, para poder calcular o valor das opções,
    # tendo o custo do último ano descontado
    option2=option.copy()
    for i in range(T,0,-1):
        for j in range(i):
            option2[j,i-1]=((p*option2[j,i])+((1-p)*option2[j+1,i]))*np.exp(-rf*dt)
    # vamor comparar os três preços:
    # o zero, o valor original da opção e o valor original da opção descontado o seu custo
    # aquele que for maior
    for i in range(tamanho-1):
        for linha in range(option.shape[0]):
            option[linha, i+1] = np.max([0, 
                                            np.array(option[linha, i+1] - custos[i]), 
                                            np.array(option2[linha, i+1])])
    option[0,0]=((p*option[0,1])+((1-p)*option[0+1,1]))*np.exp(-rf*dt)

    if imagem:
        df1=pd.DataFrame(np.round(option,2))
        df=pd.DataFrame(np.round(asset,2))
        PlotBinomialValue(df,tkWindow, "Árvore Bimonial - Valores", "600x600",T)
        PlotBinomialValue(df1,tkWindow, "Árvore Bimonial - Opções", "600x600",T)

#######################################################################
# Copyright (C) 2016 Shijie Huang (harveyh@student.unimelb.edu.au)    #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
from math import log, sqrt, exp
from scipy import stats
from typing import Tuple


class BSMOptionValuation:
    """
    Valuation of European call options in Black-Scholes-Merton Model (incl. dividend)
    Attributes
    ==========
    S0: float
        initial stock/index level
    K: float
        strike price
    T: float
        time to maturity (in year fractions)
    r: float
        constant risk-free short rate
        assume flat term structure
    sigma: float
        volatility factor in diffusion term
    div_yield: float
        dividend_yield, in percentage %, default = 0.0%
    """

    def __init__(self, S0: float, K: float, T: float, r: float, sigma: float, div_yield: float = 0.0):
        assert sigma >= 0, 'volatility cannot be less than zero'
        assert S0 >= 0, 'initial stock price cannot be less than zero'
        assert T >= 0, 'time to maturity cannot be less than zero'
        assert div_yield >= 0, 'dividend yield cannot be less than zero'

        self.S0 = float(S0)
        self.K = float(K)
        self.T = float(T)
        self.r = float(r)
        self.sigma = float(sigma)
        self.div_yield = float(div_yield)

        self.d1 = ((log(self.S0 / self.K) + (self.r - self.div_yield + 0.5 * self.sigma ** 2) * self.T) / (
                self.sigma * sqrt(self.T)))
        self.d2 = self.d1 - self.sigma * sqrt(self.T)

    def call_value(self, observed_put_price: float = None) -> float:
        """
        :return: call option value
        """
        if observed_put_price is None:
            call_value = (self.S0 * exp(-self.div_yield * self.T) * stats.norm.cdf(self.d1, 0.0, 1.0) - self.K * exp(
                -self.r * self.T) * stats.norm.cdf(self.d2, 0.0, 1.0))
        else:
            call_value = observed_put_price + exp(-self.div_yield * self.T) * self.S0 - exp(-self.r * self.T) * self.K

        return call_value

    def delta(self) -> Tuple[float, float]:
        """
        Delta measures the change in the option price for a $1 change in the stock price
        :return: delta of the option
        """
        delta_call = exp(- self.div_yield * self.T) * stats.norm.cdf(self.d1, 0.0, 1.0)
        delta_put = -exp(- self.div_yield * self.T) * stats.norm.cdf(-self.d1, 0.0, 1.0)

        return delta_call, delta_put

    def gamma(self) -> float:
        """
        Gamma measures the change in delta when the stock price changes
        :return: gamma of the option
        """
        gamma = exp(-self.div_yield * self.T) * stats.norm.pdf(self.d1) / (self.S0 * self.sigma * sqrt(self.T))

        return gamma

    def theta(self) -> Tuple[float, float]:
        """
        Theta measures the change in the option price with respect to calendar time (t ),
        holding fixed time to expiration (T).

        If time to expiration is measured in years, theta will be the annualized change in the option value.
        To obtain a per-day theta, divide by 252.
        :return: theta of the option
        """
        part1 = self.div_yield * self.S0 * exp(-self.div_yield * self.T) * stats.norm.cdf(self.d1)
        part2 = self.r * self.K * stats.norm.cdf(self.d2)
        part3 = (self.K * exp(-self.r * self.T) * stats.norm.pdf(self.d2) * self.sigma) / (2 * sqrt(self.T))

        theta_call = part1 - part2 - part3
        theta_put = theta_call + self.r * self.K * exp(-self.r * self.T) - self.div_yield * self.S0 * exp(
            -self.div_yield * self.T)

        return theta_call, theta_put

    def vega(self) -> float:
        """
        Vega measures the change in the option price when volatility changes. Some writers also
        use the terms lambda or kappa to refer to this measure:
        It is common to report vega as the change in the option price per percentage point change
        in the volatility. This requires dividing the vega formula above by 100.
        :return: vega of option
        """
        vega = self.S0 * exp(-self.div_yield * self.T) * stats.norm.pdf(self.d1, 0.0, 1.0) * sqrt(self.T)

        return vega

    def rho(self) -> Tuple[float, float]:
        """
        Returns: call_rho, put_rho
        -------
        Rho is the partial derivative of the option price with respect to the interest rate.
        These expressions for rho assume a change in r of 1.0. We are typically interested in
        evaluating the effect of a change of 0.01 (100 basis points) or 0.0001 (1 basis point). To
        report rho as a change per percentage point in the interest rate, divide this measure by 100.
        To interpret it as a change per basis point, divide by 10,000.
        """
        call_rho = self.T * self.K * exp(-self.r * self.T) * stats.norm.cdf(self.d2)
        put_rho = -self.T * self.K * exp(-self.r * self.T) * stats.norm.cdf(-self.d2)

        return call_rho, put_rho

    def psi(self) -> Tuple[float, float]:
        """
        Returns: call_psi, put psi
        -------
        Psi is the partial derivative of the option price with respect to the continuous dividend yield:
        To interpret psi as a price change per percentage point change in the dividend yield, divide
        by 100.
        """
        call_psi = - self.T * self.S0 * exp(-self.div_yield * self.T) * stats.norm.cdf(self.d1)
        put_psi = self.T * self.S0 * exp(-self.div_yield * self.T) * stats.norm.cdf(-self.d1)

        return call_psi, put_psi

    def implied_vol(self, observed_call_price: float, iteration: int = 1000) -> float:
        """
        Newton-Raphson iterative approach, assuming BSM model

        :param observed_call_price: call price from the market
        :param iteration: no. of iteration
        :return: implied volatility given option price
        """

        for _ in range(iteration):
            self.sigma -= (self.call_value() - observed_call_price) / self.vega()

        return self.sigma

    def put_value(self, observed_call_price: float = None) -> float:
        """
        Use put call parity (incl. continuous dividend) to calculate the put option value

        :return: put option value
        """
        if observed_call_price is None:
            put_value = self.call_value() + exp(-self.r * self.T) * self.K - exp(-self.div_yield * self.T) * self.S0
        else:
            put_value = observed_call_price + exp(-self.r * self.T) * self.K - exp(-self.div_yield * self.T) * self.S0

        return put_value

    def lookback_BSM(self, option_type: str, max_share_price: float, min_share_price: float) -> float:
        """
        A European lookback call at maturity pays St - min(St).
        A European lookback put at maturity pays max(St) - St.
        min(St) is the minimum price over the life of the option
        max(St) is the maximum price over the life of the option
        Robert. L. MacDonald: Derivatives Markets (3rd. edition)
        Chapter 23: Exotic Option II
        Formula 23.47 (Exercise)

        :param option_type: call, put
        :param max_share_price: maximum share price
        :param min_share_price: minimum share price
        :return: value of lookback option
        """

        assert option_type == "call" or option_type == "put"

        if option_type == "call":
            self.w = 1
            self.s_bar = float(min_share_price)

        elif option_type == "put":
            self.w = -1
            self.s_bar = float(max_share_price)

        self.d5 = (log(self.K / self.s_bar) + (self.r - self.div_yield + 0.5 * (self.sigma ** 2)) * self.T) / (
                self.sigma * sqrt(self.T))
        self.d6 = self.d5 - self.sigma * sqrt(self.T)
        self.d7 = (log(self.s_bar / self.K) + (self.r - self.div_yield + 0.5 * (self.sigma ** 2)) * self.T) / (
                self.sigma * sqrt(self.T))
        self.d8 = self.d7 - self.sigma * sqrt(self.T)

        # Lookback option pricing
        self.lb_first_part = self.w * self.K * exp(-self.div_yield * self.T) * (
                stats.norm.cdf(self.w * self.d5) - (self.sigma ** 2) * stats.norm.cdf(-self.w * self.d5) / (
                2 * (self.r - self.div_yield)))
        self.lb_second_part = self.w * self.s_bar * exp(-self.r * self.T) * (stats.norm.cdf(self.w * self.d6) - (
                (self.sigma ** 2) / (2 * (self.r - self.div_yield)) * (self.K / self.s_bar) ** (
                1 - 2 * (self.r - self.div_yield) / (self.sigma ** 2))) * stats.norm.cdf(self.w * self.d8))

        return self.lb_first_part - self.lb_second_part


class GarmanKohlhagenForex(BSMOptionValuation):
    """
    Valuation of European call options in Black-Scholes-Merton Model (for forex)
    Garman, M. B. and Kohlhagen, S. W. "Foreign Currency Option Values." Journal of
    International Money and Finance 2, 231-237, 1983.
    Price, J. F. "Optional Mathematics is Not Optional." Not. Amer. Math. Soc. 43, 964-971, 1996.

    Attributes
    ==========
    S0: float
        current spot rate: units of domestic currency per unit of foreign currency
    K: float
        strike price: units of domestic currency per unit of foreign currency
    T: float
        maturity (in year fractions)
    rd: float
        domestic risk free interest rate
        assume flat term structure
    rf: float
        foreign risk free interest rate
    sigma: float
        volatility factor in diffusion term

    Methods:
    ==========
    call_value: float
        return value of a call option on forex (in domestic currecy)
    """

    def __init__(self, S0, K, T, rd, rf, sigma):
        BSMOptionValuation.__init__(S0, S0, K, T, rd, rf, sigma)
        assert sigma >= 0, 'volatility cannot be less than zero'
        assert S0 >= 0, 'initial stock price cannot be less than zero'
        assert T >= 0, 'time to maturity cannot be less than zero'

        self.S0 = float(S0)
        self.K = float(K)
        self.T = float(T)
        self.rf = float(rf)
        self.rd = float(rd)
        self.sigma = float(sigma)

        self.d1 = ((log(self.S0 / self.K) + (self.rd - self.rf + 0.5 * self.sigma ** 2) * self.T) / (
                self.sigma * sqrt(self.T)))

        self.d2 = self.d1 - self.sigma * sqrt(self.T)

    def call_value(self, empirical_put_price=None):
        """
        :return: call option value
        """
        if empirical_put_price is None:
            call_value = (self.S0 * exp(- self.rf * self.T) * stats.norm.cdf(self.d1, 0.0, 1.0) - self.K * exp(
                - self.rd * self.T) * stats.norm.cdf(self.d2, 0.0, 1.0))
        else:
            call_value = empirical_put_price + exp(-self.div_yield * self.T) * self.S0 - exp(-self.r * self.T) * self.K

        return call_value

    def put_value(self, empirical_call_price=None):
        """
        Use put call parity (incl. continuous dividend) to calculate the put option value
        :return: put option value
        """
        if empirical_call_price is None:
            put_value = self.K * exp(- self.rd * self.T) * stats.norm.cdf(- self.d2, 0.0, 1.0) - self.S0 * exp(
                - self.rf * self.T) * stats.norm.cdf(- self.d1, 0.0, 1.0)
        else:
            put_value = empirical_call_price + exp(-self.r * self.T) * self.K - exp(-self.div_yield * self.T) * self.S0

        return put_value

