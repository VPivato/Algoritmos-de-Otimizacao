import math, random

# Retorna a melhor solução (lista agenda) após verificar x soluções aleatórias
# Uma pesquisa totalmente aleatória, não aproveita as boas soluções encontradas
def pesquisa_aleatoria(_dominio, _funcao_custo):
    melhor_custo = 999999 # Inicializa com um valor alto
    melhor_solucao = []
    for i in range(0, 10000):
        solucao = [random.randint(_dominio[i][0], _dominio[i][1]) for i in range(len(_dominio))] # Gera uma lista 'agenda' como [1,4, 3,2, 7,3, 6,3, 2,4, 5,3] aleatoriamente
        custo = _funcao_custo(solucao) # Verifica o custo com base na função de custo
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao = solucao
    return melhor_solucao


# Começa com uma solução aleatória e procura os melhores vizinhos
# Funciona melhor se, em vez de uma solução randômica, usar o resultado da pesquisa aleatória
def subida_encosta(_dominio, _funcao_custo, hibrido=False):
    # Gera uma lista 'agenda' como [1,4, 3,2, 7,3, 6,3, 2,4, 5,3] aleatoriamente
    solucao = [random.randint(_dominio[i][0], _dominio[i][1]) for i in range(len(_dominio))] if not hibrido else pesquisa_aleatoria(_dominio, _funcao_custo)

    while True:
        vizinhos = []

        for i in range(len(_dominio)):
            if solucao[i] > _dominio[i][0]: # Dominio[i][0] == 0, serve para não quebrar os limites do domínio
                if solucao[i] != _dominio[i][1]: # Dominio[i][1] == 9, serve para não quebrar os limites do domínio
                    vizinhos.append(solucao[0:i] + [solucao[i] + 1] + solucao[i+1:]) # Adiciona uma lista agenda de [0:i], [i+1:] não modificada, e soma 1 no índice [i]

            if solucao[i] < _dominio[i][1]: # Dominio[i][1] == 9, serve para não quebrar os limites do domínio
                if solucao[i] != _dominio[i][0]: # Dominio[i][0] == 0, serve para não quebrar os limites do domínio
                    vizinhos.append(solucao[0:i] + [solucao[i] - 1] + solucao[i+1:]) # Adiciona uma lista agenda de [0:i], [i+1:] não modificada, e subtrai 1 no índice [i]

        atual = _funcao_custo(solucao)
        melhor = atual
        for i in range(len(vizinhos)): # Percorre todos os vizinhos
            custo = _funcao_custo(vizinhos[i])
            if custo < melhor: # Compara seus custos e salva o menor
                melhor = custo
                solucao = vizinhos[i]

        if melhor == atual: # Caso não seja possível diminuir o custo
            break # Sai do laço while
    return solucao


# Pode ser considerada uma melhoria do algoritmo de subida da encosta
# Pode ou não escolher um vizinho pior baseado em uma probabilidade que diminui a cada loop
def tempera_simulada(_dominio, _funcao_custo, _temperatura=10000, _resfriamento=0.95, _passo=1):
    solucao = [random.randint(_dominio[i][0], _dominio[i][1]) for i in range(len(_dominio))]
    while _temperatura > 0.1:
        i = random.randint(0, len(_dominio) - 1) # Gera um índice de 0 a 11
        direcao = random.choice([-_passo, _passo]) # Escolhe como modificar o índice baseado no parâmetro passo

        solucao_temp = solucao[:] # Faz uma cópia da solução
        solucao_temp[i] += direcao # Modifica o índice conforme a direção escolhida aleatóriamente

        if solucao_temp[i] < _dominio[i][0]: # Segurança para o valor não ultrapassar os limites de 0-9 (definido pela quantidade de voos no dia)
            solucao_temp[i] = _dominio[i][0] # _dominio[i][0] == 0
        elif solucao_temp[i] > _dominio[i][1]: # Segurança para o valor não ultrapassar os limites de 0-9 (definido pela quantidade de voos no dia)
            solucao_temp[i] = _dominio[i][1] # _dominio[i][0] == 9

        custo_solucao = _funcao_custo(solucao)  # Gera custo para a solução e solução_temp
        custo_solucao_temp = _funcao_custo(solucao_temp)
        probabilidade = pow(math.e, (-custo_solucao_temp - custo_solucao) / _temperatura) # Fórmula usada no algoritmo, diminui a cada iteração

        if custo_solucao_temp < custo_solucao or random.random() < probabilidade:
            solucao = solucao_temp
        _temperatura *= _resfriamento
    return solucao


# A partir de uma solução, gera um mutante, alterando apenas um gene
# A partir de uma lista, gera outra lista, alterando apenas um índice
def mutacao(_dominio, _solucao, _passo=1):
    i = random.randint(0, len(_dominio) - 1) # Gera um índice para modificar
    mutante = _solucao[:]

    if random.random() < 0.5: # 50% de chance de -1 no índice
        if _solucao[i] != _dominio[i][0]: # Segurança para o valor não ultrapassar os limites de 0-9 (definido pela quantidade de voos no dia)
            mutante[i] -= -_passo
    else: # 50% de chance de +1 no índice
        if _solucao[i] != _dominio[i][1]: # Segurança para o valor não ultrapassar os limites de 0-9 (definido pela quantidade de voos no dia)
            mutante[i] += -_passo
    return mutante


# A partir do cruzamento de dois indivíduos, gera um novo indivíduo com base em um ponto de corte aleatório
# A partir da junção de duas listas, retorna uma nova lista contendo partes das duas (ponto de corte)
def cruzamento(_dominio, _individuo1, _individuo2):
    i = random.randint(1, len(_dominio) -2 ) # Ponto de corte para geração do cruzamento, não pode ser cortado na posição 0 ou máxima
    return _individuo1[0:i] + _individuo2[i:] # Concatena as listas


# Implementação do algoritmo genético
# tamanho_populacao > quantos indivíduos serão gerados inicialmente, feito de forma randômica
# elitismo > porcentagem dos indivíduos (apenas os melhores) que serão escolhidos para a próxima geração
def genetico(_dominio, _funcao_custo, _tamanho_populacao=50, _passo=1, _probabilidade_mutacao=0.2, _elitismo=0.2, _numero_geracoes=100):
    populacao = []
    custos = []
    for i in range(_tamanho_populacao): # Criação da população com base na quantidade definida
        solucao = [random.randint(_dominio[i][0], _dominio[i][1]) for i in range(len(_dominio))]
        populacao.append(solucao)

    numero_elitismo = int(_elitismo * _tamanho_populacao) # Quantos indivíduos serão selecionados

    for i in range(_numero_geracoes):
        custos = [(_funcao_custo(individuo), individuo) for individuo in populacao] # Adiciona um índice (custo, individuo) para cada indivíduo da população
        custos.sort() # Do menor apara o maior (crescente)
        individuos_ordenados = [individuo for (custo, individuo) in custos] # Cria uma lista com apenas os indivíduos ordenados de maneira crescente

        populacao = individuos_ordenados[0:numero_elitismo] # Reescreve a população com os melhores X indivíduos

        while len(populacao) < _tamanho_populacao: # Repopula a variável população através do cruzamento ou mutação entre indivíduos, com base nos X melhores
            if random.random() < _probabilidade_mutacao: # Caso a probabilidade de mutação seja satisfeita
                m = random.randint(0, numero_elitismo) # Seleciona um índice da lista de indivíduos_ordenados conforme o numero_elitismo 0-máx
                populacao.append(mutacao(_dominio, individuos_ordenados[m], _passo=-_passo)) # Adiciona à população esse indivíduo mutado
            else: # Caso contrário
                c1 = c2 = 0
                while c1 == c2: # Evita selecionar o mesmo indivíduo
                    c1 = random.randint(0, numero_elitismo) # Seleciona dois indivíduos para o cruzamento
                    c2 = random.randint(0, numero_elitismo)
                populacao.append(cruzamento(_dominio, individuos_ordenados[c1], individuos_ordenados[c2]))

    return custos[0][1] # Retorna o melhor indivíduo da população após todas as gerações