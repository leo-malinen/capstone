from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt

class TrafficCanvas(QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent)
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off') 

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.pos = None

    def draw_network(self, graph, current_time=0):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_title(f"Simulation Time: {current_time:.2f}")

        if self.pos is None:
            self.pos = nx.spring_layout(graph, seed=42)

        node_colors = ['gray' for _ in graph.nodes()] 
        nx.draw_networkx_nodes(graph, self.pos, ax=self.ax, node_size=300, node_color=node_colors)

        edge_colors = []
        for u, v in graph.edges():
            if graph[u][v].get('blocked', False):
                edge_colors.append('red')
            else:
                edge_colors.append('black')
        
        nx.draw_networkx_edges(graph, self.pos, ax=self.ax, edge_color=edge_colors, arrows=True)
        
        vehicle_x = []
        vehicle_y = []
        
        for u, v in graph.edges():
            vehicles = graph[u][v].get('vehicles', [])
            if vehicles:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                
                for _ in vehicles:
                    vehicle_x.append(mid_x)
                    vehicle_y.append(mid_y)

        if vehicle_x:
            self.ax.scatter(vehicle_x, vehicle_y, c='blue', s=20, zorder=5, label='Cars')

        self.canvas.draw()
