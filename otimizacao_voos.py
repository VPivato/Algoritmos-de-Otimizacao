import csv
import time
from algoritmos_otimizacao import pesquisa_aleatoria, subida_encosta, tempera_simulada, genetico

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


if __name__ == "__main__":
    dominio = [(0, 9)] * (len(pessoas) * 2) # Valores mínimos e máximos permitidos, nesse caso 0-9, pois são 10 voos

    print("\033[31m\033[1mOtimização Voos\033[0m")

    print("-" * 50)

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
    # with open("comparacao_cem_voos.csv", 'w') as f:
    #     write = csv.writer(f)
    #     write.writerow(csv_labels)
    #     for i in range(qte):
    #         write.writerows([[cem_pesquisa_aleatoria[i],
    #                          cem_subida_encosta[i],
    #                          cem_subida_encosta_mais_pesquisa_aleatoria[i],
    #                          cem_tempera_simulada[i],
    #                          cem_algoritmo_genetico[i]
    #                         ]])