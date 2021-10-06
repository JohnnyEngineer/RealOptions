from Functions import*
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Menu Inicial", font=('Arial', 12, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Estimação Volatilidade",width=40,
                  command=lambda: master.switch_frame(EstimarVolatilidade)).pack()
        tk.Button(self, text="Simulação Monte Carlo Valores",width=40,
                  command=lambda: master.switch_frame(MonteCarloValores)).pack()
        tk.Button(self, text="Opção de Abandono",width=40,
                  command=lambda: master.switch_frame(OpcaoAbandono)).pack()
        tk.Button(self, text="Opção de Expandir",width=40,
                  command=lambda: master.switch_frame(OpcaoExpandir)).pack()
        tk.Button(self, text="Opção de Contrair",width=40,
                  command=lambda: master.switch_frame(OpcaoContracao)).pack()
        tk.Button(self, text="Opções Compostas",width=40,
                  command=lambda: master.switch_frame(OpcoesCompostas)).pack()
        tk.Button(self, text="Opções de Esperar",width=40,
                  command=lambda: master.switch_frame(OpcoesEsperar)).pack()
        tk.Button(self, text="Opções Modelo Black-Scholes",width=40,
                  command=lambda: master.switch_frame(OpcaoBlackScholes)).pack()

class MonteCarloValores(tk.Frame):
    
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def Simular(self,tkWindow, retorno, volatilidade,precoinicial):
        annual_drift=retorno.get()
        annual_volatility=volatilidade.get()
        initial_stock = precoinicial.get()
        sim=MonteCarloSimulation(annual_drift,annual_volatility,initial_stock, periodo=4, 
                                 quantidade_simulacao=1000, imagem=True, tkWindow=tkWindow)
    def __init__(self, master):
        global app
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        retorno=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        precoinicial=tk.DoubleVar()
        tk.Label(self, text="Digite o valor esperado do retorno anual(10%=0.1):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self, textvariable=retorno, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor estimado da volatilidade anual(10%=0.1):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self, textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do preço inicial:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=precoinicial, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Simular",
                  command=lambda: self.Simular(app,retorno, volatilidade,precoinicial)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
class OpcaoAbandono(tk.Frame):
    
    def PrecificarOpcao(self,T,S0,sigma,rf,K):
        global app
        T=int(T.get())
        S0=S0.get()
        sigma=sigma.get()
        rf=rf.get()
        K=K.get()
        binomial_model_abandono(T=T, S0=S0, sigma=sigma, rf=rf, K=K, nome="teste", dpi=600, imagem=True, 
                             tkWindow=app)
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        df=None
        df1=None
        global app
        periodo=tk.IntVar()
        valor=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        taxalivrederisco=tk.DoubleVar()
        valorresidual=tk.DoubleVar()
        tk.Frame.configure(self)
        tk.Label(self, text="Digite o período do projeto (em anos):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=periodo, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do investimento:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valor, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a volatilidade:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor da taxa livre de risco:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=taxalivrederisco, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor residual:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valorresidual, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Calcular",
                  command=lambda: self.PrecificarOpcao(T=periodo,S0=valor,sigma=volatilidade,
                                                       rf=taxalivrederisco,K=valorresidual)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()

class OpcaoExpandir(tk.Frame):
    
    def PrecificarOpcao(self,T,S0,sigma,rf,fator_expansao,custo_expansao):
        global app
        T=int(T.get())
        S0=S0.get()
        sigma=sigma.get()
        rf=rf.get()
        fator_expansao=fator_expansao.get()
        custo_expansao=custo_expansao.get()
        binomial_model_expansion(T=T, S0=S0, sigma=sigma, rf=rf, nome="teste", dpi=600, imagem=True, 
                                 fator_expansao=fator_expansao, custo_expansao=custo_expansao, tkWindow=app)
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        df=None
        df1=None
        global app
        periodo=tk.IntVar()
        valor=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        taxalivrederisco=tk.DoubleVar()
        fator_expansao=tk.DoubleVar()
        custo_expansao=tk.DoubleVar()
        tk.Frame.configure(self)
        tk.Label(self, text="Digite o período do projeto (em anos):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=periodo, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do investimento:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valor, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a volatilidade:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor da taxa livre de risco:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=taxalivrederisco, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o fator de expansão:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=fator_expansao, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o custo de expansão:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=custo_expansao, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Calcular",
                  command=lambda: self.PrecificarOpcao(T=periodo,S0=valor,sigma=volatilidade,
                                                       rf=taxalivrederisco,fator_expansao=fator_expansao,
                                                       custo_expansao=custo_expansao)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()

class OpcaoContracao(tk.Frame):
    
    def PrecificarOpcao(self,T,S0,sigma,rf,fator_contracao,economia_contracao):
        global app
        T=int(T.get())
        S0=S0.get()
        sigma=sigma.get()
        rf=rf.get()
        fator_contracao=fator_contracao.get()
        economia_contracao=economia_contracao.get()
        binomial_model_contraction(T=T, S0=S0, sigma=sigma, rf=rf, nome="teste", dpi=600, imagem=True, 
                                   fator_contracao=fator_contracao, economia_contracao=economia_contracao, 
                                   tkWindow=app)
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        df=None
        df1=None
        global app
        periodo=tk.IntVar()
        valor=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        taxalivrederisco=tk.DoubleVar()
        fator_contracao=tk.DoubleVar()
        economia_contracao=tk.DoubleVar()
        tk.Frame.configure(self)
        tk.Label(self, text="Digite o período do projeto (em anos):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=periodo, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do investimento:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valor, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a volatilidade:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor da taxa livre de risco:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=taxalivrederisco, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o fator de contração:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=fator_contracao, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a economia na contração:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=economia_contracao, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Calcular",
                  command=lambda: self.PrecificarOpcao(T=periodo,S0=valor,sigma=volatilidade,
                                                       rf=taxalivrederisco,fator_contracao=fator_contracao,
                                                       economia_contracao=economia_contracao)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()

class OpcoesCompostas(tk.Frame):
    
    def PrecificarOpcao(self,T,S0,sigma,rf,custos):
        global app
        T=int(T.get())
        S0=S0.get()
        sigma=sigma.get()
        rf=rf.get()
        itens=list(self.listbox.get(0,END))
        binomial_model_compounds(T=T, S0=S0, sigma=sigma, rf=rf, custos=itens, nome="teste", dpi=600, 
                                 imagem=True, tkWindow=app)
    
    def AdicionarItem(self):
        self.listbox.insert(tk.END,self.custos.get())
        
    def RemoverItem(self):
        self.listbox.delete(self.listbox.curselection())
        
    def LimparListBox(self):
        self.listbox.delete(0,END)
    
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        df=None
        df1=None
        global app
        periodo=tk.IntVar()
        valor=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        taxalivrederisco=tk.DoubleVar()
        self.custos=tk.DoubleVar()
        tk.Label(self, text="Digite o período do projeto (em anos):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=periodo, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do investimento:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valor, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a volatilidade:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor da taxa livre de risco:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=taxalivrederisco, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Adicione os custos:", 
                 font=('Arial', 10, "bold")).pack()
        self.listbox = Listbox(self)
        self.listbox.pack()
        textBox=tk.Entry(self,textvariable=self.custos, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Adicionar Custo",
                  command=self.AdicionarItem).pack()
        tk.Button(self, text="Remover Custo",
                  command=self.RemoverItem).pack()
        tk.Button(self, text="Limpar toda lista de custos",
                  command=self.LimparListBox).pack()
        tk.Button(self, text="Calcular",
                  command=lambda: self.PrecificarOpcao(T=periodo,S0=valor,sigma=volatilidade,
                                                       rf=taxalivrederisco,custos=self.custos)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()

class OpcoesEsperar(tk.Frame):
    
    def PrecificarOpcao(self,T,S0,sigma,rf,custos):
        global app
        T=int(T.get())
        S0=S0.get()
        sigma=sigma.get()
        rf=rf.get()
        itens=list(self.listbox.get(0,END))
        binomial_model_dynamicstrikes(T=T, S0=S0, sigma=sigma, rf=rf, custos=itens, nome="teste", dpi=600, 
                                      imagem=True, tkWindow=app)
    
    def AdicionarItem(self):
        self.listbox.insert(tk.END,self.custos.get())
        
    def RemoverItem(self):
        self.listbox.delete(self.listbox.curselection())
        
    def LimparListBox(self):
        self.listbox.delete(0,END)
    
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        df=None
        df1=None
        global app
        periodo=tk.IntVar()
        valor=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        taxalivrederisco=tk.DoubleVar()
        self.custos=tk.DoubleVar()
        tk.Label(self, text="Digite o período do projeto (em anos):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=periodo, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do investimento:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valor, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a volatilidade:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor da taxa livre de risco:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=taxalivrederisco, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Adicione os custos:", 
                 font=('Arial', 10, "bold")).pack()
        self.listbox = Listbox(self)
        self.listbox.pack()
        textBox=tk.Entry(self,textvariable=self.custos, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Adicionar Custo",
                  command=self.AdicionarItem).pack()
        tk.Button(self, text="Remover Custo",
                  command=self.RemoverItem).pack()
        tk.Button(self, text="Limpar toda lista de custos",
                  command=self.LimparListBox).pack()
        tk.Button(self, text="Calcular",
                  command=lambda: self.PrecificarOpcao(T=periodo,S0=valor,sigma=volatilidade,
                                                       rf=taxalivrederisco,custos=self.custos)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()

class OpcaoBlackScholes(tk.Frame):
    
    def PrecificarOpcao(self,T,S0,sigma,rf,precoexercicio,dividendos):
        global app
        T=int(T.get())
        S0=S0.get()
        sigma=sigma.get()
        rf=rf.get()
        precoexercicio=precoexercicio.get()
        dividendos=dividendos.get()
        x = BSMOptionValuation(S0=S0, K=precoexercicio, T=T, r=rf, sigma=sigma, div_yield=dividendos)
        messagebox.showinfo('Precificaão Modelo Black-Scholes-Merton', 'A call possui preço de: '+str(np.round(x.call_value(),2))+"."+
                           " O valor da put é de:"+str(np.round(x.put_value(),2)))
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',','.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        df=None
        df1=None
        global app
        periodo=tk.IntVar()
        valor=tk.DoubleVar()
        volatilidade=tk.DoubleVar()
        taxalivrederisco=tk.DoubleVar()
        precoexercicio=tk.DoubleVar()
        dividendos=tk.DoubleVar()
        tk.Frame.configure(self)
        tk.Label(self, text="Digite o período do projeto (em anos):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=periodo, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor do investimento:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=valor, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite a volatilidade:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=volatilidade, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor da taxa livre de risco:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=taxalivrederisco, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o preço do exercício:", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=precoexercicio, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Label(self, text="Digite o valor dos dividendos (em %):", 
                 font=('Arial', 10, "bold")).pack()
        textBox=tk.Entry(self,textvariable=dividendos, validate="key")
        textBox['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        textBox.pack()
        tk.Button(self, text="Calcular",
                  command=lambda: self.PrecificarOpcao(T=periodo,S0=valor,sigma=volatilidade,
                                                       rf=taxalivrederisco,precoexercicio=precoexercicio,
                                                       dividendos=dividendos)).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
class EstimarVolatilidade(tk.Frame):
    
    def CalcularVolatilidade(self):
        itens=list(self.listbox.get(0,END))
        messagebox.showinfo('Volatilidade', 'A volatilidade do fluxo de caixa informado é de: '+str(np.round(Volatilidade(itens)[0]*100,2))+"%")
    
    def NumeroValidation(self,S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                 '.']:
            return True
        else:
            messagebox.showinfo('Alerta!', 'Digite apenas números')
            return False
    def AdicionarItem(self):
        self.listbox.insert(tk.END,self.caixa.get())
        
    def RemoverItem(self):
        self.listbox.delete(self.listbox.curselection())
        
    def LimparListBox(self):
        self.listbox.delete(0,END)
        
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        self.listbox = Listbox(self)
        self.listbox.pack()
        self.caixa=tk.DoubleVar()
        tk.Label(self, text="Insira o valor do fluxo de caixa:", 
                 font=('Arial', 10, "bold")).pack()
        self.entrada=tk.Entry(self,textvariable=self.caixa, validate="key")
        self.entrada['validatecommand'] = (self.register(self.NumeroValidation),'%S')
        self.entrada.pack()
        tk.Button(self, text="Adicionar Fluxo de Caixa",
                  command=self.AdicionarItem).pack()
        tk.Button(self, text="Remover Fluxo de Caixa",
                  command=self.RemoverItem).pack()
        tk.Button(self, text="Calcular Volatilidade",
                  command=self.CalcularVolatilidade).pack()
        tk.Button(self, text="Limpar Fluxo de Caixa",
                  command=self.LimparListBox).pack()
        tk.Button(self, text="Voltar para página inical",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = App()
    app.title("Análise de Opções Reais v1.0")
    app.geometry("400x550")
    app.mainloop()