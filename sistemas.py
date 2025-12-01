import numpy as np
import os
import math
import copy
import time

# ler arquivo Ax = b
def ler_sistema(nome_arquivo):
    with open(nome_arquivo, "r") as f:
        linhas = f.readlines()

    # b é a ultima linha
    b = list(map(float, linhas[-1].split()))

    A = [list(map(float, linha.split())) for linha in linhas[:-1]]

    return A, b

# ler arquivo Ax
def ler_A(nome_arquivo):
    with open(nome_arquivo, "r") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    A = [list(map(float, linha.split())) for linha in linhas]
    return A

# ler arquivo b
def ler_b(nome_arquivo):
    with open(nome_arquivo, "r") as f:
        linha = f.readline().strip()

    b = list(map(float, linha.split()))
    return b
    
# Gauss
def gauss(A, b):
    n = len(A)

    # linha do pivo
    for k in range(n-1):
        pivo = A[k][k]
        if pivo == 0:
            raise ValueError("Pivo zero em Gauss")
        
        # linha a ser zerada
        for i in range(k+1, n):
            m = A[i][k] / pivo
            # coluna
            for j in range(n):
                A[i][j] -= m*A[k][j]
                A[i][j] = float(A[i][j])

            b[i] -= m*b[k]
            b[i] = float(b[i])
    
    # descobrir valores de x
    x = np.zeros(n)
    x[-1] = b[-1] / A[-1][-1]
    
    for i in range(n-2, -1, -1):  # n-2 ate 0
        soma = 0
        for j in range(i+1, n):
            soma += A[i][j] * x[j]

        x[i] = (b[i] - soma) / A[i][i]

    return x

def gauss_pivoteamento_parcial(A, b):
    n = len(A)

    # linha do pivo
    for k in range(n-1):
        pivo = A[k][k]
        maior_valor = abs(pivo)
        linha_pivo = k

        # procura o maior valor
        for aux in range(k+1, n):
            if abs(A[aux][k]) > maior_valor:
                maior_valor = abs(A[aux][k])
                linha_pivo = aux
        
        # trocar linhas
        if k != linha_pivo:
            for aux in range(n):
                temp = A[linha_pivo][aux]
                temp2 = A[k][aux]
                A[k][aux] = temp
                A[linha_pivo][aux] = temp2
            
            tempB = b[linha_pivo]
            b[linha_pivo] = b[k]
            b[k] = tempB

        if maior_valor == 0:
            raise ValueError("Coluna do pivo zerada, não é possível resolver por Método de Gauss Pivoteamento Parcial")

        # linha a ser zerada
        for i in range(k+1, n):
            pivo = A[k][k]
            m = A[i][k] / pivo
            # coluna
            for j in range(n):
                A[i][j] -= m*A[k][j]
                A[i][j] = float(A[i][j])

            b[i] -= m*b[k]
            b[i] = float(b[i])
    
    # descobrir valores de x
    x = np.zeros(n)
    x[-1] = b[-1] / A[-1][-1]
    
    for i in range(n-2, -1, -1):  # n-2 ate 0
        soma = 0
        for j in range(i+1, n):
            soma += A[i][j] * x[j]

        x[i] = (b[i] - soma) / A[i][i]

    return x

def gauss_pivoteamento_completo(A, b):
    n = len(A)
    coluna_indices = np.array(range(n))

    # linha do pivo
    for k in range(n-1):
        pivo = A[k][k]
        maior_valor = abs(pivo)
        linha_pivo = k
        coluna_pivo = k

        # procura o maior valor
        for i in range(k, n):
            for j in range(k, n):
                if abs(A[i][j]) > maior_valor:
                    maior_valor = abs(A[i][j])
                    linha_pivo = i
                    coluna_pivo = j
        
        # trocar linhas
        if k != linha_pivo:
            for aux in range(n):
                temp = A[linha_pivo][aux]
                temp2 = A[k][aux]
                A[k][aux] = temp
                A[linha_pivo][aux] = temp2
            
            tempB = b[linha_pivo]
            b[linha_pivo] = b[k]
            b[k] = tempB

        # trocar colunas
        if coluna_pivo != k:
            for aux in range(n):
                temp = A[aux][k]
                A[aux][k] = A[aux][coluna_pivo]
                A[aux][coluna_pivo] = temp
            
            temp = coluna_indices[coluna_pivo]
            temp2 = coluna_indices[k]
            coluna_indices[k] = temp
            coluna_indices[coluna_pivo] = temp2

        if maior_valor == 0:
            raise ValueError("Não é possível resolver a matriz")

        # linha a ser zerada
        for i in range(k+1, n):
            pivo = A[k][k]
            m = A[i][k] / pivo
            # coluna
            for j in range(n):
                A[i][j] -= m*A[k][j]
                A[i][j] = float(A[i][j])

            b[i] -= m*b[k]
            b[i] = float(b[i])
    
    # descobrir valores de x
    x = np.zeros(n)
    x[-1] = b[-1] / A[-1][-1]
    
    for i in range(n-2, -1, -1):  # n-2 ate 0
        soma = 0
        for j in range(i+1, n):
            soma += A[i][j] * x[j]

        x[i] = (b[i] - soma) / A[i][i]


    # coloca em ordem
    x_corrigido = np.zeros(n)

    for i in range(n):
        pos_original = coluna_indices[i]
        x_corrigido[pos_original] = x[i]

    return x_corrigido

def decomposicao_LU(A, b):
    n = len(A)
    L = np.eye(n) # cria matriz identidade
    m_valores = np.eye(n)

    # zerar linhas, mesmo parte de código de gauss, mas armazena o valor m
    for k in range(n-1):
        pivo = A[k][k]
        if pivo == 0:
            raise ValueError("Pivo zero em Gauss")

        # linha a ser zerada
        for i in range(k+1, n):
            m = A[i][k] / pivo
            L[i][k] = m

            # coluna
            for j in range(n):
                A[i][j] -= m * A[k][j]
                A[i][j] = float(A[i][j])

    ## A se tornou U
    ## L ja recebeu valores de -(m)
    U = A

    # resolver Ly = b
    y = np.zeros(n)
    
    for i in range(n):
        soma = 0
        for j in range(0, i):
            soma += L[i][j] * y[j]

        y[i] = (b[i] - soma) / L[i][i]

    # resolver Ux = y
    x = np.zeros(n)
    x[-1] = y[-1] / A[-1][-1]
    
    for i in range(n-2, -1, -1):  # n-2 ate 0
        soma = 0
        for j in range(i+1, n):
            soma += U[i][j] * x[j]

        x[i] = (y[i] - soma) / U[i][i]

    return x

def cholesky(A, b):
    n = len(A)
    L = np.zeros((n, n))

    #verifica simetrica
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != A[j][i]:
                raise ValueError("Matriz não é simétrica")

    ## criar L
    # percorrer diagonal inferior
    for i in range(n):
        for j in range(i+1):
            soma = 0

            for k in range(j):
                soma += L[i][k] * L[j][k]

            if i == j:
                # diagonal
                valor = A[i][i] - soma
                if valor <= 0:
                    raise ValueError("Matriz não é definida positiva.")
                L[i][j] = math.sqrt(valor)
            else:
                # fora da diagonal
                L[i][j] = (A[i][j] - soma) / L[j][j]    

    # Ly = b inferior
    y = np.zeros(n)
    for i in range(n):
        soma = 0.0
        for j in range(i):
            soma += L[i][j] * y[j]
        y[i] = (b[i] - soma) / L[i][i]
    
    # L(transposta)x = y
    # muda os indices para ser superior
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = 0.0
        for j in range(i+1, n):
            soma += L[j][i] * x[j] 
        x[i] = (y[i] - soma) / L[i][i]
    
    return x


def gaussJacobi(A, b, n, delta, parada):
    tam = len(b)
    x = np.zeros(tam) # chute inicial 

    # critério de convergencia
    for i in range(tam):
        diag = abs(A[i][i])

        soma = 0
        for j in range(tam):
            if j != i:
                soma += abs(A[i][j])

        if diag <= soma:
            raise ValueError(f"Critério de convergência não satisfeito.")

    # loop de iterações
    for k in range(n): 
        x_old = x.copy() # valor de x x^(k-1)

        for i in range(tam):
            # soma elementos da linha menos o pivo
            soma = 0
            for j in range(tam):
                if j != i:
                    soma += A[i][j] * x_old[j]

            # formula
            x[i] = (b[i] - soma) / A[i][i]

        if parada == 'Erro Absoluto':
            erro = 0
            for i in range(tam):
                diferenca = abs(x[i] - x_old[i])
                if diferenca > erro:
                    erro = diferenca

            if erro < delta:
                return x, k+1

        elif parada == 'Erro Relativo':
            erro = 0
            for i in range(tam):
                if x[i] != 0:
                    diferenca = abs((x[i] - x_old[i]) / x[i])
                    if diferenca > erro:
                        erro = diferenca

            if erro < delta:
                return x, k+1

    raise ValueError("Gauss-Jacobi não convergiu dentro do número máximo de iterações.")


def gaussSeidel(A, b, n, delta, parada):
    A = copy.deepcopy(A)
    b = copy.deepcopy(b)
    sassenfeld = []

    tam = len(b)
    x = np.zeros(tam) # chute inicial

    # criterio de convergência sassenfeld
    for i in range(tam):
        soma = 0
        for j in range(tam):
            if j < i:
                soma += abs(A[i][j]) * sassenfeld[j]
            elif j > i:
                soma += abs(A[i][j])

        fator = soma / abs(A[i][i])
        sassenfeld.append(fator)

    if max(sassenfeld) >= 1:
        raise ValueError("Critério de Sassenfeld não satisfeito.")

    # iterações
    for k in range(n):
        x_old = x.copy() # guardar valores

        for i in range(tam):
            # somar valores atualizados antes da diagonal
            soma1 = 0
            for j in range(i):
                soma1 += A[i][j] * x[j]

            # somar valores antigos depois da diagonal
            soma2 = 0
            for j in range(i + 1, tam):
                soma2 += A[i][j] * x_old[j]

            # formula
            x[i] = (b[i] - soma1 - soma2) / A[i][i]

        # Erro Absoluto
        if parada == "Erro Absoluto":
            erro = 0
            for i in range(tam):
                diferenca = abs(x[i] - x_old[i])
                if diferenca > erro:
                    erro = diferenca
            if erro < delta:
                return x, k+1

        # Erro Relativo
        elif parada == "Erro Relativo":
            erro = 0
            for i in range(tam):
                if x[i] != 0:
                    diferenca_rel = abs((x[i] - x_old[i]) / x[i])
                    if diferenca_rel > erro:
                        erro = diferenca_rel
            if erro < delta:
                return x, k+1

    raise ValueError("Gauss-Seidel não convergiu dentro do número máximo de iterações.")


if __name__ == "__main__":
    arquivo_saida = './arquivos/resultado_sistema'

    A, b = ler_sistema("./arquivos/sistema_arquivo.txt")

    # A = ler_A("./arquivos/ler_A.txt")
    # b = ler_b("./arquivos/ler_b.txt")

    x = np.linalg.solve(copy.deepcopy(A), copy.deepcopy(b))
    print("Solução:", x)

    # x = gauss(copy.deepcopy(A), copy.deepcopy(b))
    # print("Gauss: ", x)

    # x = gauss_pivoteamento_parcial(copy.deepcopy(A), copy.deepcopy(b))
    # print("Gauss Pivoteamento Parcial: ", x)

    # x = gauss_pivoteamento_completo(copy.deepcopy(A), copy.deepcopy(b))
    # print("Gauss Pivoteamento Completo: ", x)

    # x = decomposicao_LU(copy.deepcopy(A), copy.deepcopy(b))
    # print("Decomposição LU: ", x)

    x = cholesky(copy.deepcopy(A), copy.deepcopy(b))
    print("Cholesky: ", x)

    n = 50
    delta = 0.05

    x, k = gaussJacobi(copy.deepcopy(A), copy.deepcopy(b), n, delta, "Erro Absoluto")
    print("Gauss Jacobi: ", x, k)

    x, k = gaussSeidel(copy.deepcopy(A), copy.deepcopy(b), n, delta, "Erro Relativo")
    print("Gauss Seidel: ", x, k)
