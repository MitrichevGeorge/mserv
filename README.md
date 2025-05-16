``` python
import socket
import pyautogui
import json
import logging
import signal
import sys

# Настройки
HOST = '0.0.0.0'  # Слушать все интерфейсы
PORT = 12345
pyautogui.FAILSAFE = False  # Отключить защиту от резких движений

# Настройка логирования
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Глобальная переменная для сокета
server_socket = None

def signal_handler(sig, frame):
    """Обработчик сигналов для graceful shutdown."""
    logging.info("Получен сигнал завершения. Закрываем сервер.")
    if server_socket:
        server_socket.close()
    sys.exit(0)

def main():
    global server_socket
    # Регистрируем обработчик сигналов
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Создаем сокет
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        logging.info(f"Сервер запущен на {HOST}:{PORT}")
        print(f"Сервер запущен на {HOST}:{PORT}. Логи записываются в server.log")
    except Exception as e:
        logging.error(f"Ошибка запуска сервера: {e}")
        sys.exit(1)

    while True:
        try:
            client_socket, addr = server_socket.accept()
            logging.info(f"Подключен клиент: {addr}")
            
            try:
                while True:
                    # Получаем данные от клиента
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    data = data[:data.index("}")+1]
                    logging.info(f"Получены данные: {data}")
                    
                    # Парсим JSON-команду
                    try:
                        command = json.loads(data)
                        action = command.get('action')
                        x = command.get('x', 0)
                        y = command.get('y', 0)

                        if action == 'move':
                            # Перемещаем курсор
                            pyautogui.moveRel(x, y)
                            logging.info(f"Выполнено перемещение курсора: x={x}, y={y}")
                        elif action == 'left_click':
                            # Клик левой кнопкой
                            pyautogui.click(button='left')
                            logging.info("Выполнен клик левой кнопкой")
                        elif action == 'right_click':
                            # Клик правой кнопкой
                            pyautogui.click(button='right')
                            logging.info("Выполнен клик правой кнопкой")

                    except json.JSONDecodeError:
                        logging.error("Ошибка парсинга команды")
            
            except Exception as e:
                logging.error(f"Ошибка при обработке клиента {addr}: {e}")
            
            finally:
                client_socket.close()
                logging.info(f"Клиент {addr} отключен")

        except KeyboardInterrupt:
            logging.info("Сервер остановлен пользователем")
            break
        except Exception as e:
            logging.error(f"Ошибка сервера: {e}")

    if server_socket:
        server_socket.close()

if __name__ == "__main__":
    main()
```
