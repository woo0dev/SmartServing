# 무선네트워크 프로젝트 <스마트 자동 배식기>

### * **프로젝트 참여자**
    201744005 김경은
    201744020 박지석
    201644034 정우영

1. 프로젝트 개요
    * 개발 배경/목표
    * 주요 기능
    * 설계
2. 개발 준비
    * 제작 재료 목록
    * 개발 일정
3. 개발 과정
    * 개발 환경
    * 구현 과정
    * 문제 해결
4. 개발 결과
    * 결과 화면
    * 개선 방향


# 1. 프로젝트 개요
***
- ### 스마트 자동 배식기란?
    - 어플을 이용해 사료 배급이 가능하고 카메라를 통해 실시간으로 반려동물을 확인할 수 있는<br>화면으로 이루어진 애플리케이션 

- ### 개발 배경
    - 어린 강아지 같은 경우 항상 일정한 시간에 개월 수에 따라 급식해야하는 사료랑이 다른데<br>이를 스마트 자동 급식기를 사용하면 밖에서도 편리하게 관리 가능
    - 최근 반려동물을 기르는 1인 가구가 증가함에 따라 약속, 야근등과 같은 반려동물이 불가피하게<br>혼자 있어야 할 상황에 대비하기 위해

- ### 목표
    - 원격지원을 통한 다양한 반려동물 케어 서비스 제공

- ### 주요 기능
    - 앱 내부의 버튼을 통한 사료 배식 기능
    - 앱 내부의 화면을 통한 실시간 반려동물 확인 및 관리 기능
   
- ### 설계 
     <img src="./img/회로도.png"><br>
     <img src="./img/설계.jpg">
<br>
  
# 2. 개발 준비
***
- ### 제작재료
    | 재료 | 구매주소 | 수량 | 가격대 |
    |---|---|---|---|
    | 라즈베리파이 | 실습용 | 1 | 실습용 |
    | L298N 모터 | 실습용 | 1 | 실습용 | 
    | DC 모터 | 실습용 | 1 | 실습용 |
    | 캠 | 실습용 | 1 | 실습용 |
    | 급식기 | https://url.kr/w3laor | 1 | 17,400 |

- ### 개발 일정
    | 항목 | 세부내용 및 개발 항목 | 개발자 | 시작일 | 종료일 |
    |---|---|---|---|---|
    | 아이디어 | 주제 선정 및 분석 개발 준비 | 김경은 | 11/8 | 11/11 |
    | 요구사항 분석 | 요구 분석 및 자료 조사 | 팀 전원 | 11/12 | 11/15 |
    | 장비 | 장비 마련, 재료 선정 및 준비 | 팀 전원 | 11/16 | 11/22 |
    | 관련분야 연구 | 주요 기술 연구 및 분석 | 팀 전원 | 11/23 | 11/28 |
    | 관련분야 설계 | 관련 시스템 분석, 시스템 설계 | 김경은 | 11/29 | 12/2 |
    | 설계 구현 | 코딩 및 모듈 테스트 | 박지석, 정우영 | 12/3 | 12/9 |
    | 테스트 | 시스템 테스트 | 팀 전원 | 12/3 | 12/9 | 4-5
    
 - ### 간트 차트
     <img src="./img/개발일정.png">
    
# 3. 개발 과정
***
- ### 개발 환경
    - Raspbian: 라즈베리파이에 최적화, Xwindow를 사용할 수 있는 OS  
    - VNC Viewer: 라즈베리를 원격으로 다루기 위해 사용하는 원격 데스크톱 클라이언트
    - GitHub: 소프트웨어 개발 프로젝트를 위한 소스코드 관리서비스, 버전 관리를 위해 사용
    - AndroidStudio: 안드로이드 전용 어플(앱) 제작을 위한 통합 개발 환경(IDE)<br>
- ### 구현 과정
    - #### 소켓 통신 서버 구현
	    - 소켓 서버 
	    <pre><code>
	    import socket
	    from subprocess import call

	    HOST = ""
	    PORT = 8282
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    print ('Socket created')
	    s.bind((HOST, PORT))
	    print ('Socket bind complete')
	    s.listen(1)
	    print ('Socket now listening')

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
	    </code></pre>

    - #### 모터 제어 구현
	   - ServoBlaster 설치
	    <pre><code> pi@raspberrypi:~ $ sudo git clone https://github.com/richardghirst/PiBits </code></pre>

	    - echo 명령어로 모터 제어
	    <pre><code> pi@raspberrypi:~ $ echo 0=150 > /dev/servoblaster </code></pre>

	   - 서버파일에 ServoBlaster 코드 추가
	    <pre><code>
	    def do_some_stuffs_with_input(input_string):
	    pan_pos=0
	    max_pos=300
	    
	    // 라즈베리파이를 컨트롤할 명령어 설정
	    if input_string == "FEED":
		pan_pos +=100
		if pan_pos >=max_pos:
		    pan_pos =max_pos
		input_string = "사료를 배급합니다.."
		call("echo 0="+str(pan_pos)+"%"+" > /dev/servoblaster", shell= True)
	    else :
		input_string = input_string + " 없는 명령어 입니다."
	    return input_string
	    </pre></code>
	    
    - #### 실시간 캠 구현
	   - 스트리밍 프로그램 motion 설치
	    <pre><code> pi@raspberrypi:~ $ sudo apt-get install motion </code></pre>

	   - motion service 실행
	    <pre><code> pi@raspberrypi:~ $ sudo service motion start </code></pre>
	    
	   - 스트리밍 화면 확인
	    <pre><code> http://[라즈베리파이IP주소]:[포트번호] </code></pre>
	    
    - #### 안드로이드 소켓 통신 구현
	<img width="{30%" src="./img/socket.png">
	
    - #### 안드로이드 WebView 구현
    	<img width="{80%" src="./img/webview.png">

- ### 문제 해결
    - #### WebView가 정상적으로 동작하지 않는 문제(ERR_CLEARTEXT_NOT_PERMITTIED)
    	<img src="./img/android-error.jpeg" width="150" height="300">
	#### 해결방법 - Manifest 파일에 아래 코드 추가
	<img src="./img/webViewError.png">
	<img src="./img/internetPermission.png">
	
    - #### 실시간 스트리밍화면이 끊기는 문제
	#### 해결방법 - /etc/motion/motion.conf 파일에 아래 코드 
	<img src="./img/스트리밍에러_1.png">
	<img src="./img/스트리밍에러_2.png">
# 4. 개발 결과
***
- ### 결과 화면
    * **사료배급 어플 화면**<br>
    <img src="./img/사료배급_1.jpeg">
    <img src="./img/사료배급.jpeg">
    * **사료배급 기능**<br>
       <img width="{80%" src="./gif/cctv.gif">
    * **CCTV 기능**<br>
       <img width="{80%" src="./gif/사료배급.gif"><br><br>
       
- ### 개선 방향
-  #### 포트포워딩: 같은 공간이 아닌 사용자가 밖에서 다른 네트워크를 사용할 때 제어할 수 있도록 적용시키지 않은 것이 아쉽다.
-  #### 모터 속도: 서보블라스터를 사용하니 일반적인 모터보다 속도와 힘이 훨씬 약한 것을 확인했다. 속도 제어를 사용자가 원하는 만큼 제어 가능하게 코드를 수정 및 보완할 예정이다.
-  #### 모터 고정: 배식기와 모터 구조상 테이프나 본드로 제대로 부착하기에 어려움이 있었다. 3d프린터로 모터와 배식기 사이의 구성품을 설계하거나 글루건을 사용해 모터를 직접 제대로 부착하지 못한 것이 아쉽다. 
