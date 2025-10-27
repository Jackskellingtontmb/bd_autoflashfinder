#!/usr/bin/env python3
"""
Главный скрипт для запуска эмулятора криптоноды
Включает проверку зависимостей и выбор режима работы
"""

import sys
import subprocess
import os

def check_dependencies():
    """Проверка необходимых зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    missing_deps = []
    
    # Проверка Python версии
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше")
        return False
    
    # Проверка tkinter
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError:
        missing_deps.append("python3-tk")
        print("❌ tkinter - НЕ НАЙДЕН")
    
    # Проверка requests
    try:
        import requests
        print("✅ requests - OK")
    except ImportError:
        missing_deps.append("python3-requests")
        print("❌ requests - НЕ НАЙДЕН")
    
    # Проверка стандартных библиотек
    std_libs = ['hashlib', 'threading', 'time', 'random', 'socket', 'json', 'datetime', 'queue', 'uuid']
    for lib in std_libs:
        try:
            __import__(lib)
            print(f"✅ {lib} - OK")
        except ImportError:
            print(f"❌ {lib} - НЕ НАЙДЕН")
            return False
    
    if missing_deps:
        print(f"\n📦 Установка недостающих зависимостей: {', '.join(missing_deps)}")
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y'] + missing_deps, check=True, capture_output=True)
            print("✅ Зависимости установлены успешно!")
        except subprocess.CalledProcessError:
            print("❌ Ошибка установки зависимостей")
            print("Попробуйте установить вручную:")
            print(f"sudo apt install -y {' '.join(missing_deps)}")
            return False
    
    return True

def show_menu():
    """Показать меню выбора режима"""
    print("\n🎯 ЭМУЛЯТОР КРИПТОНОДЫ")
    print("=" * 40)
    print("Выберите режим работы:")
    print("1. 🖥️  Запустить GUI эмулятор")
    print("2. 📊 Показать демонстрацию")
    print("3. 🧪 Запустить тесты")
    print("4. 📚 Показать документацию")
    print("5. 🔧 Расширенный симулятор")
    print("0. ❌ Выход")
    print("=" * 40)

def run_gui_emulator():
    """Запуск GUI эмулятора"""
    print("🚀 Запуск GUI эмулятора...")
    try:
        from crypto_node_emulator import CryptoNodeEmulator
        emulator = CryptoNodeEmulator()
        emulator.run()
    except Exception as e:
        print(f"❌ Ошибка запуска GUI: {e}")
        print("Попробуйте запустить напрямую: python3 crypto_node_emulator.py")

def run_demo():
    """Запуск демонстрации"""
    print("📊 Запуск демонстрации...")
    try:
        subprocess.run([sys.executable, 'demo.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска демонстрации: {e}")

def run_tests():
    """Запуск тестов"""
    print("🧪 Запуск тестов...")
    try:
        subprocess.run([sys.executable, 'test_all.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска тестов: {e}")

def show_documentation():
    """Показать документацию"""
    print("📚 ДОКУМЕНТАЦИЯ")
    print("=" * 40)
    
    docs = [
        ("README.md", "Основная документация"),
        ("USAGE_GUIDE.md", "Руководство пользователя"),
        ("PROJECT_SUMMARY.md", "Краткое описание проекта"),
        ("requirements.txt", "Список зависимостей")
    ]
    
    for filename, description in docs:
        if os.path.exists(filename):
            print(f"📄 {filename} - {description}")
        else:
            print(f"❌ {filename} - НЕ НАЙДЕН")
    
    print("\nДля просмотра документации используйте:")
    print("cat README.md")
    print("cat USAGE_GUIDE.md")
    print("cat PROJECT_SUMMARY.md")

def run_advanced_simulator():
    """Запуск расширенного симулятора"""
    print("🔧 Запуск расширенного симулятора...")
    try:
        subprocess.run([sys.executable, 'advanced_node_features.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска расширенного симулятора: {e}")

def main():
    """Главная функция"""
    print("🎯 ДОБРО ПОЖАЛОВАТЬ В ЭМУЛЯТОР КРИПТОНОДЫ!")
    print("=" * 50)
    
    # Проверка зависимостей
    if not check_dependencies():
        print("\n❌ Не удалось установить зависимости")
        print("Попробуйте установить вручную:")
        print("sudo apt install -y python3-tk python3-requests")
        return
    
    print("\n✅ Все зависимости установлены!")
    
    # Основной цикл меню
    while True:
        show_menu()
        
        try:
            choice = input("\nВведите номер (0-5): ").strip()
            
            if choice == '0':
                print("👋 До свидания!")
                break
            elif choice == '1':
                run_gui_emulator()
            elif choice == '2':
                run_demo()
            elif choice == '3':
                run_tests()
            elif choice == '4':
                show_documentation()
            elif choice == '5':
                run_advanced_simulator()
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()