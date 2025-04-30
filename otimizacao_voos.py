import csv
import time, random, math

pessoas = [("Amanda", "CWB"),
           ("Pedro", "GIG"),
           ("Marcos", "POA"),
           ("Priscila", "FLN"),
           ("Jessica", "CNF"),
           ("Paulo", "GYN")
          ]
destino = "GRU"

voos = {} # Dicionário no formato {(origem, destino): [(saida, chegada, preco)]}
for linha in open("voos.txt", "r"): # Abre o arquivo de voos e lê linha por linha
    _origem, _destino, _saida, _chegada, _preco = linha.split(",") # Separa as linhas pelo delimitador e atribui às suas respectivas variáveis
    voos.setdefault((_origem, _destino), [])
    voos[(_origem, _destino)].append((_saida, _chegada, int(_preco)))


# [1,4, 3,2, 7,3, 6,3, 2,4, 5,3] exemplo de agenda, separado por pares para cada pessoa (id_voo_ida, id_voo_volta)
# A obtenção da agenda é feita com os algoritmos de otimização, essa função apenas imprime
def imprimir_agenda(agenda):
    id_voo = -1
    for i in range(len(agenda) // 2): # // 2 para separar em pares para cada pessoa, são 6 nessa situação
        nome = pessoas[i][0] # Pessoa o nome da lista 'pessoas'
        origem = pessoas[i][1] # Pessoa a origem da lista 'pessoas'
        id_voo += 1 # +1 para apontar para o id_voo_ida da primeira pessoa
        ida = voos[(origem, destino)][agenda[id_voo]] # Retorna uma tupla ('hora_saida', 'hora_chegada', preco) para o voo de ida
        id_voo += 1 # +1 para apontar para o id_voo_volta da primeira pessoa
        volta = voos[(destino, origem)][agenda[id_voo]] # Retorna uma tupla ('hora_saida', 'hora_chegada', preco) para o voo de volta
        print(f"{nome:<10} {origem:<5} {ida[0]:>5}-{ida[1]:<5} R${ida[2]:<5} {volta[0]:>5}-{volta[1]:>5} R${volta[2]:<5}") # imprime em formato de tabela


# Transforma uma string hora em minutos '02:20' > 140 min
def get_minutos(hora):
    x = time.strptime(hora, "%H:%M") # strptime transforma string de hora em um objeto do tipo time.struct_type
    minutos = x[3] * 60 + x[4] # x[3] retorna as horas, x[4] retorna os minutos
    return minutos


# 'solucao' é uma lista como a agenda, com 12 valores, 2 para cada pessoa (id_ida, id_volta)
# [1,4, 3,2, 7,3, 6,3, 2,4, 5,3] exemplo de agenda, separado por pares para cada pessoa (id_voo_ida, id_voo_volta)
def funcao_custo(solucao):
    preco_total = 0
    ultima_chegada = 0 # Atribui o menor valor possível
    primeira_partida = 1439 # Atribui o maior valor possível 1439 > 23:59

    id_voo = -1
    for i in range(len(solucao) // 2): # // 2 para separar em pares para cada pessoa, são 6 nessa situação
        origem = pessoas[i][1]
        id_voo += 1 # +1 para apontar para o id_voo_ida da primeira pessoa
        ida = voos[(origem, destino)][solucao[id_voo]] # Retorna uma tupla ('hora_saida', 'hora_chegada', preco) para o voo de ida
        id_voo += 1  # +1 para apontar para o id_voo_volta da primeira pessoa
        volta = voos[(destino, origem)][solucao[id_voo]] # Retorna uma tupla ('hora_saida', 'hora_chegada', preco) para o voo de volta

        preco_total += ida[2] # Retorna o valor do voo de ida
        preco_total += volta[2]  # Retorna o valor do voo de volta

        if ultima_chegada < get_minutos(ida[1]): # Compara para pegar o maior valor de chegada
            ultima_chegada = get_minutos(ida[1]) # ida[1] retorna o valor de chegada do voo de ida

        if primeira_partida > get_minutos(volta[0]): # Compara para pegar o menor valor de partida
            primeira_partida = get_minutos(volta[0]) # volta[0] retorna o valor de saida do voo de volta

    total_espera = 0
    id_voo = -1
    for i in range(len(solucao) // 2):
        origem = pessoas[i][1]
        id_voo += 1  # +1 para apontar para o id_voo_ida da primeira pessoa
        ida = voos[(origem, destino)][solucao[id_voo]]  # Retorna uma tupla ('hora_saida', 'hora_chegada', preco) para o voo de ida
        id_voo += 1  # +1 para apontar para o id_voo_volta da primeira pessoa
        volta = voos[(destino, origem)][solucao[id_voo]]  # Retorna uma tupla ('hora_saida', 'hora_chegada', preco) para o voo de volta

        total_espera += ultima_chegada - get_minutos(ida[1]) # Calcula, para cada pessoa, a diferença (tempo de espera), em relação à pessoa que chegou por último
        total_espera += get_minutos(volta[0]) - primeira_partida # Calcula, para cada pessoa, a diferença (tempo de espera), em relação à pessoa que saiu primeiro

    if ultima_chegada > primeira_partida: # Penalidade caso a volta seja no dia seguinte a chegada
        preco_total += 50

    return preco_total + total_espera


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

if __name__ == "__main__":
    dominio = [(0, 9)] * (len(pessoas) * 2) # Valores mínimos e máximos permitidos, nesse caso 0-9, pois são 10 voos

    print("\033[35m\033[1mPesquisa Randômica\033[0m")
    solucao_aleatoria = pesquisa_aleatoria(dominio, funcao_custo)
    custo_aleatoria = funcao_custo(solucao_aleatoria)
    imprimir_agenda(solucao_aleatoria)
    print(f"Custo: R${custo_aleatoria}")

    print("-" * 50)

    print("\033[36m\033[1mSubida da Encosta + Pesquisa Randômica\033[0m")
    solucao_subida_encosta = subida_encosta(dominio, funcao_custo, hibrido=True) # Hibrida para usar o resultado de uma pesquisa randômica como solução inicial
    custo_subida_encosta = funcao_custo(solucao_subida_encosta)
    imprimir_agenda(solucao_subida_encosta)
    print(f"Custo: R${custo_subida_encosta}")

    print("-" * 50)

    print("\033[34m\033[1mTêmpera Simulada\033[0m")
    solucao_tempera = tempera_simulada(dominio, funcao_custo)
    custo_tempera = funcao_custo(solucao_tempera)
    imprimir_agenda(solucao_tempera)
    print(f"Custo: R${custo_tempera}")

    print("-" * 50)

    print("\033[32m\033[1mAlgoritmo Genético\033[0m")
    solucao_genetico = genetico(dominio, funcao_custo)
    custo_genetico = funcao_custo(solucao_genetico)
    imprimir_agenda(solucao_genetico)
    print(f"Custo: R${custo_genetico}")


    # transforma o resultado de X execuções dos 5 algoritmos (4 + subida_encosta_hibrida) e gera um arquivo csv com os resultados dos custos
    # qte = 100
    # cem_pesquisa_aleatoria = []
    # cem_subida_encosta = []
    # cem_subida_encosta_mais_pesquisa_aleatoria = []
    # cem_tempera_simulada = []
    # cem_algoritmo_genetico = []
    #
    # csv_labels = ["Pesquisa Aleatória", "Subida da Encosta", "Subida da Encosta + Pesquisa Aleatória", "Têmpera Simulada", "Algoritmo Genético"]
    #
    # for i in range(qte):
    #     cem_pesquisa_aleatoria.append(funcao_custo(pesquisa_aleatoria(dominio, funcao_custo)))
    #     cem_subida_encosta.append(funcao_custo(subida_encosta(dominio, funcao_custo)))
    #     cem_subida_encosta_mais_pesquisa_aleatoria.append(funcao_custo(subida_encosta(dominio, funcao_custo, hibrido=True)))
    #     cem_tempera_simulada.append(funcao_custo(tempera_simulada(dominio, funcao_custo)))
    #     cem_algoritmo_genetico.append(funcao_custo(genetico(dominio, funcao_custo)))
    #     print(f"{(i+1)/qte*100:.1f}%")
    # with open("comparacao_resultado_custos.csv", 'w') as f:
    #     write = csv.writer(f)
    #     write.writerow(csv_labels)
    #     for i in range(qte):
    #         write.writerows([[cem_pesquisa_aleatoria[i],
    #                          cem_subida_encosta[i],
    #                          cem_subida_encosta_mais_pesquisa_aleatoria[i],
    #                          cem_tempera_simulada[i],
    #                          cem_algoritmo_genetico[i]
    #                         ]])