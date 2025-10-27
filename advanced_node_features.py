#!/usr/bin/env python3
"""
Дополнительные возможности для эмулятора криптоноды
Включает:
- Эмуляцию различных типов узлов (полный, легкий, майнинг)
- Реалистичную эмуляцию сети
- Статистику и метрики
- Расширенную визуализацию
"""

import random
import time
import hashlib
import json
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class NodeType(Enum):
    """Типы узлов"""
    FULL = "full"           # Полный узел
    LIGHT = "light"         # Легкий узел
    MINING = "mining"       # Майнинг узел
    VALIDATOR = "validator" # Валидатор

class NetworkProtocol(Enum):
    """Сетевые протоколы"""
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    CUSTOM = "custom"

@dataclass
class NetworkMetrics:
    """Метрики сети"""
    latency: float  # Задержка в мс
    bandwidth: float  # Пропускная способность в МБ/с
    packet_loss: float  # Потери пакетов в %
    uptime: float  # Время работы в %

@dataclass
class NodeMetrics:
    """Метрики узла"""
    cpu_usage: float  # Использование CPU в %
    memory_usage: float  # Использование памяти в МБ
    disk_usage: float  # Использование диска в ГБ
    network_io: float  # Сетевой трафик в МБ/с

class AdvancedBlockchainNode:
    """Расширенный класс узла блокчейн-сети"""
    
    def __init__(self, node_id: str, node_type: NodeType, x: int, y: int, 
                 protocol: NetworkProtocol = NetworkProtocol.BITCOIN):
        self.node_id = node_id
        self.node_type = node_type
        self.x = x
        self.y = y
        self.protocol = protocol
        self.status = "online"
        self.last_seen = datetime.now()
        
        # Блокчейн данные
        self.block_height = random.randint(100000, 999999)
        self.blockchain_size = self._calculate_blockchain_size()
        self.peers = []
        self.pending_transactions = []
        self.mempool_size = 0
        
        # Сетевые метрики
        self.network_metrics = NetworkMetrics(
            latency=random.uniform(10, 200),
            bandwidth=random.uniform(1, 100),
            packet_loss=random.uniform(0, 5),
            uptime=random.uniform(95, 99.9)
        )
        
        # Метрики узла
        self.node_metrics = NodeMetrics(
            cpu_usage=random.uniform(5, 80),
            memory_usage=random.uniform(100, 2000),
            disk_usage=random.uniform(10, 500),
            network_io=random.uniform(0.1, 10)
        )
        
        # Дополнительные параметры
        self.sync_status = "synced"
        self.last_block_time = datetime.now() - timedelta(minutes=random.randint(1, 60))
        self.connection_count = random.randint(5, 50)
        self.version = self._get_node_version()
        
    def _calculate_blockchain_size(self) -> float:
        """Расчет размера блокчейна в ГБ"""
        base_size = 400  # Базовый размер Bitcoin блокчейна
        return base_size + random.uniform(0, 50)
    
    def _get_node_version(self) -> str:
        """Получение версии узла"""
        versions = {
            NetworkProtocol.BITCOIN: ["24.0.1", "23.0.0", "22.0.0"],
            NetworkProtocol.ETHEREUM: ["1.12.0", "1.11.0", "1.10.0"],
            NetworkProtocol.CUSTOM: ["1.0.0", "0.9.0", "0.8.0"]
        }
        return random.choice(versions[self.protocol])
    
    def update_metrics(self):
        """Обновление метрик узла"""
        # Обновление сетевых метрик
        self.network_metrics.latency += random.uniform(-5, 5)
        self.network_metrics.latency = max(1, min(500, self.network_metrics.latency))
        
        self.network_metrics.bandwidth += random.uniform(-1, 1)
        self.network_metrics.bandwidth = max(0.1, min(200, self.network_metrics.bandwidth))
        
        # Обновление метрик узла
        self.node_metrics.cpu_usage += random.uniform(-2, 2)
        self.node_metrics.cpu_usage = max(0, min(100, self.node_metrics.cpu_usage))
        
        self.node_metrics.memory_usage += random.uniform(-10, 10)
        self.node_metrics.memory_usage = max(50, min(4000, self.node_metrics.memory_usage))
        
        # Обновление времени последнего блока
        if random.random() < 0.1:  # 10% шанс получения нового блока
            self.last_block_time = datetime.now()
            self.block_height += 1
    
    def get_detailed_info(self) -> Dict:
        """Получение детальной информации об узле"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "protocol": self.protocol.value,
            "status": self.status,
            "version": self.version,
            "block_height": self.block_height,
            "blockchain_size_gb": round(self.blockchain_size, 2),
            "peers_count": len(self.peers),
            "pending_txs": len(self.pending_transactions),
            "mempool_size": self.mempool_size,
            "sync_status": self.sync_status,
            "last_block_time": self.last_block_time.strftime("%H:%M:%S"),
            "connection_count": self.connection_count,
            "uptime": round(self.network_metrics.uptime, 2),
            "latency_ms": round(self.network_metrics.latency, 1),
            "bandwidth_mbps": round(self.network_metrics.bandwidth, 1),
            "cpu_usage": round(self.node_metrics.cpu_usage, 1),
            "memory_usage_mb": round(self.node_metrics.memory_usage, 1),
            "disk_usage_gb": round(self.node_metrics.disk_usage, 1)
        }

class NetworkSimulator:
    """Симулятор сети"""
    
    def __init__(self):
        self.nodes = []
        self.connections = []
        self.network_load = 0.0
        self.total_bandwidth = 1000  # МБ/с
        
    def add_node(self, node: AdvancedBlockchainNode):
        """Добавление узла в сеть"""
        self.nodes.append(node)
        
    def simulate_network_activity(self):
        """Симуляция сетевой активности"""
        # Обновление метрик всех узлов
        for node in self.nodes:
            node.update_metrics()
        
        # Симуляция сетевой нагрузки
        self.network_load = sum(node.node_metrics.network_io for node in self.nodes)
        self.network_load = min(self.total_bandwidth, self.network_load)
        
        # Случайные события сети
        self._simulate_network_events()
    
    def _simulate_network_events(self):
        """Симуляция сетевых событий"""
        events = [
            "node_connection", "node_disconnection", "network_congestion",
            "packet_loss", "bandwidth_fluctuation"
        ]
        
        for _ in range(random.randint(1, 3)):
            event = random.choice(events)
            if event == "node_connection":
                self._simulate_node_connection()
            elif event == "node_disconnection":
                self._simulate_node_disconnection()
            elif event == "network_congestion":
                self._simulate_network_congestion()
    
    def _simulate_node_connection(self):
        """Симуляция подключения узла"""
        if len(self.nodes) >= 2:
            node = random.choice(self.nodes)
            node.connection_count += 1
            node.network_metrics.uptime = min(99.9, node.network_metrics.uptime + 0.1)
    
    def _simulate_node_disconnection(self):
        """Симуляция отключения узла"""
        if len(self.nodes) >= 1:
            node = random.choice(self.nodes)
            if random.random() < 0.1:  # 10% шанс отключения
                node.status = "offline"
                node.connection_count = max(0, node.connection_count - 1)
    
    def _simulate_network_congestion(self):
        """Симуляция перегрузки сети"""
        for node in self.nodes:
            node.network_metrics.latency += random.uniform(10, 50)
            node.network_metrics.packet_loss += random.uniform(0.1, 1.0)
    
    def get_network_statistics(self) -> Dict:
        """Получение статистики сети"""
        online_nodes = [n for n in self.nodes if n.status == "online"]
        
        return {
            "total_nodes": len(self.nodes),
            "online_nodes": len(online_nodes),
            "network_load_percent": round((self.network_load / self.total_bandwidth) * 100, 1),
            "average_latency": round(sum(n.network_metrics.latency for n in online_nodes) / len(online_nodes), 1) if online_nodes else 0,
            "average_bandwidth": round(sum(n.network_metrics.bandwidth for n in online_nodes) / len(online_nodes), 1) if online_nodes else 0,
            "total_connections": sum(n.connection_count for n in online_nodes),
            "network_health": self._calculate_network_health()
        }
    
    def _calculate_network_health(self) -> str:
        """Расчет здоровья сети"""
        online_ratio = len([n for n in self.nodes if n.status == "online"]) / len(self.nodes)
        
        if online_ratio >= 0.9:
            return "Отличное"
        elif online_ratio >= 0.7:
            return "Хорошее"
        elif online_ratio >= 0.5:
            return "Удовлетворительное"
        else:
            return "Плохое"

class TransactionPool:
    """Пул транзакций"""
    
    def __init__(self):
        self.transactions = []
        self.max_pool_size = 10000
        
    def add_transaction(self, transaction):
        """Добавление транзакции в пул"""
        if len(self.transactions) < self.max_pool_size:
            self.transactions.append(transaction)
            return True
        return False
    
    def get_transactions_for_block(self, count: int) -> List:
        """Получение транзакций для блока"""
        # Сортируем по комиссии (приоритет)
        sorted_txs = sorted(self.transactions, key=lambda x: x.fee, reverse=True)
        selected_txs = sorted_txs[:count]
        
        # Удаляем выбранные транзакции из пула
        for tx in selected_txs:
            self.transactions.remove(tx)
        
        return selected_txs
    
    def get_pool_stats(self) -> Dict:
        """Получение статистики пула"""
        total_fees = sum(tx.fee for tx in self.transactions)
        avg_fee = total_fees / len(self.transactions) if self.transactions else 0
        
        return {
            "transaction_count": len(self.transactions),
            "total_fees": round(total_fees, 6),
            "average_fee": round(avg_fee, 6),
            "pool_utilization": round((len(self.transactions) / self.max_pool_size) * 100, 1)
        }

class MiningSimulator:
    """Симулятор майнинга"""
    
    def __init__(self, difficulty: int = 1000000):
        self.difficulty = difficulty
        self.current_nonce = 0
        self.target_hash = "0" * 4  # Цель для хеша
        self.mining_power = random.uniform(1, 100)  # Хешрейт в MH/s
        
    def mine_block(self, block_data: str) -> Optional[str]:
        """Майнинг блока"""
        start_time = time.time()
        
        while self.current_nonce < 1000000:  # Ограничение для эмуляции
            # Создаем хеш с текущим nonce
            data_to_hash = f"{block_data}{self.current_nonce}"
            block_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
            
            # Проверяем, соответствует ли хеш цели
            if block_hash.startswith(self.target_hash):
                mining_time = time.time() - start_time
                return {
                    "hash": block_hash,
                    "nonce": self.current_nonce,
                    "mining_time": mining_time,
                    "hashrate": self.mining_power
                }
            
            self.current_nonce += 1
        
        return None
    
    def adjust_difficulty(self, block_time: float):
        """Корректировка сложности"""
        target_time = 600  # 10 минут для Bitcoin
        
        if block_time < target_time * 0.5:
            self.difficulty = int(self.difficulty * 1.5)
        elif block_time > target_time * 2:
            self.difficulty = int(self.difficulty * 0.75)
        
        # Обновляем цель хеша
        self.target_hash = "0" * (self.difficulty // 1000000 + 1)

# Пример использования
if __name__ == "__main__":
    # Создание симулятора сети
    network = NetworkSimulator()
    
    # Создание узлов разных типов
    nodes = [
        AdvancedBlockchainNode("FULL_001", NodeType.FULL, 100, 100, NetworkProtocol.BITCOIN),
        AdvancedBlockchainNode("LIGHT_001", NodeType.LIGHT, 200, 100, NetworkProtocol.BITCOIN),
        AdvancedBlockchainNode("MINING_001", NodeType.MINING, 300, 100, NetworkProtocol.BITCOIN),
        AdvancedBlockchainNode("ETH_001", NodeType.FULL, 400, 100, NetworkProtocol.ETHEREUM),
    ]
    
    # Добавление узлов в сеть
    for node in nodes:
        network.add_node(node)
    
    # Симуляция работы сети
    for i in range(10):
        print(f"\n=== Итерация {i+1} ===")
        network.simulate_network_activity()
        
        stats = network.get_network_statistics()
        print(f"Статистика сети: {stats}")
        
        for node in nodes:
            info = node.get_detailed_info()
            print(f"Узел {info['node_id']}: {info['status']}, CPU: {info['cpu_usage']}%, "
                  f"Латентность: {info['latency_ms']}мс")
        
        time.sleep(1)