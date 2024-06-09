import socket


class FileClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message):
        self.client_socket.send(message.encode())
        response = self.client_socket.recv(4096).decode()
        return response

    def receive_file(self, filepath):
        with open(filepath, 'wb') as file:
            file_data = self.client_socket.recv(4096)
            file.write(file_data)
        print("Файл успешно скачан.")

    def run(self):
        self.client_socket.connect((self.host, self.port))
        print("Успешно подключено к серверу.")

        print("Введите команды для управления файлами на сервере:")
        while True:
            message = input(" -> ")
            if message.lower() == 'exit':
                response = self.send_message(message)
                print('Ответ сервера: ' + response)
                break

            elif message.lower().startswith('copyfrom'):
                _, filename = message.split()
                self.send_message(message)
                self.receive_file(filename)

            else:
                response = self.send_message(message)
                print('Ответ сервера: ' + response)

        self.client_socket.close()
        print("Соединение закрыто.")


client = FileClient()
client.run()
