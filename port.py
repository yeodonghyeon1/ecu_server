import socket
import os

def recv_file(sock, filename):
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(4096)
            # print(data)
            if b'--EOF--' in data:
                f.write(data[:data.find(b'--EOF--')])
                break
            f.write(data)

def main():
    host = '192.168.112.1'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print('서버가 시작되었습니다.')
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f'{addr}에 연결됨')
        while True:
            try:
                data = client_socket.recv(4096)
                load = ""
                print("들어온 데이터: ", data.decode())
                if data.decode() == 'LCA':

                    load = "../camera/org_video"
                    list_file = ""
                    for i in os.listdir(load):
                        i = i + " "
                        list_file = list_file + i
                    
                    load = "../camera/cv_video"
                    
                    for i in os.listdir(load):
                        i = i + " "
                        list_file = list_file + i
                    if list_file == "":
                        list_file = "NOT_FILE"
                    list_file = "LCA " + list_file
                    client_socket.send(list_file.encode())
                if not data:
                    break

                filename_end_idx = data.find(b'--EOF--')
                if filename_end_idx != -1:
                    filename = data[:filename_end_idx].decode()
                    dataname = filename[0:3]
                    filename = filename[3:]
                    data = data[filename_end_idx + len(b'--EOF--'):]
                    print(f'파일 이름 수신: {filename}')
                    if filename == None:
                        print("None")
                    if filename == "":
                        print("sd")
                        client_socket.send(b"--ERORR--")
                        continue
                    print(dataname)
                    if dataname == "ORG":
                        save_path = os.path.join('../camera/org_video', filename)
                    elif dataname == "CVV":
                        save_path = os.path.join('../camera/cv_video', filename)
                    recv_file(client_socket, save_path)
                    print(f'{filename} 파일이 성공적으로 저장되었습니다.')
                    # client_socket.send(b'ok')  # 다음 파일 준비 완료
            except:
                pass
        client_socket.close()
        print('연결 종료')

    server_socket.close()

if __name__ == '__main__':
    main()