import socket
import os

def recv_file(sock, filename):
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(4096)
            if b'--EOF--' in data:
                f.write(data[:data.find(b'--EOF--')])
                break
            f.write(data)

def main():
    host = '0.0.0.0'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print('서버가 시작되었습니다.')
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f'{addr}에 연결됨')

        while True:
            data = client_socket.recv(4096)
            print(data)
            if data.decode() == 'LCA':
                load = "../ecu_server/org_video"
            elif data.decode() == 'LCB':
                load = "../ecu_server/cv_video"

            if data.decode()[0:1] == "LC":
                list_file = ""
                for i in os.listdir(load):
                    i = i + " "
                    list_file = list_file + i
                if list_file == "":
                    list_file = "NOT_FILE"
                client_socket.send(list_file.encode())
            if not data:
                break

            filename_end_idx = data.find(b'--EOF--')
            if filename_end_idx != -1:
                filename = data[:filename_end_idx].decode()
                dataname = filename[0:2]
                filename = filename[3:]
                data = data[filename_end_idx + len(b'--EOF--'):]
                print(f'파일 이름 수신: {filename}')
                print(data)
                save_path = os.path.join(load, filename)# LCA면 load는 org_video, LCB면 cv_video
                recv_file(client_socket, save_path)
                print(f'{filename} 파일이 성공적으로 저장되었습니다.')
                client_socket.send(b'ok')  # 다음 파일 준비 완료

        client_socket.close()
        print('연결 종료')

    server_socket.close()

if __name__ == '__main__':
    main()