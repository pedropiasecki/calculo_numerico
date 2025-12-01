from tkinter import *
from tkinter import ttk, messagebox
import time
import copy
import funcoes
import sistemas

# criação da janela
# abre e automaticamente fecha <-
root = Tk()

### backend
class Funcs():
    ## inciiar como padrão de exemplo
    def reinicia_arquivo_funcao(self):
        conteudo = """# exemplo de iserção
funcao: x**3 + 4*x**2 - 10
a: 1
b: 2
delta: 1e-6
n: 100
phi: (10 - 4*x**2)**(1/3)
dfuncao: 3*x**2 + 8*x
x0: 1.5
"""
        with open("./arquivos/funcao_arquivo.txt", "w", encoding="utf-8") as f:
            f.write(conteudo)

        # limpa o relatorio antes de usar
        with open("./arquivos/iteracoes_funcoes.txt", "w") as f:
            pass

    def carrega_arquivo(self):
        with open("./arquivos/funcao_arquivo.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.txt_mostra_funcao.delete("1.0", END)
        self.txt_mostra_funcao.insert("1.0", conteudo)

    def salvar_arquivo(self):
        conteudo = self.txt_mostra_funcao.get("1.0", END)
        with open("./arquivos/funcao_arquivo.txt", "w", encoding="utf-8") as f:
            f.write(conteudo)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def voltar_menu(self):
        self.limpar_tela()
        self.tela()
        self.tela_de_escolhas()
        self.Ab_carregado = False
        self.A_carregado = False
        self.b_carregado = False

    def realiza_metodo(self, metodo='Bisseccao'):
        params = funcoes.ler_parametros("./arquivos/funcao_arquivo.txt")

        # criar as funções
        funcao = funcoes.lerFuncao(params["funcao"])
        a = params["a"]
        b = params["b"]
        delta = params["delta"]
        n = params["n"]
        phi_str = params.get("phi", "").strip()
        phi = funcoes.lerFuncao(phi_str) if phi_str else None
        dfuncao_str = params.get("dfuncao", "").strip()
        dfuncao = funcoes.lerFuncao(dfuncao_str) if dfuncao_str else None
        x0 = params.get("x0", (a+b)/2)

        # abre o arquivo de relatorio
        arquivo_saida = "./arquivos/iteracoes_funcoes.txt"
        open(arquivo_saida, "w").close()

        if (n <= 0):
            with open(arquivo_saida, "a", encoding="utf-8") as f:
                    f.write(f'Numero (n) de iterações não informado ou  <= 0')
        else:
            if (metodo == 'Bisseccao'):
                funcoes.Bisseccao(funcao, a, b, delta, n, arquivo_saida)
            if (metodo == 'Mil'):
                if phi is None:
                    with open(arquivo_saida, "a", encoding="utf-8") as f:
                        f.write(f'Método: MIL: Phi não informado')
                else:
                    funcoes.Mil(funcao, dfuncao, x0, delta, n, arquivo_saida)
            if (metodo == 'NewtonRaphson'):
                if dfuncao is None:
                    with open(arquivo_saida, "a", encoding="utf-8") as f:
                        f.write(f'Método: Newrton Raphson: Deriavda não informada')
                else:
                    funcoes.NewtonRaphson(funcao, dfuncao, x0, delta, n, arquivo_saida)
            if (metodo == 'Secante'):
                funcoes.Secante(funcao, a, b, delta, n, arquivo_saida)
            if (metodo == 'Regula Falsi'):
                funcoes.RegulaFalsi(funcao, a, b, delta, n, arquivo_saida)

        self.resultados_funcoes()

    def resultados_funcoes(self):
        # carrega o conteúdo
        with open("./arquivos/iteracoes_funcoes.txt", "r", encoding="utf-8") as f:
            conteudo = f.readline()

        self.lbl_sistemas.config(text=conteudo)

    def ver_iteracoes(self):
        # cria uma nova janela
        janela = Toplevel(self.root)
        janela.title("Resultados das Funções")
        janela.geometry("600x500")
        janela.configure(background="lightgrey")

        # frame para deixar organizado
        frame = Frame(janela, bd=4, bg="white", highlightbackground='#759fe6',
                    highlightthickness=3)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # scrollbar
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)

        # txt_mostra_funcao
        txt_mostra_funcao = Text(frame, wrap=WORD, yscrollcommand=scroll.set,
                    font=("Arial", 12), bg="white", bd=0)
        txt_mostra_funcao.pack(fill=BOTH, expand=True)

        scroll.config(command=txt_mostra_funcao.yview)

        # carrega o conteúdo
        with open("./arquivos/iteracoes_funcoes.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()

        txt_mostra_funcao.insert("1.0", conteudo)

    ## SISTEMAS
    def carrega_arquivo_sistemas(self):
        with open("./arquivos/sistema_arquivo.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()

        if not conteudo:
            messagebox.showwarning("Aviso", "Arquivo Ab está vazio.")
            return


        self.txt_mostra_sistemas.config(state="normal")

        self.txt_mostra_sistemas.delete("1.0", END)
        self.txt_mostra_sistemas.insert("1.0", "Sistema completo:\n")
        self.txt_mostra_sistemas.insert(END, conteudo)

        self.txt_mostra_sistemas.config(state="disabled")

        self.A, self.b = sistemas.ler_sistema("./arquivos/sistema_arquivo.txt")

        self.Ab_carregado = True

    def carrega_arquivo_A(self):
        with open("./arquivos/ler_A.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()

        if not conteudo:
            messagebox.showwarning("Aviso", "Arquivo A está vazio.")
            return

        self.txt_mostra_sistemas.config(state="normal")

        self.txt_mostra_sistemas.delete("1.0", END)
        self.txt_mostra_sistemas.insert("1.0", "Matriz A:\n")
        self.txt_mostra_sistemas.insert(END, conteudo + "\n")

        self.txt_mostra_sistemas.config(state="disabled")

        self.A = sistemas.ler_A("./arquivos/ler_A.txt")

        self.Ab_carregado = False
        self.A_carregado = True
        self.b_carregado = False

    def carrega_arquivo_b(self):
        with open("./arquivos/ler_b.txt", "r", encoding="utf-8") as f:
            conteudo = f.read().strip()

        if not conteudo:
            messagebox.showwarning("Aviso", "Arquivo b está vazio.")
            return

        if self.Ab_carregado:
            messagebox.showwarning("Aviso", "Carregue a matriz A antes de carregar o vetor b.")
            return

        if not self.A_carregado:
            messagebox.showwarning("Aviso", "Carregue a matriz A antes de carregar o vetor b.")
            return

        if self.b_carregado:
            messagebox.showinfo("Aviso", "O vetor b já foi carregado!")
            return

        self.txt_mostra_sistemas.config(state="normal")
        self.txt_mostra_sistemas.insert(END, "\nVetor b:\n")
        self.txt_mostra_sistemas.insert(END, conteudo + "\n")
        self.txt_mostra_sistemas.config(state="disabled")

        self.b = sistemas.ler_b("./arquivos/ler_b.txt")

        self.b_carregado = True

    
    def realiza_metodo_sistemas(self, metodo):
        arquivo_saida = "./arquivos/resultado_sistema.txt"
        open(arquivo_saida, "w").close()

        if (self.b_carregado == False and self.Ab_carregado == False):
            if (self.A_carregado == True):
                messagebox.showwarning("Aviso", "Matriz b não foi carregada")
                return
            else:
                messagebox.showwarning("Aviso", "Matriz não foi carregada")
                return
            
        try:
            inicio = time.time()
            if metodo == 'Gauss':
                x = sistemas.gauss(copy.deepcopy(self.A), copy.deepcopy(self.b))

            elif metodo == 'Gauss Pivoteamento Parcial':
                x = sistemas.gauss_pivoteamento_parcial(copy.deepcopy(self.A), copy.deepcopy(self.b))

            elif metodo == 'Gauss Pivoteamento Completo':
                x = sistemas.gauss_pivoteamento_completo(copy.deepcopy(self.A), copy.deepcopy(self.b))

            elif metodo == 'Decomposição LU':
                x = sistemas.decomposicao_LU(copy.deepcopy(self.A), copy.deepcopy(self.b))

            elif metodo == 'Cholesky':
                x = sistemas.cholesky(copy.deepcopy(self.A), copy.deepcopy(self.b))

            elif metodo == 'Gauss Jacobi':
                try:
                    n = int(self.entry_numero_iteracoes.get())
                    delta = float(self.entry_delta.get())
                except ValueError:
                    messagebox.showwarning("Aviso", "Digite valores numéricos válidos para n e delta")
                    return

                if n <= 0 or delta <= 0:
                    messagebox.showwarning("Aviso", "n e delta devem ser maiores que zero")
                    return
                
                tipo_erro = self.combo_erro.get()
                x, k= sistemas.gaussJacobi(self.A, self.b, n, delta, tipo_erro)

            elif metodo == 'Gauss Seidel':
                try:
                    n = int(self.entry_numero_iteracoes.get())
                    delta = float(self.entry_delta.get())
                except ValueError:
                    messagebox.showwarning("Aviso", "Digite valores numéricos válidos para n e delta")
                    return

                if n <= 0 or delta <= 0:
                    messagebox.showwarning("Aviso", "n e delta devem ser maiores que zero")
                    return
                
                tipo_erro = self.combo_erro.get()
                x, k = sistemas.gaussSeidel(self.A, self.b, n, delta, tipo_erro)

            fim = time.time()
            tempo = fim - inicio
            
            if (metodo != 'Gauss Seidel' and metodo != 'Gauss Jacobi'): 
                self.resultado_sistemas(arquivo_saida, x, metodo, tempo)
            else:
                self.resultado_sistemas_iterativos(arquivo_saida, x, metodo, tempo, k, delta)

        except Exception as e:
            messagebox.showwarning("Erro", f"erro ao executar {e}")
            return

    def resultado_sistemas(self, arquivo_saida, x, metodo, tempo):
        # salvar resultado
        with open(arquivo_saida, "a", encoding="utf-8") as f:
            f.write(f'Método: {metodo}, x = {x}, tempo: {tempo}')

        # mostrar na tela
        with open(arquivo_saida, "r", encoding="utf-8") as f:
            conteudo = f.readline()

        self.lbl_sistemas.config(text=conteudo)

    def resultado_sistemas_iterativos(self, arquivo_saida, x, metodo, tempo, k, delta):
        # salvar resultado
        with open(arquivo_saida, "a", encoding="utf-8") as f:
            f.write(f'Método: {metodo}, x = {x}, iterações: {k} tempo: {tempo}')

        # mostrar na tela
        with open(arquivo_saida, "r", encoding="utf-8") as f:
            conteudo = f.readline()

        self.lbl_sistemas.config(text=conteudo)
        

### interface
class Application(Funcs):
    def __init__(self):
        self.root = root
        self.reinicia_arquivo_funcao()
        self.tela()
        self.tela_de_escolhas()
        self.Ab_carregado = False
        self.A_carregado = False
        self.b_carregado = False
        # entra em loop e se mantém aberta
        root.mainloop()
    
    def tela(self):
        # titulo da janela
        self.root.title("Calculo Numérico")

        # cor de fundo ou imagem 
        self.root.configure(background='grey')

        # dimensões que a janela vai iniciar x vs y
        self.root.geometry("800x600")

        # janela responsiva, horizontal e vertical
        self.root.resizable(True , True)

        # maximo que pode expandir
        self.root.maxsize(width=1000, height=800 )

        # minimo que pode diminuir
        self.root.minsize(width=500, height=400)

    def tela_de_escolhas(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = Frame(self.root, bg="#e0e0e0")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        titulo = Label(frame, text="Cálculo Numérico", bg="#e0e0e0", fg="#000000",
                        font=('Verdana', 24, 'bold'))
        titulo.pack(pady=20)

        frame_sistemas = Frame(frame, bg="#e0e0e0")
        frame_sistemas.pack(pady=20)

        frame_funcoes = Frame(frame, bg="#e0e0e0")
        frame_funcoes.pack(pady=20)

        lbl_sistemas = Label(frame_sistemas, text="Resolver Sistemas Lineares", bg="#e0e0e0", fg="#000000",
                            font=('Verdana', 14, 'bold'))
        lbl_sistemas.pack()

        bt_sistemas = Button(frame_sistemas, text="Abrir Sistemas", bd=2, bg="#26698b", fg='white',
                             font=('Verdana', 10, 'bold'), width=20, height=2, command=self.tela_sistemas)
        bt_sistemas.pack(pady=10)

        lbl_funcoes = Label(frame_funcoes, text="Encontrar Raiz de Funções", bg="#e0e0e0", fg="#000000",
                            font=('Verdana', 14, 'bold'))
        lbl_funcoes.pack()

        bt_funcoes = Button(frame_funcoes, text="Abrir Funções", bd=2, bg="#26698b", fg='white',
                            font=('Verdana', 10, 'bold'), width=20, height=2, command=self.tela_funcoes)
        bt_funcoes.pack(pady=10)


    #### TELA DE FUNÇÕES
    def tela_funcoes(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1_2()
        self.widgets_frame_3_4()
        self.carrega_arquivo()

    def frames_da_tela(self):
        # border, background (color), borda bg, grossura borda
        self.frame_1 = Frame(self.root, bd = 4, bg = "lightgrey", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.46)

        # border, background (color), borda bg, grossura borda
        self.frame_2 = Frame(self.root, bd = 4, bg = "white", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_2.place(relx=0.05 , rely=0.15, relwidth=0.9, relheight=0.3)

        # border, background (color), borda bg, grossura borda
        self.frame_3 = Frame(self.root, bd = 4, bg = "lightgrey", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_3.place(relx=0.02 , rely=0.5, relwidth=0.96, relheight=0.46)

        # border, background (color), borda bg, grossura borda
        self.frame_4 = Frame(self.root, bd = 4, bg = "white", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_4.place(relx=0.05 , rely=0.70, relwidth=0.9, relheight=0.10)

    def widgets_frame_1_2(self):
        # Criação botão de voltar
        # dentro do frame_1
        self.bt_voltar = Button(self.frame_1, text="Voltar", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=self.voltar_menu) 
        self.bt_voltar.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.12)

        self.bt_carregar_funcao = Button(self.frame_1, text="Carregar Função", bd=2, bg="#26698b", fg='white',
                                font=('verdana', 8, 'bold'), command=self.carrega_arquivo)
        self.bt_carregar_funcao.place(relx=0.30, rely=0.05, relwidth=0.3, relheight=0.12)

        self.bt_salvar = Button(self.frame_1, text="Salvar", bd=2, bg="#26698b", fg='white',
                                font=('verdana', 8, 'bold'),command=self.salvar_arquivo)
        self.bt_salvar.place(relx=0.65, rely=0.05, relwidth=0.3, relheight=0.12)

        ## função passada em arquivo mostrada na interface
        scroll = Scrollbar(self.frame_2)
        scroll.pack(side=RIGHT, fill=Y)

        self.txt_mostra_funcao = Text(self.frame_2, wrap=WORD, yscrollcommand=scroll.set,
                            font=("Arial", 12), bg="white", bd=0)
        self.txt_mostra_funcao.pack(fill=BOTH, expand=True)

        scroll.config(command=self.txt_mostra_funcao.yview)

    def widgets_frame_3_4(self):
        self.bt_bisseccao = Button(self.frame_3, text="Bisseccao", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo("Bisseccao")) 
        self.bt_bisseccao.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.12)

        self.bt_mil = Button(self.frame_3, text="Mil", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo("Mil")) 
        self.bt_mil.place(relx=0.35, rely=0.05, relwidth=0.2, relheight=0.12)

        self.bt_newtonRaphson = Button(self.frame_3, text="Newton-Raphson", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo("NewtonRaphson")) 
        self.bt_newtonRaphson.place(relx=0.65, rely=0.05, relwidth=0.2, relheight=0.12)

        self.bt_secante = Button(self.frame_3, text="Secante", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo("Secante")) 
        self.bt_secante.place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.12)

        self.bt_regulaFalsi = Button(self.frame_3, text="Regula Falsi", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo("Regula Falsi")) 
        self.bt_regulaFalsi.place(relx=0.35, rely=0.25, relwidth=0.2, relheight=0.12)

        self.bt_bisseccao = Button(self.frame_3, text="Ver iterações", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.ver_iteracoes()) 
        self.bt_bisseccao.place(relx=0.05, rely=0.7, relwidth=0.2, relheight=0.12)

        self.lbl_sistemas = Label(self.frame_4, bg="#ffffff", fg="#000000",
                            font=('Verdana', 8))
        self.lbl_sistemas.pack()

    ### TELA DE SISTEMAS
    def tela_sistemas(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.tela()
        self.frames_da_tela_sistemas()
        self.widgets_frame_1_2_sistemas()
        self.widgets_frame_3_4_sistemas()
        # self.carrega_arquivo_sistemas()

    def frames_da_tela_sistemas(self):
        # border, background (color), borda bg, grossura borda
        self.frame_1 = Frame(self.root, bd = 4, bg = "lightgrey", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.46)

        # border, background (color), borda bg, grossura borda
        self.frame_2 = Frame(self.root, bd = 4, bg = "white", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_2.place(relx=0.05 , rely=0.15, relwidth=0.9, relheight=0.3)

        # border, background (color), borda bg, grossura borda
        self.frame_3 = Frame(self.root, bd = 4, bg = "lightgrey", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_3.place(relx=0.02 , rely=0.5, relwidth=0.96, relheight=0.46)

        # border, background (color), borda bg, grossura borda
        self.frame_4 = Frame(self.root, bd = 4, bg = "white", highlightbackground='#759fe6', 
                             highlightthickness=3)

        # numeração de 0 a 1, onde 0 é o começo e 1 é o fim
        self.frame_4.place(relx=0.05 , rely=0.80, relwidth=0.9, relheight=0.10)

    def widgets_frame_1_2_sistemas(self):
        self.bt_voltar = Button(self.frame_1, text="Voltar", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=self.voltar_menu) 
        self.bt_voltar.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.12)

        self.bt_carregar_sistema = Button(self.frame_1, text="Carregar Sistema", bd=2, bg="#26698b", fg='white',
                                font=('verdana', 8, 'bold'), command=self.carrega_arquivo_sistemas)
        self.bt_carregar_sistema.place(relx=0.2, rely=0.05, relwidth=0.20, relheight=0.12)

        self.bt_carregar_A = Button(self.frame_1, text="Carregar A", bd=2, bg="#26698b", fg='white',
                                font=('verdana', 8, 'bold'),command=self.carrega_arquivo_A)
        self.bt_carregar_A.place(relx=0.45, rely=0.05, relwidth=0.15, relheight=0.12)

        self.bt_carregar_b = Button(self.frame_1, text="Carregar b", bd=2, bg="#26698b", fg='white',
                                font=('verdana', 8, 'bold'),command=self.carrega_arquivo_b)
        self.bt_carregar_b.place(relx=0.65, rely=0.05, relwidth=0.15, relheight=0.12)

        ## sistema passado em arquivo mostrada na interface
        scroll = Scrollbar(self.frame_2)
        scroll.pack(side=RIGHT, fill=Y)

        self.txt_mostra_sistemas = Text(self.frame_2, wrap=WORD, yscrollcommand=scroll.set,
                            font=("Arial", 12), bg="white", bd=0, state="disabled")
        self.txt_mostra_sistemas.pack(fill=BOTH, expand=True)

        scroll.config(command=self.txt_mostra_sistemas.yview)

    def widgets_frame_3_4_sistemas(self):
        self.bt_gauss = Button(self.frame_3, text="Gauss", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Gauss")) 
        self.bt_gauss.place(relx=0.1, rely=0.05, relwidth=0.15, relheight=0.12)

        self.bt_gauss_pivo_parcial = Button(self.frame_3, text="Gauss PP", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Gauss Pivoteamento Parcial")) 
        self.bt_gauss_pivo_parcial.place(relx=0.30, rely=0.05, relwidth=0.15, relheight=0.12)

        self.bt_gauss_pivo_completo = Button(self.frame_3, text="Gauss PC", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Gauss Pivoteamento Completo")) 
        self.bt_gauss_pivo_completo.place(relx=0.50, rely=0.05, relwidth=0.15, relheight=0.12)

        self.bt_lu = Button(self.frame_3, text="Fatoração LU", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Decomposição LU")) 
        self.bt_lu.place(relx=0.70, rely=0.05, relwidth=0.15, relheight=0.12)

        self.bt_cholesky = Button(self.frame_3, text="Cholesky", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Cholesky")) 
        self.bt_cholesky.place(relx=0.1, rely=0.25, relwidth=0.15, relheight=0.12)

        self.bt_gauss_jacobi = Button(self.frame_3, text="Gauss Jacobi", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Gauss Jacobi")) 
        self.bt_gauss_jacobi.place(relx=0.3, rely=0.25, relwidth=0.15, relheight=0.12)

        self.bt_gauss_seidel = Button(self.frame_3, text="Gauss Seidel", bd=2, bg="#26698b", fg='white', 
                                font=('verdana', 8, 'bold'), command=lambda: self.realiza_metodo_sistemas("Gauss Seidel")) 
        self.bt_gauss_seidel.place(relx=0.5, rely=0.25, relwidth=0.15, relheight=0.12)

        self.lbl_tipo_erro = Label(self.frame_3, text="Condição de parada:", bg='lightgrey', fg='#107db2')
        self.lbl_tipo_erro.place(relx=0.55, rely=0.45)

        self.opcoes_erro = ["Erro Absoluto", "Erro Relativo"]

        self.combo_erro = ttk.Combobox(self.frame_3, values=self.opcoes_erro, state="readonly")
        self.combo_erro.current(0)
        self.combo_erro.place(relx=0.7, rely=0.45, relwidth=0.15)

        self.lb_numero_iteracoes = Label(self.frame_3, text = "Nº Iterações:", bg='lightgrey', fg='#107db2')
        self.lb_numero_iteracoes.place(relx=0.1, rely=0.45)

        self.entry_numero_iteracoes = Entry(self.frame_3, bd=2)
        self.entry_numero_iteracoes.place(relx=0.20, rely=0.45, relwidth=0.1)
        self.entry_numero_iteracoes.insert(0, 50)

        self.lb_delta = Label(self.frame_3, text = "delta:", bg='lightgrey', fg='#107db2')
        self.lb_delta.place(relx=0.35, rely=0.45)

        self.entry_delta = Entry(self.frame_3, bd=2)
        self.entry_delta.place(relx=0.40, rely=0.45, relwidth=0.1, )
        self.entry_delta.insert(0, 0.05)

        self.lbl_sistemas = Label(self.frame_4, bg="#ffffff", fg="#000000",
                            font=('Verdana', 8))
        self.lbl_sistemas.pack()



Application()
