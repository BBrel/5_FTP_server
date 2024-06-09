import socket
import threading
import os
import shutil


def client_thread(conn, ip, port):
    base_dir = "server_workdir"

    while True:
        try:
            # Получение данных от клиента
            data = conn.recv(4096).decode('utf-8').strip()
            if not data: break  # выход, если данные пусты

            print(f"Received from {ip}:{port} - {data}")
            command, *args = data.split()

            if command == 'LS':  # Посмотреть содержимое папки
                response = '\n'.join(os.listdir(base_dir)) or "Папка пуста"

            elif command == 'MKDIR':  # Создать папку
                os.makedirs(os.path.join(base_dir, *args), exist_ok=True)
                response = "Папка создана"

            elif command == 'RMDIR':  # Удалить папку
                shutil.rmtree(os.path.join(base_dir, *args))
                response = "Папка удалена"

            elif command == 'RM':  # Удалить файл
                os.remove(os.path.join(base_dir, *args))
                response = "Файл удален"

            elif command == 'MV':  # Переименовать файл
                shutil.move(os.path.join(base_dir, args[0]), os.path.join(base_dir, args[1]))
                response = "Файл переименован"

            elif command == 'COPYFROM':  # Скопировать файл с сервера на клиент
                filepath = os.path.join(base_dir, args[0])
                with open(filepath, 'rb') as f:
                    conn.sendall(f.read())
                continue

            elif command == 'EXIT':  # Выход
                response = "Вы отключены от сервера"
                conn.send(response.encode('utf-8'))
                break

            else:
                response = "Неизвестная команда"

            # Отправка ответа клиенту
            conn.send(response.encode('utf-8'))

        except Exception as e:
            print(f"Error handling {ip}:{port} - {e}")
            conn.send(str(e).encode('utf-8'))
    conn.close()  # закрытие соединения
    print(f"Connection {ip}:{port} has been closed.")


def start_server(host="0.0.0.0", port=8080):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((host, port))
    soc.listen(10)
    print(f"Socket now listening")

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print(f"Accepting connection from {ip}:{port}")
        threading.Thread(target=client_thread, args=(conn, ip, port)).start()


start_server()