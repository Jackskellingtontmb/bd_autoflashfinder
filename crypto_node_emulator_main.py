#!/usr/bin/env python3
"""
Эмулятор криптоноды с GUI
Включает:
- Проверку интернет-соединения
- Визуализацию передачи данных блокчейна
- Статус Online/Offline узлов
- Реалистичную эмуляцию работы блокчейн-сети
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import socket
import requests
import json
import hashlib
from datetime import datetime
import queue
import uuid

class BlockchainNode:
    """Класс для представления узла блокчейн-сети"""
    
    def __init__(self, node_id, x, y, is_local=False):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.is_local = is_local
        self.status = "online"
        self.last_seen = datetime.now()
        self.block_height = random.randint(100000, 999999)
        self.peers = []
        self.pending_transactions = []
        self.sync_status = "synced"
        
    def update_status(self, status):
        self.status = status
        self.last_seen = datetime.now()
        
    def add_transaction(self, tx):
        self.pending_transactions.append(tx)
        
    def get_info(self):
        return {
            "node_id": self.node_id,
            "status": self.status,
            "block_height": self.block_height,
            "peers": len(self.peers),
            "pending_txs": len(self.pending_transactions),
            "sync_status": self.sync_status
        }

class Transaction:
    """Класс для представления транзакции"""
    
    def __init__(self, tx_id, from_addr, to_addr, amount, fee):
        self.tx_id = tx_id
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.fee = fee
        self.timestamp = datetime.now()
        self.status = "pending"
        
    def to_dict(self):
        return {
            "tx_id": self.tx_id,
            "from": self.from_addr,
            "to": self.to_addr,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status
        }

class Block:
    """Класс для представления блока"""
    
    def __init__(self, block_hash, height, prev_hash, transactions, timestamp):
        self.block_hash = block_hash
        self.height = height
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.difficulty = random.randint(1000000, 9999999)
        
    def to_dict(self):
        return {
            "block_hash": self.block_hash,
            "height": self.height,
            "prev_hash": self.prev_hash,
            "transactions": len(self.transactions),
            "timestamp": self.timestamp.isoformat(),
            "difficulty": self.difficulty
        }

class NetworkConnection:
    """Класс для проверки сетевого соединения"""
    
    @staticmethod
    def check_internet():
        """Проверка подключения к интернету"""
        try:
            # Проверяем подключение к DNS Google
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    @staticmethod
    def check_api_endpoints():
        """Проверка доступности API эндпоинтов"""
        endpoints = [
            "https://api.coingecko.com/api/v3/ping",
            "https://blockchain.info/latestblock",
            "https://api.blockcypher.com/v1/btc/main"
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                results[endpoint] = response.status_code == 200
            except:
                results[endpoint] = False
                
        return results

class CryptoNodeEmulator:
    """Основной класс эмулятора криптоноды"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Эмулятор Криптоноды v1.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Переменные состояния
        self.is_running = False
        self.network_status = "checking"
        self.nodes = []
        self.transactions = []
        self.blocks = []
        self.message_queue = queue.Queue()
        
        # Инициализация узлов
        self.init_nodes()
        
        # Создание GUI
        self.create_gui()
        
        # Запуск фоновых процессов
        self.start_background_processes()
        
    def init_nodes(self):
        """Инициализация узлов сети"""
        # Локальный узел
        local_node = BlockchainNode("LOCAL_NODE", 100, 200, is_local=True)
        local_node.block_height = 789456
        local_node.sync_status = "synced"
        
        # Удаленные узлы
        remote_nodes = [
            BlockchainNode("NODE_001", 300, 150),
            BlockchainNode("NODE_002", 500, 250),
            BlockchainNode("NODE_003", 700, 180),
            BlockchainNode("NODE_004", 400, 350),
            BlockchainNode("NODE_005", 600, 320),
            BlockchainNode("NODE_006", 800, 280),
        ]
        
        self.nodes = [local_node] + remote_nodes
        
        # Создание связей между узлами
        for node in self.nodes:
            node.peers = random.sample([n for n in self.nodes if n != node], 
                                     min(3, len(self.nodes) - 1))
    
    def create_gui(self):
        """Создание графического интерфейса"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Верхняя панель статуса
        self.create_status_panel(main_frame)
        
        # Центральная панель с сетью
        self.create_network_panel(main_frame)
        
        # Нижняя панель с логами
        self.create_log_panel(main_frame)
        
        # Боковая панель управления
        self.create_control_panel(main_frame)
    
    def create_status_panel(self, parent):
        """Создание панели статуса"""
        status_frame = ttk.LabelFrame(parent, text="Статус системы", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Статус интернета
        self.internet_status = tk.StringVar(value="Проверка...")
        ttk.Label(status_frame, text="Интернет:").grid(row=0, column=0, sticky=tk.W)
        self.internet_label = ttk.Label(status_frame, textvariable=self.internet_status)
        self.internet_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Статус синхронизации
        self.sync_status = tk.StringVar(value="Синхронизация...")
        ttk.Label(status_frame, text="Синхронизация:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.sync_label = ttk.Label(status_frame, textvariable=self.sync_status)
        self.sync_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        # Высота блока
        self.block_height = tk.StringVar(value="789456")
        ttk.Label(status_frame, text="Высота блока:").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.height_label = ttk.Label(status_frame, textvariable=self.block_height)
        self.height_label.grid(row=0, column=5, sticky=tk.W, padx=(10, 0))
        
        # Количество подключенных узлов
        self.peers_count = tk.StringVar(value="6")
        ttk.Label(status_frame, text="Узлы:").grid(row=0, column=6, sticky=tk.W, padx=(20, 0))
        self.peers_label = ttk.Label(status_frame, textvariable=self.peers_count)
        self.peers_label.grid(row=0, column=7, sticky=tk.W, padx=(10, 0))
    
    def create_network_panel(self, parent):
        """Создание панели визуализации сети"""
        network_frame = ttk.LabelFrame(parent, text="Сеть узлов", padding=10)
        network_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas для отрисовки сети
        self.canvas = tk.Canvas(network_frame, bg='#0a0a0a', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий мыши
        self.canvas.bind("<Button-1>", self.on_node_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
    
    def create_log_panel(self, parent):
        """Создание панели логов"""
        log_frame = ttk.LabelFrame(parent, text="Лог событий", padding=10)
        log_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Текстовое поле для логов
        self.log_text = tk.Text(log_frame, height=8, bg='#0a0a0a', fg='#00ff00', 
                               font=('Consolas', 9), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_control_panel(self, parent):
        """Создание панели управления"""
        control_frame = ttk.LabelFrame(parent, text="Управление", padding=10)
        control_frame.pack(fill=tk.X)
        
        # Кнопки управления
        self.start_btn = ttk.Button(control_frame, text="Запустить узел", 
                                   command=self.start_node)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="Остановить узел", 
                                  command=self.stop_node, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_tx_btn = ttk.Button(control_frame, text="Создать транзакцию", 
                                         command=self.generate_transaction)
        self.generate_tx_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.mine_block_btn = ttk.Button(control_frame, text="Майнить блок", 
                                        command=self.mine_block)
        self.mine_block_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Прогресс-бар синхронизации
        ttk.Label(control_frame, text="Прогресс синхронизации:").pack(side=tk.LEFT, padx=(20, 5))
        self.sync_progress = ttk.Progressbar(control_frame, length=200, mode='determinate')
        self.sync_progress.pack(side=tk.LEFT, padx=(0, 10))
        
        # Статус майнинга
        self.mining_status = tk.StringVar(value="Остановлен")
        ttk.Label(control_frame, textvariable=self.mining_status).pack(side=tk.LEFT)
    
    def start_background_processes(self):
        """Запуск фоновых процессов"""
        # Проверка интернета
        self.check_internet_thread()
        
        # Обновление GUI
        self.update_gui()
        
        # Отрисовка сети
        self.draw_network()
    
    def check_internet_thread(self):
        """Поток проверки интернет-соединения"""
        def check():
            while True:
                if NetworkConnection.check_internet():
                    self.network_status = "online"
                    self.internet_status.set("✅ Подключен")
                    self.internet_label.configure(foreground='green')
                else:
                    self.network_status = "offline"
                    self.internet_status.set("❌ Отключен")
                    self.internet_label.configure(foreground='red')
                
                time.sleep(5)
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def update_gui(self):
        """Обновление GUI"""
        def update():
            # Обновление статуса синхронизации
            if self.is_running:
                progress = random.randint(85, 100)
                self.sync_progress['value'] = progress
                if progress == 100:
                    self.sync_status.set("✅ Синхронизирован")
                    self.sync_label.configure(foreground='green')
                else:
                    self.sync_status.set(f"🔄 Синхронизация {progress}%")
                    self.sync_label.configure(foreground='orange')
            else:
                self.sync_status.set("⏸️ Остановлен")
                self.sync_label.configure(foreground='gray')
            
            # Обновление высоты блока
            if self.blocks:
                self.block_height.set(str(self.blocks[-1].height))
            
            # Обновление количества узлов
            online_nodes = sum(1 for node in self.nodes if node.status == "online")
            self.peers_count.set(f"{online_nodes}/{len(self.nodes)}")
            
            # Обновление статуса майнинга
            if self.is_running:
                self.mining_status.set("🔄 Активен")
            else:
                self.mining_status.set("⏸️ Остановлен")
            
            # Обработка сообщений из очереди
            try:
                while True:
                    message = self.message_queue.get_nowait()
                    self.add_log_message(message)
            except queue.Empty:
                pass
            
            # Перерисовка сети
            self.draw_network()
            
            # Следующее обновление через 100мс
            self.root.after(100, update)
        
        update()
    
    def draw_network(self):
        """Отрисовка сети узлов"""
        self.canvas.delete("all")
        
        # Отрисовка связей между узлами
        for node in self.nodes:
            for peer in node.peers:
                if node.status == "online" and peer.status == "online":
                    self.canvas.create_line(node.x, node.y, peer.x, peer.y, 
                                          fill='#00ff00', width=1, dash=(5, 5))
        
        # Отрисовка узлов
        for node in self.nodes:
            # Цвет узла в зависимости от статуса
            if node.status == "online":
                color = '#00ff00' if node.is_local else '#0088ff'
            else:
                color = '#ff0000'
            
            # Рисуем узел
            radius = 15 if node.is_local else 10
            self.canvas.create_oval(node.x - radius, node.y - radius,
                                  node.x + radius, node.y + radius,
                                  fill=color, outline='white', width=2)
            
            # Подпись узла
            label = f"ЛОКАЛЬНЫЙ" if node.is_local else f"NODE_{node.node_id[-3:]}"
            self.canvas.create_text(node.x, node.y + radius + 15,
                                  text=label, fill='white', font=('Arial', 8))
            
            # Статус
            status_text = "🟢" if node.status == "online" else "🔴"
            self.canvas.create_text(node.x, node.y - radius - 10,
                                  text=status_text, fill='white', font=('Arial', 12))
        
        # Анимация передачи данных
        if self.is_running and random.random() < 0.3:
            self.animate_data_transfer()
    
    def animate_data_transfer(self):
        """Анимация передачи данных между узлами"""
        online_nodes = [n for n in self.nodes if n.status == "online"]
        if len(online_nodes) < 2:
            return
        
        source = random.choice(online_nodes)
        target = random.choice([n for n in online_nodes if n != source])
        
        # Создаем анимированную точку
        dot = self.canvas.create_oval(source.x - 2, source.y - 2,
                                    source.x + 2, source.y + 2,
                                    fill='yellow', outline='yellow')
        
        # Анимация движения
        def animate_dot(step=0):
            if step <= 20:
                t = step / 20
                x = source.x + (target.x - source.x) * t
                y = source.y + (target.y - source.y) * t
                
                self.canvas.coords(dot, x - 2, y - 2, x + 2, y + 2)
                self.root.after(50, lambda: animate_dot(step + 1))
            else:
                self.canvas.delete(dot)
        
        animate_dot()
    
    def start_node(self):
        """Запуск узла"""
        self.is_running = True
        self.start_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        
        self.add_log_message("🚀 Узел запущен")
        self.add_log_message("📡 Подключение к сети...")
        
        # Запуск фоновых процессов узла
        self.start_node_processes()
    
    def stop_node(self):
        """Остановка узла"""
        self.is_running = False
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        
        self.add_log_message("⏹️ Узел остановлен")
    
    def start_node_processes(self):
        """Запуск процессов узла"""
        def node_process():
            while self.is_running:
                # Эмуляция работы узла
                time.sleep(random.uniform(1, 3))
                
                # Случайные события
                event = random.choice([
                    "peer_connection", "block_received", "transaction_received",
                    "sync_progress", "network_activity"
                ])
                
                if event == "peer_connection":
                    self.add_log_message("🔗 Новое подключение к узлу")
                elif event == "block_received":
                    self.add_log_message("📦 Получен новый блок")
                elif event == "transaction_received":
                    self.add_log_message("💸 Получена новая транзакция")
                elif event == "sync_progress":
                    self.add_log_message("🔄 Обновление синхронизации")
                elif event == "network_activity":
                    self.add_log_message("🌐 Сетевая активность")
        
        thread = threading.Thread(target=node_process, daemon=True)
        thread.start()
    
    def generate_transaction(self):
        """Создание новой транзакции"""
        if not self.is_running:
            messagebox.showwarning("Предупреждение", "Узел не запущен!")
            return
        
        # Генерация случайной транзакции
        tx_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]
        from_addr = f"addr_{random.randint(1000, 9999)}"
        to_addr = f"addr_{random.randint(1000, 9999)}"
        amount = random.uniform(0.001, 10.0)
        fee = random.uniform(0.0001, 0.01)
        
        tx = Transaction(tx_id, from_addr, to_addr, amount, fee)
        self.transactions.append(tx)
        
        self.add_log_message(f"💸 Создана транзакция {tx_id[:8]}...")
        self.add_log_message(f"   От: {from_addr} → К: {to_addr}")
        self.add_log_message(f"   Сумма: {amount:.6f} BTC, Комиссия: {fee:.6f} BTC")
    
    def mine_block(self):
        """Майнинг нового блока"""
        if not self.is_running:
            messagebox.showwarning("Предупреждение", "Узел не запущен!")
            return
        
        if not self.transactions:
            messagebox.showinfo("Информация", "Нет транзакций для майнинга!")
            return
        
        self.add_log_message("⛏️ Начало майнинга блока...")
        
        # Эмуляция майнинга
        def mine_process():
            for i in range(10):
                if not self.is_running:
                    break
                time.sleep(0.5)
                self.add_log_message(f"⛏️ Майнинг... {i+1}/10")
            
            if self.is_running:
                # Создание блока
                block_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
                height = len(self.blocks) + 789456
                prev_hash = self.blocks[-1].block_hash if self.blocks else "0" * 64
                
                # Берем последние транзакции
                block_txs = self.transactions[-min(5, len(self.transactions)):]
                self.transactions = self.transactions[:-len(block_txs)]
                
                block = Block(block_hash, height, prev_hash, block_txs, datetime.now())
                self.blocks.append(block)
                
                self.add_log_message(f"✅ Блок {height} найден!")
                self.add_log_message(f"   Хеш: {block_hash[:16]}...")
                self.add_log_message(f"   Транзакций: {len(block_txs)}")
        
        thread = threading.Thread(target=mine_process, daemon=True)
        thread.start()
    
    def add_log_message(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.message_queue.put(log_entry)
    
    def on_node_click(self, event):
        """Обработка клика по узлу"""
        for node in self.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= 20:
                self.show_node_info(node)
                break
    
    def show_node_info(self, node):
        """Показать информацию об узле"""
        info = node.get_info()
        
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Информация об узле {node.node_id}")
        info_window.geometry("400x300")
        info_window.configure(bg='#1a1a1a')
        
        # Информация об узле
        ttk.Label(info_window, text=f"ID узла: {info['node_id']}").pack(pady=5)
        ttk.Label(info_window, text=f"Статус: {info['status']}").pack(pady=5)
        ttk.Label(info_window, text=f"Высота блока: {info['block_height']}").pack(pady=5)
        ttk.Label(info_window, text=f"Подключенных узлов: {info['peers']}").pack(pady=5)
        ttk.Label(info_window, text=f"Ожидающих транзакций: {info['pending_txs']}").pack(pady=5)
        ttk.Label(info_window, text=f"Статус синхронизации: {info['sync_status']}").pack(pady=5)
        
        # Кнопка закрытия
        ttk.Button(info_window, text="Закрыть", command=info_window.destroy).pack(pady=20)
    
    def on_mouse_move(self, event):
        """Обработка движения мыши"""
        # Подсветка узлов при наведении
        for node in self.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= 20:
                self.canvas.configure(cursor="hand2")
                return
        
        self.canvas.configure(cursor="")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    # Создание и запуск эмулятора
    emulator = CryptoNodeEmulator()
    emulator.run()