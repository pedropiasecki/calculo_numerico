import math

# avaliar expressões
# permite as funções do math
# cria a váriavel x
def aval_expr(expr, x_val=None):
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    if x_val is not None:
        allowed_names["x"] = x_val
    return eval(expr, {"__builtins__": None}, allowed_names)


# le o arquivo linha por linha
# converte os números para int ou float
def ler_parametros(nome_arquivo):
    params = {}
    with open(nome_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            chave, valor = linha.split(":", 1)
            chave = chave.strip()
            valor = valor.strip()
            try:
                if "." in valor or "e" in valor.lower():
                    valor = float(valor)
                else:
                    valor = int(valor)
            except:
                pass
            params[chave] = valor
    return params

# função f(x)
def lerFuncao(expr: str):
    def f(x):
        return aval_expr(expr, x)
    return f

# escrever no relatorio
def salvar_tabela(nome_arquivo, metodo, cabecalho, linhas):
    with open(nome_arquivo, "a", encoding="utf-8") as f:
        f.write(f"\n===== {metodo} =====\n")

        for linha in linhas:
            f.write("---------------\n")
            for titulo, valor in zip(cabecalho, linha):
                f.write(f"{titulo} = {valor}\n")
        f.write("---------------\n")

# escrever antes do relatório
def salvar_tabela_antes(nome_arquivo, metodo, it, raiz):
        with open(nome_arquivo, "a", encoding="utf-8") as f:
            f.write(f'Método: {metodo}, k = {it}, raiz = {raiz}')

# caso não convergir
def salvar_tabela_caso(nome_arquivo, metodo, it, raiz):
        with open(nome_arquivo, "a", encoding="utf-8") as f:
            f.write(f'Método: {metodo}, k = {it}, raiz = {raiz}, Não convergiu no limite de iterações')


def Bisseccao(func, a, b, delta, n, arquivo_saida):
    k = 0
    tabelas = []
    while abs(b - a) > delta and k < n:
        k += 1
        meio = (a + b) / 2
        fmeio = func(meio)
        tabelas.append([k, a, b, meio, fmeio])
        if func(a) * fmeio < 0:
            b = meio
        else:
            a = meio
    if (k == n):
        salvar_tabela_caso(arquivo_saida, "Bisseccao", k, meio)
    salvar_tabela_antes(arquivo_saida, "Bisseccao", k, meio)
    salvar_tabela(arquivo_saida, "Bisseccao", ["k", "a", "b", "meio", "f(meio)"], tabelas)

def Mil(func, phi, x0, delta, n, arquivo_saida):
    tabelas = []
    k = 0
    while k < n:
        k += 1

        try:
            x1 = phi(x0)
            f_x1 = func(x1)
        except OverflowError:
            with open(arquivo_saida, "a", encoding="utf-8") as f:
                f.write(f'Método MIL: Overflow na iteração {k}, x0 = {x0}\n')
            break
        
        tabelas.append([k, x0, x1, f_x1])
        if abs(f_x1) < delta or abs(x1 - x0) < delta:
            salvar_tabela_antes(arquivo_saida, "Método Iterativo Linear (MIL)", k, x1)
            break
        x0 = x1
    if (k==n):
        salvar_tabela_caso(arquivo_saida, "MIL não convergiu", k, x1)
    salvar_tabela(arquivo_saida, "MIL", ["k", "x0", "x1", "f(x1)"], tabelas)

def NewtonRaphson(func, dfunc, x0, delta, n, arquivo_saida):
    tabelas = []
    k = 0
    while k < n:
        k += 1
        f0 = func(x0)
        df0 = dfunc(x0)
        x1 = x0 - f0 / df0
        tabelas.append([k, x0, f0, df0, x1, func(x1)])
        if abs(func(x1)) < delta or abs(x1 - x0) < delta:
            salvar_tabela_antes(arquivo_saida, "Newton-Raphson", k, x1)
            break
        x0 = x1
    if (k==n):
        salvar_tabela_caso(arquivo_saida, "Newton-Raphson", k, x1)
    salvar_tabela(arquivo_saida, "NewtonRaphson", ["k", "x0", "f(x0)", "f'(x0)", "x1", "f(x1)"], tabelas)

def Secante(func, x0, x1, delta, n, arquivo_saida):
    f0 = func(x0)
    f1 = func(x1)
    tabelas = []
    k = 0
    while k < n and abs(x1 - x0) > delta:
        k += 1
        if f1 - f0 == 0:
            print("\nMétodo da Secante: Divisão por zero.")
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        tabelas.append([k, x0, x1, f0, f1, x2, func(x2)])
        if abs(func(x2)) < delta or abs(x2 - x1) < delta:
            salvar_tabela_antes(arquivo_saida, "Secante", k, x2)
            break
        x0, x1 = x1, x2
        f0, f1 = f1, func(x2)
    if (k==n):
        salvar_tabela_caso(arquivo_saida, "Secante", k, x2)
    salvar_tabela(arquivo_saida, "Secante", ["k", "x0", "x1", "f(x0)", "f(x1)", "x2", "f(x2)"], tabelas)

def RegulaFalsi(func, a, b, delta, n, arquivo_saida):
    fa = func(a)
    fb = func(b)
    if fa * fb > 0:
        with open(arquivo_saida, "a", encoding="utf-8") as f:
            f.write(f'Método: RegulaFalsi: Intervalo inválido')
        return
    tabelas = []
    k = 0
    while k < n:
        k += 1
        x = (a * fb - b * fa) / (fb - fa)
        fx = func(x)
        tabelas.append([k, a, b, fa, fb, x, fx])
        if abs(fx) < delta or abs(b - a) < delta:
            salvar_tabela_antes(arquivo_saida, "RegulaFalsi", k, x)
            break
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
    if (k==n):
        salvar_tabela_caso(arquivo_saida, "RegulaFalsi", k, x)
    salvar_tabela(arquivo_saida, "RegulaFalsi", ["k", "a", "b", "fa", "fb", "x", "f(x)"], tabelas)

if __name__ == "__main__":
    # ler parâmetros do arquivo
    params = ler_parametros("./arquivos/funcao_arquivo.txt")

    # criar as funções
    funcao = lerFuncao(params["funcao"])
    a = params["a"]
    b = params["b"]
    delta = params["delta"]
    n = params["n"]
    phi = lerFuncao(params["phi"]) if "phi" in params else None
    dfuncao = lerFuncao(params["dfuncao"]) if "dfuncao" in params else None
    x0 = params.get("x0", (a+b)/2)

    # abre o arquivo de relatorio
    arquivo_saida = "./arquivos/iteracoes_funcoes.txt"
    open(arquivo_saida, "w").close()

    # executa os métodos
    Bisseccao(funcao, a, b, delta, n, arquivo_saida)
    if phi:
        Mil(funcao, phi, x0, delta, n, arquivo_saida)
    if dfuncao:
        NewtonRaphson(funcao, dfuncao, x0, delta, n, arquivo_saida)
    Secante(funcao, a, b, delta, n, arquivo_saida)
    RegulaFalsi(funcao, a, b, delta, n, arquivo_saida)


