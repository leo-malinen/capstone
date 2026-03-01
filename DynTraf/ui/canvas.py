import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class TrafficCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig = Figure()
        self.background_color = '#a3c9a8'
        self.fig.patch.set_facecolor(self.background_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.pos = None
        self.district_colors = {
            'Residential': '#5a9367', 'Commercial': '#5fa8d3',
            'Industrial': '#f4a261', 'Downtown': '#9d4edd', 'Unknown': 'gray'
        }

    def draw_network(self, graph, current_time=0, style='Straight'):
        self.ax.clear()
        self.ax.axis('off')
        self.fig.patch.set_facecolor(self.background_color)
        self.ax.set_facecolor(self.background_color)
        
        self.ax.text(0.88, 0.98, "Time: ", transform=self.ax.transAxes, 
                     color='black', fontsize=12, fontweight='bold', ha='right', va='top')
        self.ax.text(0.88, 0.98, f"{current_time:.1f}", transform=self.ax.transAxes, 
                     color='white', fontsize=12, fontweight='bold', ha='left', va='top')

        if graph.graph.get('type') == 'sample':
            self.pos = nx.spring_layout(graph, seed=42) 
        else:
            self.pos = {n: (n[0], n[1]) for n in graph.nodes()} 

        node_colors = [self.district_colors.get(graph.nodes[n].get('district', 'Unknown'), 'gray') 
                       for n in graph.nodes()]
        nx.draw_networkx_nodes(graph, self.pos, ax=self.ax, node_size=150, node_color=node_colors)      
        edge_colors = ['#d62828' if graph[u][v].get('blocked') else '#22223b' for u, v in graph.edges()]      
        conn_style = 'arc3,rad=0.15' if style == 'Curved' else 'arc3,rad=0.0'  
        nx.draw_networkx_edges(graph, self.pos, ax=self.ax, edge_color=edge_colors, 
                               width=1.5, connectionstyle=conn_style)
        
        car_x, car_y = [], []
        for u, v in graph.edges():
            if graph[u][v].get('vehicles'):
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                car_x.append((x1+x2)/2)
                car_y.append((y1+y2)/2)
        
        if car_x:
            self.ax.scatter(car_x, car_y, c='#ffffff', edgecolors='black', s=45, zorder=5) 
        
        self.canvas.draw()
