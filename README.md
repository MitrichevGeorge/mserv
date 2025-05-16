```
import socket
import pyautogui
import json

# Настройки
HOST = '0.0.0.0'  # Слушать все интерфейсы
PORT = 12345
pyautogui.FAILSAFE = False  # Отключить защиту от резких движений

def main():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")
        
        try:
            while True:
                # Получаем данные от клиента
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                data = data[:data.index("}")+1]
                print(data)
                
                # Парсим JSON-команду
                try:
                    command = json.loads(data)
                    action = command.get('action')
                    x = command.get('x', 0)
                    y = command.get('y', 0)

                    if action == 'move':
                        # Перемещаем курсор
                        pyautogui.moveRel(x, y)
                    elif action == 'left_click':
                        # Клик левой кнопкой
                        pyautogui.click(button='left')
                    elif action == 'right_click':
                        # Клик правой кнопкой
                        pyautogui.click(button='right')

                except json.JSONDecodeError:
                    print("Ошибка парсинга команды")
        
        except Exception as e:
            print(f"Ошибка: {e}")
        
        finally:
            client_socket.close()
            print(f"Клиент {addr} отключен")

if __name__ == "__main__":
    main()
```
