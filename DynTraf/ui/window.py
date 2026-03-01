import config
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QComboBox)
from PyQt5.QtCore import QTimer
from ui.canvas import TrafficCanvas
from models.traffic_light import TrafficLight
from simulation.env_manager import SimulationManager

class MainWindow(QMainWindow):
    def __init__(self, net_builder, spawner_func, optimizer_class):
        super().__init__()
        self.net_builder = net_builder
        self.spawner_func = spawner_func
        self.optimizer_class = optimizer_class
        
        self.current_time = 0
        self.grid_style = 'Straight' # Default
        
        self.init_ui()
        self.setup_timer()
        self.reset_simulation() # Build the initial state

    def init_ui(self):
        self.setWindowTitle("DynTraf - Grid Selection")
        self.resize(1000, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        left_panel = QVBoxLayout()
        
        grid_group = QGroupBox("Map Settings")
        grid_layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(["7x7 Straight Grid", "7x7 Curved Grid", "Sample OSM Grid"])
        self.combo.currentTextChanged.connect(self.change_grid)
        grid_layout.addWidget(self.combo)
        grid_group.setLayout(grid_layout)
        left_panel.addWidget(grid_group)

        control_group = QGroupBox("Controls")
        control_layout = QVBoxLayout()
        self.btn_start = QPushButton("Start / Resume")
        self.btn_start.clicked.connect(self.start_simulation)
        self.btn_stop = QPushButton("Pause")
        self.btn_stop.clicked.connect(self.stop_simulation)
        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_group.setLayout(control_layout)
        left_panel.addWidget(control_group)

        stats_group = QGroupBox("Live Statistics")
        stats_layout = QVBoxLayout()
        self.lbl_time = QLabel("Time: 0")
        stats_layout.addWidget(self.lbl_time)
        stats_group.setLayout(stats_layout)
        left_panel.addWidget(stats_group)
        
        left_panel.addStretch()
        main_layout.addLayout(left_panel, 1)

        right_panel = QVBoxLayout()
        self.canvas = TrafficCanvas(self)
        right_panel.addWidget(self.canvas)
        main_layout.addLayout(right_panel, 4)

    def change_grid(self, text):
        self.stop_simulation()
        if "Straight" in text:
            self.grid_style = 'Straight'
        elif "Curved" in text:
            self.grid_style = 'Curved'
        else:
            self.grid_style = 'Sample'
        
        self.reset_simulation()

    def reset_simulation(self):
        self.current_time = 0
        self.lbl_time.setText("Time: 0")
        
        if self.grid_style == 'Sample':
            self.graph = self.net_builder.build_sample_network()
        else:
            self.graph = self.net_builder.build_grid_network(7, 7)
            
        self.sim_manager = SimulationManager(self.graph, config)
        optimizer = self.optimizer_class(self.graph)
        
        for node in self.graph.nodes():
            TrafficLight(self.sim_manager.env, node, optimizer)
            
        self.sim_manager.register_spawner(self.spawner_func)    
        self.canvas.draw_network(self.graph, self.current_time, self.grid_style)

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.step_simulation)

    def start_simulation(self):
        self.timer.start()

    def stop_simulation(self):
        self.timer.stop()

    def step_simulation(self):
        self.current_time += 1
        self.sim_manager.env.run(until=self.current_time)
        self.canvas.draw_network(self.graph, self.current_time, self.grid_style)
        self.lbl_time.setText(f"Time: {self.current_time}")
