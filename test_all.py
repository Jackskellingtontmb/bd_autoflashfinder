#!/usr/bin/env python3
"""
Тестовый скрипт для проверки всех компонентов эмулятора криптоноды
"""

import sys
import time
import traceback

def test_imports():
    """Тест импорта всех модулей"""
    print("🔍 Тестирование импортов...")
    
    try:
        import tkinter as tk
        print("  ✅ tkinter - OK")
    except ImportError as e:
        print(f"  ❌ tkinter - ОШИБКА: {e}")
        return False
    
    try:
        import requests
        print("  ✅ requests - OK")
    except ImportError as e:
        print(f"  ❌ requests - ОШИБКА: {e}")
        return False
    
    try:
        import hashlib
        print("  ✅ hashlib - OK")
    except ImportError as e:
        print(f"  ❌ hashlib - ОШИБКА: {e}")
        return False
    
    try:
        import threading
        print("  ✅ threading - OK")
    except ImportError as e:
        print(f"  ❌ threading - ОШИБКА: {e}")
        return False
    
    return True

def test_basic_classes():
    """Тест основных классов"""
    print("\n🔧 Тестирование основных классов...")
    
    try:
        from crypto_node_emulator import BlockchainNode, Transaction, Block
        
        # Тест BlockchainNode
        node = BlockchainNode("TEST_NODE", 100, 100)
        assert node.node_id == "TEST_NODE"
        assert node.status == "online"
        print("  ✅ BlockchainNode - OK")
        
        # Тест Transaction
        tx = Transaction("tx_test", "addr1", "addr2", 0.001, 0.0001)
        assert tx.tx_id == "tx_test"
        assert tx.amount == 0.001
        print("  ✅ Transaction - OK")
        
        # Тест Block
        block = Block("hash_test", 1000, "prev_hash", [], time.time())
        assert block.block_hash == "hash_test"
        assert block.height == 1000
        print("  ✅ Block - OK")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в основных классах: {e}")
        traceback.print_exc()
        return False

def test_advanced_classes():
    """Тест расширенных классов"""
    print("\n🔧 Тестирование расширенных классов...")
    
    try:
        from advanced_node_features import (
            AdvancedBlockchainNode, NodeType, NetworkProtocol,
            NetworkSimulator, TransactionPool, MiningSimulator
        )
        
        # Тест AdvancedBlockchainNode
        node = AdvancedBlockchainNode("ADV_NODE", NodeType.FULL, 100, 100)
        assert node.node_type == NodeType.FULL
        assert node.protocol == NetworkProtocol.BITCOIN
        print("  ✅ AdvancedBlockchainNode - OK")
        
        # Тест NetworkSimulator
        network = NetworkSimulator()
        network.add_node(node)
        assert len(network.nodes) == 1
        print("  ✅ NetworkSimulator - OK")
        
        # Тест TransactionPool
        pool = TransactionPool()
        assert pool.max_pool_size == 10000
        print("  ✅ TransactionPool - OK")
        
        # Тест MiningSimulator
        miner = MiningSimulator()
        assert miner.difficulty == 1000000
        print("  ✅ MiningSimulator - OK")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в расширенных классах: {e}")
        traceback.print_exc()
        return False

def test_network_connection():
    """Тест сетевого соединения"""
    print("\n🌐 Тестирование сетевого соединения...")
    
    try:
        from crypto_node_emulator import NetworkConnection
        
        # Тест проверки интернета
        internet_status = NetworkConnection.check_internet()
        print(f"  📡 Статус интернета: {'✅ Подключен' if internet_status else '❌ Отключен'}")
        
        # Тест API эндпоинтов
        api_results = NetworkConnection.check_api_endpoints()
        print(f"  🔗 Проверено API эндпоинтов: {len(api_results)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в сетевом соединении: {e}")
        traceback.print_exc()
        return False

def test_crypto_functions():
    """Тест криптографических функций"""
    print("\n🔐 Тестирование криптографических функций...")
    
    try:
        import hashlib
        import uuid
        
        # Тест генерации хешей
        test_data = "test_blockchain_data"
        hash_result = hashlib.sha256(test_data.encode()).hexdigest()
        assert len(hash_result) == 64
        print("  ✅ Генерация хешей - OK")
        
        # Тест генерации UUID
        test_uuid = str(uuid.uuid4())
        assert len(test_uuid) == 36
        print("  ✅ Генерация UUID - OK")
        
        # Тест майнинга
        from advanced_node_features import MiningSimulator
        miner = MiningSimulator(difficulty=1000)
        result = miner.mine_block("test_block_data")
        if result:
            print("  ✅ Майнинг блоков - OK")
        else:
            print("  ⚠️ Майнинг блоков - Не найден блок (нормально)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в криптографических функциях: {e}")
        traceback.print_exc()
        return False

def test_gui_components():
    """Тест компонентов GUI"""
    print("\n🎨 Тестирование компонентов GUI...")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Создание тестового окна
        root = tk.Tk()
        root.withdraw()  # Скрываем окно
        
        # Тест создания виджетов
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text="Test")
        button = ttk.Button(frame, text="Test")
        progress = ttk.Progressbar(frame)
        
        assert frame is not None
        assert label is not None
        assert button is not None
        assert progress is not None
        
        print("  ✅ Создание виджетов - OK")
        
        # Закрытие окна
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в GUI компонентах: {e}")
        traceback.print_exc()
        return False

def test_demo_functions():
    """Тест демонстрационных функций"""
    print("\n🎮 Тестирование демонстрационных функций...")
    
    try:
        # Импорт функций из demo.py
        import demo
        
        # Проверяем, что функции существуют
        assert hasattr(demo, 'demo_basic_features')
        assert hasattr(demo, 'demo_advanced_features')
        assert hasattr(demo, 'demo_transaction_creation')
        assert hasattr(demo, 'demo_mining_simulation')
        
        print("  ✅ Демонстрационные функции - OK")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в демонстрационных функциях: {e}")
        traceback.print_exc()
        return False

def run_performance_test():
    """Тест производительности"""
    print("\n⚡ Тестирование производительности...")
    
    try:
        from advanced_node_features import NetworkSimulator, AdvancedBlockchainNode, NodeType
        
        # Создание сети с множеством узлов
        network = NetworkSimulator()
        start_time = time.time()
        
        for i in range(10):
            node = AdvancedBlockchainNode(f"PERF_NODE_{i}", NodeType.FULL, i*50, i*50)
            network.add_node(node)
        
        # Симуляция работы сети
        for _ in range(5):
            network.simulate_network_activity()
        
        end_time = time.time()
        performance_time = end_time - start_time
        
        print(f"  ⏱️ Время выполнения: {performance_time:.2f}с")
        print(f"  📊 Узлов в сети: {len(network.nodes)}")
        
        if performance_time < 1.0:
            print("  ✅ Производительность - Отличная")
        elif performance_time < 2.0:
            print("  ✅ Производительность - Хорошая")
        else:
            print("  ⚠️ Производительность - Медленная")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка в тесте производительности: {e}")
        traceback.print_exc()
        return False

def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ ЭМУЛЯТОРА КРИПТОНОДЫ")
    print("=" * 50)
    
    tests = [
        ("Импорты", test_imports),
        ("Основные классы", test_basic_classes),
        ("Расширенные классы", test_advanced_classes),
        ("Сетевое соединение", test_network_connection),
        ("Криптографические функции", test_crypto_functions),
        ("GUI компоненты", test_gui_components),
        ("Демонстрационные функции", test_demo_functions),
        ("Производительность", run_performance_test),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"  ❌ Тест '{test_name}' не прошел")
        except Exception as e:
            print(f"  ❌ Критическая ошибка в тесте '{test_name}': {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print(f"✅ Пройдено: {passed}/{total}")
    print(f"❌ Провалено: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n🚀 Эмулятор готов к использованию!")
        print("   Запустите: python3 crypto_node_emulator.py")
    else:
        print("⚠️ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")
        print("   Проверьте установку зависимостей")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)