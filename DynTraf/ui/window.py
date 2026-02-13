from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QSlider)
from PyQt5.QtCore import QTimer, Qt
from ui.canvas import TrafficCanvas

class MainWindow(QMainWindow):
    def __init__(self, simulation_manager):
        super().__init__()
        self.sim_manager = simulation_manager
        self.env = simulation_manager.env
        self.current_time = 0
        self.step_size = 1  # How many SimPy ticks to advance per UI update
        
        self.init_ui()
        self.setup_timer()

    def init_ui(self):
        self.setWindowTitle("DynTraf - Capstone Simulator")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_panel = QVBoxLayout()
        
        control_group = QGroupBox("Simulation Controls")
        control_layout = QVBoxLayout()      
        self.btn_start = QPushButton("Start / Resume")
        self.btn_start.clicked.connect(self.start_simulation)
        control_layout.addWidget(self.btn_start)
        self.btn_stop = QPushButton("Pause")
        self.btn_stop.clicked.connect(self.stop_simulation)
        control_layout.addWidget(self.btn_stop)      
        self.btn_step = QPushButton("Step +1")
        self.btn_step.clicked.connect(self.step_simulation)
        control_layout.addWidget(self.btn_step)
        control_group.setLayout(control_layout)
        left_panel.addWidget(control_group)

        stats_group = QGroupBox("Live Statistics")
        stats_layout = QVBoxLayout()
        self.lbl_time = QLabel("Time: 0")
        self.lbl_cars = QLabel("Active Cars: 0")
        self.lbl_accidents = QLabel("Active Accidents: 0")
        
        stats_layout.addWidget(self.lbl_time)
        stats_layout.addWidget(self.lbl_cars)
        stats_layout.addWidget(self.lbl_accidents)
        stats_group.setLayout(stats_layout)
        left_panel.addWidget(stats_group)
        left_panel.addStretch()
        main_layout.addLayout(left_panel, 1) 

        right_panel = QVBoxLayout()
        self.canvas = TrafficCanvas(self)
        right_panel.addWidget(self.canvas)
        main_layout.addLayout(right_panel, 4) 
        self.canvas.draw_network(self.sim_manager.network)

    def setup_timer(self):
        """Timer acts as the 'Game Loop'"""
        self.timer = QTimer()
        self.timer.setInterval(100)  # time in milliseconds
        self.timer.timeout.connect(self.step_simulation)

    def start_simulation(self):
        self.timer.start()
        print("UI: Simulation Started")

    def stop_simulation(self):
        self.timer.stop()
        print("UI: Simulation Paused")

    def step_simulation(self):
        try:
            
            target_time = self.current_time + self.step_size
            self.env.run(until=target_time)
            self.current_time = target_time            
            self.update_visuals()
            
        except StopIteration:
            self.timer.stop()
            self.lbl_time.setText("Status: Finished")

    def update_visuals(self):
        self.canvas.draw_network(self.sim_manager.network, self.current_time)       
        self.lbl_time.setText(f"Time: {self.current_time}")       
        total_cars = sum(len(self.sim_manager.network[u][v].get('vehicles', [])) 
                         for u, v in self.sim_manager.network.edges())
        self.lbl_cars.setText(f"Active Cars: {total_cars}")
