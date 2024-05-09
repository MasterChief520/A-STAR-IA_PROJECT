# PEDRO COSTA CALAZANS
# RENAN UNSONST CRUZ
# THALES HENRIQUE BASTOS NEVES

def read_graph_from_file(file_path):
    """
    Lê o grafo a partir de um arquivo e retorna uma lista de dicionários representando as arestas.
    Cada dicionário contém as chaves 'origin' (origem), 'destination' (destino) e 'cost' (custo).
    """
    with open(file_path, 'r') as file:
        graph = []
        for line in file:
            origin, destination, cost = line.strip().split(';')
            graph.append({
                'origin': origin,
                'destination': destination,
                'cost': int(cost)
            })
    return graph

def read_heuristic_from_file(file_path):
    """
    Lê a heurística a partir de um arquivo e retorna um dicionário com as cidades como chaves e os custos como valores.
    """
    with open(file_path, 'r') as file:
        heuristic = {}
        for line in file:
            city, cost = line.strip().split(';')
            heuristic[city] = int(cost)
    return heuristic

def print_final_path(final_cost):
    """
    Imprime a rota final e o custo total do melhor caminho encontrado.
    """
    print("Rota Final")
    print(f"O melhor caminho de {start_city} até {end_city} é de {final_cost}Km")

def print_options(current_node, open_nodes):
    """
    Imprime as opções disponíveis para o próximo nó a ser expandido, mostrando a cidade, o custo atual e a heurística.
    Também imprime a cidade selecionada com o custo total (custo atual + heurística).
    """
    print("\nOpções:")
    for node in open_nodes:
        print(f"{node['city']} {node['cost']} + {node['heuristic']} = {node['cost'] + node['heuristic']}")
    print(f"\nCidade Selecionada: {current_node['city']} ({current_node['cost'] + current_node['heuristic']})")
    print("-------------------------------")

def print_final_route():
    """
    Imprime a rota final encontrada, separando as cidades com " -> ".
    """
    print(" -> ".join(route))
    print("-------------------------------\n")

def expand_node(current_node):
    """
    Expande o nó atual, gerando os próximos nós possíveis com base nas arestas do grafo.
    Retorna uma lista de dicionários representando os novos nós, contendo a cidade, o custo atual e a heurística.
    """
    open_nodes = []
    if current_node is None:
        open_nodes.append({
            'city': start_city,
            'cost': 0,
            'heuristic': heuristic[start_city]
        })
    else:
        for edge in graph:
            if edge['origin'] == current_node['city']:
                open_nodes.append({
                    'city': edge['destination'],
                    'cost': edge['cost'] + current_node['cost'],
                    'heuristic': heuristic[edge['destination']]
                })
            elif edge['destination'] == current_node['city']:
                open_nodes.append({
                    'city': edge['origin'],
                    'cost': edge['cost'] + current_node['cost'],
                    'heuristic': heuristic[edge['origin']]
                })
    return open_nodes

def a_star_search(current_node=None, open_nodes=[]):
    """
    Realiza a busca A* para encontrar o melhor caminho entre a cidade de origem e a cidade de destino.
    Retorna a rota encontrada como uma lista de cidades.
    """
    current_city = None
    if current_node is not None:
        current_city = current_node['city']
        print_options(current_node, open_nodes)
        if current_node['city'] == end_city:
            print_final_path(current_node['cost'])
            return [end_city]
        open_nodes.remove(current_node)
    open_nodes += expand_node(current_node)
    best_node = min(open_nodes, key=lambda node: node['cost'] + node['heuristic'])
    path = a_star_search(best_node, open_nodes)
    for edge in graph:
        if (edge['origin'] == current_city and edge['destination'] == path[0]) or (edge['destination'] == current_city and edge['origin'] == path[0]):
            return [current_city] + path
    return path

# Caminhos dos arquivos
graph_file = 'Grafo.txt'
heuristic_file = 'Heuristica.txt'

# Lê os dados dos arquivos
graph = read_graph_from_file(graph_file)
heuristic = read_heuristic_from_file(heuristic_file)

# Cidades de origem e destino
start_city = "Arad"
end_city = "Bucareste"

# Executa a busca A* e imprime a rota final
route = a_star_search()
print_final_route()