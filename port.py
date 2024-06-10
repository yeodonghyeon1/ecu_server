import socket
import os
import ffmpeg
import queue
import threading
import time
def recv_file(sock, filename):
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(4096)
            # print(data)
            if b'--EOF--' in data:
                f.write(data[:data.find(b'--EOF--')])
                break
            f.write(data)

def codec(client_socket):
    global codec_queue
    global stop
    while True:
        if stop == True:
            break
        print("queue size: ", codec_queue.qsize())
        if codec_queue.empty() == False:
            data = codec_queue.get()
            split_data = data.split("-")
            temp_path = split_data[0]
            save_path = split_data[1]
            filename = split_data[2]
            try:
                (
                    ffmpeg
                    .input(temp_path)
                    .output(save_path, vcodec='libx264', acodec='aac')
                    .run(overwrite_output=True)
                )
                print("변환 완료:", save_path)
                client_socket.send(b'ok')  # 다음 파일 준비 완료
            except:
                print("변환 중 에러 발생:")
                client_socket.send(filename.encode())  # 다음 파일 준비 완료
                print(filename)
            try:
                os.remove(temp_path)
            except:
                print("지정된 파일을 찾을 수 없습니다")
        else:
            time.sleep(0.5)

def main():
    global codec_queue
    global stop
    host = '192.168.64.187'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print('서버가 시작되었습니다.')
    one_time = 0
    while True:
        client_socket, addr = server_socket.accept()
        # client_socket.settimeout(120)
        stop = False
        codec_queue_thread = threading.Thread(target=codec, args=(client_socket,))
        codec_queue_thread.daemon = True    
        codec_queue_thread.start()
        print(f'{addr}에 연결됨')

        while True:
            try:
                data = client_socket.recv(4096)
                load = ""
                try:
                    print("들어온 데이터: ", data.decode())
                except:
                    print("데이터 수신 중 에러")
                    client_socket.send(b"--ERORR--")
                    continue
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
                    list_file = "LCA-" + "{}-".format(len(list_file)) + list_file
                    print(list_file)
                    client_socket.send(list_file.encode("utf-8"))
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
                    print(dataname)
                    if dataname == "ORG":
                        temp_path = os.path.join('../camera/temp', filename)
                        save_path = os.path.join('../camera/org_video', filename)
                    elif dataname == "CVV":
                        temp_path = os.path.join('../camera/temp', filename)
                        save_path = os.path.join('../camera/cv_video', filename)
                    try:
                        recv_file(client_socket, temp_path)
                    except:
                        print("파일 저장 중 에러")
                        pass
                    print(f'{filename} 파일이 성공적으로 저장되었습니다.')
                    print(save_path)
                    codec_queue.put("{}-{}-{}".format(temp_path,save_path, filename))
                        #변환

            except:
                print("프로그램 종료")
                break
        stop = True
        client_socket.close()
        print('연결 종료')  

    

if __name__ == '__main__':
    codec_queue = queue.Queue()
    stop = False
    main()
    