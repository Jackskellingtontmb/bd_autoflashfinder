#!/usr/bin/env python3
"""
Демонстрационный скрипт для эмулятора криптоноды
Показывает основные возможности и функции
"""

import time
import random
from crypto_node_emulator import CryptoNodeEmulator, BlockchainNode, Transaction, Block
from advanced_node_features import AdvancedBlockchainNode, NodeType, NetworkProtocol, NetworkSimulator

def demo_basic_features():
    """Демонстрация основных возможностей"""
    print("🚀 Запуск демонстрации эмулятора криптоноды")
    print("=" * 50)
    
    # Создание эмулятора
    emulator = CryptoNodeEmulator()
    
    print("✅ Эмулятор создан успешно")
    print("📊 Статистика узлов:")
    
    for i, node in enumerate(emulator.nodes):
        info = node.get_info()
        print(f"  Узел {i+1}: {info['node_id']} - {info['status']} "
              f"(Высота: {info['block_height']}, Синхронизация: {info['sync_status']})")
    
    print("\n🎮 Доступные действия:")
    print("  1. Запустить узел")
    print("  2. Создать транзакции")
    print("  3. Майнить блоки")
    print("  4. Просматривать информацию об узлах")
    print("  5. Мониторить сетевую активность")
    
    return emulator

def demo_advanced_features():
    """Демонстрация расширенных возможностей"""
    print("\n🔧 Демонстрация расширенных возможностей")
    print("=" * 50)
    
    # Создание симулятора сети
    network = NetworkSimulator()
    
    # Создание различных типов узлов
    nodes = [
        AdvancedBlockchainNode("FULL_BTC_001", NodeType.FULL, 100, 100, NetworkProtocol.BITCOIN),
        AdvancedBlockchainNode("LIGHT_BTC_001", NodeType.LIGHT, 200, 100, NetworkProtocol.BITCOIN),
        AdvancedBlockchainNode("MINING_BTC_001", NodeType.MINING, 300, 100, NetworkProtocol.BITCOIN),
        AdvancedBlockchainNode("FULL_ETH_001", NodeType.FULL, 400, 100, NetworkProtocol.ETHEREUM),
        AdvancedBlockchainNode("VALIDATOR_001", NodeType.VALIDATOR, 500, 100, NetworkProtocol.CUSTOM),
    ]
    
    # Добавление узлов в сеть
    for node in nodes:
        network.add_node(node)
    
    print(f"📡 Создано {len(nodes)} узлов разных типов:")
    for node in nodes:
        print(f"  - {node.node_id} ({node.node_type.value}, {node.protocol.value})")
    
    # Симуляция работы сети
    print("\n🌐 Симуляция сетевой активности:")
    for i in range(5):
        network.simulate_network_activity()
        stats = network.get_network_statistics()
        
        print(f"  Итерация {i+1}:")
        print(f"    Узлов онлайн: {stats['online_nodes']}/{stats['total_nodes']}")
        print(f"    Нагрузка сети: {stats['network_load_percent']}%")
        print(f"    Средняя латентность: {stats['average_latency']}мс")
        print(f"    Здоровье сети: {stats['network_health']}")
        
        # Показ детальной информации об узлах
        for node in nodes:
            info = node.get_detailed_info()
            print(f"    {info['node_id']}: CPU {info['cpu_usage']}%, "
                  f"Память {info['memory_usage_mb']}МБ, "
                  f"Латентность {info['latency_ms']}мс")
        
        time.sleep(1)
    
    return network

def demo_transaction_creation():
    """Демонстрация создания транзакций"""
    print("\n💸 Демонстрация создания транзакций")
    print("=" * 50)
    
    # Создание пула транзакций
    from advanced_node_features import TransactionPool
    
    pool = TransactionPool()
    
    # Создание различных транзакций
    transaction_types = [
        ("Перевод", 0.001, 0.0001),
        ("Покупка", 0.05, 0.001),
        ("Продажа", 0.1, 0.002),
        ("Микротранзакция", 0.0001, 0.00005),
        ("Крупная сделка", 1.0, 0.01),
    ]
    
    for tx_type, amount, fee in transaction_types:
        tx_id = f"tx_{random.randint(10000, 99999)}"
        from_addr = f"addr_{random.randint(1000, 9999)}"
        to_addr = f"addr_{random.randint(1000, 9999)}"
        
        tx = Transaction(tx_id, from_addr, to_addr, amount, fee)
        pool.add_transaction(tx)
        
        print(f"  Создана транзакция: {tx_type}")
        print(f"    ID: {tx_id}")
        print(f"    От: {from_addr} → К: {to_addr}")
        print(f"    Сумма: {amount} BTC, Комиссия: {fee} BTC")
    
    # Статистика пула
    stats = pool.get_pool_stats()
    print(f"\n📊 Статистика пула транзакций:")
    print(f"  Количество транзакций: {stats['transaction_count']}")
    print(f"  Общая сумма комиссий: {stats['total_fees']} BTC")
    print(f"  Средняя комиссия: {stats['average_fee']} BTC")
    print(f"  Заполненность пула: {stats['pool_utilization']}%")
    
    return pool

def demo_mining_simulation():
    """Демонстрация симуляции майнинга"""
    print("\n⛏️ Демонстрация симуляции майнинга")
    print("=" * 50)
    
    from advanced_node_features import MiningSimulator
    
    # Создание симулятора майнинга
    miner = MiningSimulator(difficulty=1000000)
    
    print(f"🔧 Настройки майнинга:")
    print(f"  Сложность: {miner.difficulty}")
    print(f"  Цель хеша: {miner.target_hash}")
    print(f"  Хешрейт: {miner.mining_power:.1f} MH/s")
    
    # Симуляция майнинга нескольких блоков
    for i in range(3):
        print(f"\n  Майнинг блока {i+1}:")
        
        block_data = f"block_{i+1}_data_{random.randint(1000, 9999)}"
        result = miner.mine_block(block_data)
        
        if result:
            print(f"    ✅ Блок найден!")
            print(f"    Хеш: {result['hash'][:16]}...")
            print(f"    Nonce: {result['nonce']}")
            print(f"    Время майнинга: {result['mining_time']:.2f}с")
            print(f"    Хешрейт: {result['hashrate']:.1f} MH/s")
            
            # Корректировка сложности
            miner.adjust_difficulty(result['mining_time'])
            print(f"    Новая сложность: {miner.difficulty}")
        else:
            print(f"    ❌ Блок не найден (превышен лимит попыток)")
    
    return miner

def demo_network_visualization():
    """Демонстрация визуализации сети"""
    print("\n🎨 Демонстрация визуализации сети")
    print("=" * 50)
    
    print("📊 Создание интерактивной карты сети:")
    print("  - Узлы отображаются как круги")
    print("  - Связи между узлами как пунктирные линии")
    print("  - Цвета указывают на статус узлов:")
    print("    🟢 Зеленый - локальный узел")
    print("    🔵 Синий - удаленные узлы")
    print("    🔴 Красный - отключенные узлы")
    print("  - Анимированные точки показывают передачу данных")
    print("  - Клик по узлу показывает детальную информацию")
    
    print("\n🖱️ Интерактивные возможности:")
    print("  - Наведение мыши подсвечивает узлы")
    print("  - Клик по узлу открывает окно с информацией")
    print("  - Автоматическое обновление статусов")
    print("  - Реальное время отображения событий")

def main():
    """Главная функция демонстрации"""
    print("🎯 ДЕМОНСТРАЦИЯ ЭМУЛЯТОРА КРИПТОНОДЫ")
    print("=" * 60)
    
    try:
        # Демонстрация основных возможностей
        emulator = demo_basic_features()
        
        # Демонстрация расширенных возможностей
        network = demo_advanced_features()
        
        # Демонстрация создания транзакций
        pool = demo_transaction_creation()
        
        # Демонстрация майнинга
        miner = demo_mining_simulation()
        
        # Демонстрация визуализации
        demo_network_visualization()
        
        print("\n" + "=" * 60)
        print("✅ Демонстрация завершена успешно!")
        print("\n🎮 Для запуска полного эмулятора выполните:")
        print("   python crypto_node_emulator.py")
        
        print("\n📚 Дополнительные возможности:")
        print("   - Запуск расширенного симулятора: python advanced_node_features.py")
        print("   - Просмотр документации: README.md")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время демонстрации: {e}")
        print("Проверьте, что все зависимости установлены корректно")

if __name__ == "__main__":
    main()