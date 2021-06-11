# boba-cup-checker 사용법

본 프로젝트는 라즈베리파이에서 카메라를 이용하여 컵 유뮤를 확인하는 것을 목표로 한다.


## **실험 환경**
* Raspberry Pi 3
* Python3.7이상

## **설치 방법**
라즈베리파이의 설정 방법은 아래의 링크를 참고.
설치는 아래의 쉘 스크립트를 실행한다.
```
sh install.sh
```
만약 설치가 정상적으로 진행되지 않을 시 수동으로 다음과 같이 설정한다. (libcblas-dev는 정상적으로 설치되지 않아도 상관없다.)
```
pip3 install opencv-python
sudo apt install -y libcblas-dev
sudo apt install -y libhdf5-dev
sudo apt install -y libhdf5-serial-dev
sudo apt install -y libatlas-base-dev
sudo apt install -y libjasper-dev
sudo apt install -y libqtgui4
sudo apt install -y libqt4-test
```
환경설정을 마쳤으면 프로젝트를 가져온다.
```
git clone https://github.com/messy-snail/boba-cup-checker.git
```
해당 경로로 이동하여 정상적으로 동작하는지 확인한다. 이 때 카메라는 반드시 연결되어 있어야 한다.

```
cd boba-cup-checker
python3 main.py -v True
```
## **프로그램 자동 실행 설정**
설정은 아래의 쉘 스크립트를 실행한다.
```
sh auto.sh
```
만약 정상적으로 열리지 않는다면 다음과 같이 수동으로 진행한다.
```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
마지막에 다음과 같이 문자열을 입력한다. 프로그램 실행 인자에 대해서는 다음 챕터를 참고한다.

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-spalsh
# 여기부터 추가
lxterminal -e python3 /home/pi/boba-cup-checker/main.py -i 192.168.100.91 -p 7777
```
## **프로그램 실행 인자**  
프로그램 실행 시 옵션으로 줄 수 있는 인자는 다음과 같다.

* -i(--ip): 서버로 설정할 IP 주소  
* -p(--port): 서버로 설정할 PORT 번호
* -v(--viz): 가시화 옵션으로 True 또는 False를 입력
* -w(--write): 이미지 저장 옵션으로 True 또는 False를 입력
* ~~-d(--delay): 딜레이 옵션으로 0~5초 사이 값을 입력~~
* -c(--counter): 달라진 픽셀 수로 10~245760개 사이 값을 입력 (기본:200)
* -q(--threshold): 민감도로 차이가 얼마만큼 났을 때 달라진 픽셀로 간주할 것인가에 대한 인자. 0~255 사이 값을 입력 (기본:30)
* -o(--open): 침식->팽창 필터링으로 노이즈를 날리는 작업을 한다. 0~5 사이의 값을 입력 (기본:2)
* -l(--left): ROI 설정 옵션으로 왼쪽 몇번째 픽셀부터 크롭할지 설정한다. (기본:0)
* -r(--right): ROI 설정 옵션으로 오른쪽 몇번째 픽셀까지 크롭할지 설정한다. (기본:640)
* -t(--top): ROI 설정 옵션으로 위쪽 몇번째 픽셀부터 크롭할지 설정한다. (기본:0)
* -b(--bot): ROI 설정 옵션으로 아래쪽 몇번째 픽셀까지 크롭할지 설정한다. (기본:480)

각 인자의 사용 예시는 다음과 같다.

```
# boba라는 윈도우 창에 현재 캠 화면을 표시함
python3 main.py -v True
```

```
# boba라는 윈도우 창에 현재 캠 화면을 표시하고, 설정한 ROI로 크롭하여 획득
python3 main.py -v True -l 100 -r 500
```
## **통신 스트링**
### **Input string**
* init: 알고리즘 수행에 필요한 참조 영상을 획득
* stat: cup or nocup 판단 시작
* stop: cup or nocup 판단 종료
* set: 옵션을 설정함(위에서 기술한 프로그램 실행 인자 사용)

```
#가시화를 수행하고, IP주소는 192.168.1.92로 설정, 포트는 7777로 설정함.
set -v True -i 192.168.1.92 -p 7777
```

### **Output string**
* cup: 컵이 있음
* nocup: 컵이 없음
* success: set을 정상적으로 수행함
* fail: set 설정을 실패함

