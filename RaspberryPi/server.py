import socket
from subprocess import call

HOST = ""
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
s.bind((HOST, PORT))
print ('Socket bind complete')
s.listen(1)
print ('Socket now listening')

#파이 컨트롤 함수
def do_some_stuffs_with_input(input_string):
    global pan_pos

	#라즈베리파이를 컨트롤할 명령어 설정
	if input_string == "left":
                pan_pos +=10
                if pan_pos >=max_pos:
                    pan_pos =max_pos
		input_string = "서보모터 좌회전 합니다."
                call("echo 0="+str(pan_pos)+" > /dev/servoblaster", shell= True)
	else :
		input_string = input_string + " 없는 명령어 입니다."
	return input_string

while True:
	#접속 승인
	conn, addr = s.accept()
	print("Connected by ", addr)

	#데이터 수신
	data = conn.recv(1024)
	data = data.decode("utf8").strip()
	if not data: break
	print("Received: " + data)

	#수신한 데이터로 파이를 컨트롤 
	res = do_some_stuffs_with_input(data)
	print("파이 동작 :" + res)

	#클라이언트에게 답을 보냄
	conn.sendall(res.encode("utf-8"))
	#연결 닫기
	conn.close()
s.close()
