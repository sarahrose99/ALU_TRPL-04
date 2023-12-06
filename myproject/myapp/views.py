from django.shortcuts import render
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Gunakan backend 'Agg' untuk matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64

# Fungsi untuk menggambar graf
def draw_graph(G, pos=None):
    plt.figure()
    plt.clf()

    if pos is None:
        pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', font_size=12)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title('Graf Jaringan')

    # Mengubah plot menjadi gambar PNG dalam bentuk string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = urllib.parse.quote(base64.b64encode(img.read()).decode())
    img.close()
    
    return plot_url  # Mengembalikan URL gambar untuk ditampilkan di template

# Fungsi untuk mencari jalur terpendek
def shortest_path_decrease_conquer(G, start_node, end_node):
    stack = [(start_node, [start_node])]
    shortest_distance = float('inf')
    shortest_path = []

    while stack:
        current_node, path = stack.pop()

        if current_node == end_node:
            distance = sum(G.get_edge_data(path[i], path[i+1])['weight'] for i in range(len(path)-1))
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_path = path

        for neighbor in G.neighbors(current_node):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return shortest_path, shortest_distance

def index(request):
    G = nx.Graph()
    edges = [
        ('Jakarta', 'Bandung', 150), ('Jakarta', 'Surabaya', 700), ('Bandung', 'Yogyakarta', 450),
        ('Yogyakarta', 'Semarang', 150), ('Surabaya', 'Malang', 100), ('Malang', 'Yogyakarta', 350),
        ('Surabaya', 'Denpasar', 350), ('Denpasar', 'Semarang', 950), ('Yogyakarta', 'Medan', 1800),
        ('Medan', 'Semarang', 2100), ('Semarang', 'Denpasar', 1200)
    ]
    G.add_weighted_edges_from(edges)

    shortest_path = None
    shortest_distance = None

    if request.method == 'POST':
        start_node = request.POST.get('start_node')
        end_node = request.POST.get('end_node')

        shortest_path, shortest_distance = shortest_path_decrease_conquer(G, start_node, end_node)

    plot_url = draw_graph(G)

    return render(request, 'index.html', {'plot_url': plot_url, 'shortest_path': shortest_path, 'shortest_distance': shortest_distance})