import csv
from algoritmos_otimizacao import pesquisa_aleatoria, subida_encosta, tempera_simulada, genetico

dormitorios = ["São Paulo", "Flamengo", "Coritiba", "Cruzeiro", "Fortaleza"]

preferencias = [("Amanda", ("Cruzeiro", "Coritiba")),
                ("Pedro", ("São Paulo", "Fortaleza")),
                ("Marcos", ("Flamengo", "São Paulo")),
                ("Priscila", ("São Paulo", "Fortaleza")),
                ("Jessica", ("Flamengo", "Cruzeiro")),
                ("Paulo", ("Coritiba", "Fortaleza")),
                ("Fred", ("Fortaleza", "Flamengo")),
                ("Suzana", ("Cruzeiro", "Coritiba")),
                ("Laura", ("Cruzeiro", "Coritiba")),
                ("Ricardo", ("Coritiba", "Flamengo"))
                ]

def imprimir_solucao(_solucao):
    vagas = []
    for i in range(len(dormitorios)):
        vagas += [i, i] # Duas vagas para cada dormitório
    for i in range(len(_solucao)):
        atual = _solucao[i]
        dormitorio = dormitorios[vagas[atual]] # Atribui o nome do dormitório com base na solução
        print(preferencias[i][0], dormitorio)
        del vagas[atual] # Para duas ou mais pessoas não serem alocadas na mesma vaga

def funcao_custo(_solucao):
    custo = 0
    vagas = [0,0,1,1,2,2,3,3,4,4] # Duas vagas para cada dormitório (5 dormitórios)
    for i in range(len(_solucao)):
        atual = _solucao[i]
        dormitorio = dormitorios[vagas[atual]] # Atribui o nome do dormitório com base na solução
        preferencia = preferencias[i][1] # Pega a lista de duas preferências da pessoa i
        if preferencia[0] == dormitorio: # Se for a primeira preferência da pessoa
            custo += 0 # Não aplica penalidade
        elif preferencia[1] == dormitorio: # Se for a segunda preferência da pessoa
            custo += 1 # 1 de penalidade
        else: # Se não for nem a primeira, nem a segunda
            custo += 3 # 3 de penalidade
        del vagas[atual] # Para duas ou mais pessoas não serem alocadas na mesma vaga
    return custo

if __name__ == "__main__":
    # Domínio > indica os valores mínimos e máximos
    dominio = [(0, (len(dormitorios) * 2) - i - 1) for i in range(0, len(dormitorios) * 2)]  # Domínio [(0, 9), (0, 8), (0, 7)...]

    print("\033[31m\033[1mOtimização Dormitórios\033[0m")

    print("-" * 50)

    print("\033[35m\033[1mPesquisa Randômica\033[0m")
    solucao_aleatoria = pesquisa_aleatoria(dominio, funcao_custo)
    custo_aleatoria = funcao_custo(solucao_aleatoria)
    imprimir_solucao(solucao_aleatoria)
    print(f"Penalidade: {custo_aleatoria}")

    print("-" * 50)

    print("\033[36m\033[1mSubida da Encosta + Pesquisa Randômica\033[0m")
    solucao_subida_encosta = subida_encosta(dominio, funcao_custo, hibrido=True)  # Hibrida para usar o resultado de uma pesquisa randômica como solução inicial
    custo_subida_encosta = funcao_custo(solucao_subida_encosta)
    imprimir_solucao(solucao_subida_encosta)
    print(f"Penalidade: {custo_subida_encosta}")

    print("-" * 50)

    print("\033[34m\033[1mTêmpera Simulada\033[0m")
    solucao_tempera = tempera_simulada(dominio, funcao_custo)
    custo_tempera = funcao_custo(solucao_tempera)
    imprimir_solucao(solucao_tempera)
    print(f"Penalidade: {custo_tempera}")

    print("-" * 50)

    print("\033[32m\033[1mAlgoritmo Genético\033[0m")
    solucao_genetico = genetico(dominio, funcao_custo)
    custo_genetico = funcao_custo(solucao_genetico)
    imprimir_solucao(solucao_genetico)
    print(f"Penalidade: {custo_genetico}")

    # Transforma o resultado de X execuções dos 5 algoritmos (4 + subida_encosta_hibrida) e gera um arquivo csv com os resultados dos custos
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
    # with open("comparacao_cem_dormitorios.csv", 'w') as f:
    #     write = csv.writer(f)
    #     write.writerow(csv_labels)
    #     for i in range(qte):
    #         write.writerows([[cem_pesquisa_aleatoria[i],
    #                          cem_subida_encosta[i],
    #                          cem_subida_encosta_mais_pesquisa_aleatoria[i],
    #                          cem_tempera_simulada[i],
    #                          cem_algoritmo_genetico[i]
    #                         ]])