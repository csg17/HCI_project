# HCI(team project code 2020-1)

## 1.  Introduction: Background and goal of your research

Due to COVID 19's global trend, many schools and universities offer online classes. 
However, since online classes are currently centered on lectures, they have not enough interaction between students and teachers. Through this problem, out team decided to find and apply measures to stimulate insufficient interaction. As a method of activating interaction, the built-in webcam of the laptop and the desktop computer will be used with hand detection and face recognition.
To resolve lack of interaction between teachers and students,  we aim to raise students’ concentration by using visual effects to encourage students. also, we aim to enable teachers to know students’ concentration and understanding during lectures. 

## 2. Usage

### 1. git에서 해당되는 소스파일을 clone 해온다.
git clone https://github.com/csg17/HCI

### 2. 사용한 오픈소스 github주소에 들어가서 필요한 것들을 다운받는다.
  1. https://github.com/jaredvasquez/CNN-HowManyFingers
  img.tgz와 model_6cat.h5를 다운받아서 finger_counting에 넣어준다.  
  1. https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/
  shape_predictor_68_landmarks.dat을 다운받아서 drowsiness&sleep폴더에 넣어준다.  
  1. pyqt 설치하기.
  https://mainia.tistory.com/5604

### 3. 총 3가지의 폴더가 다운로드 받아진다. (drowsiness&sleep, zoom_version2_pyqt2, finger_counting)
  1. 졸거나 하품할 때 알림이 나오는 코드를 실행하려면 drowsiness&sleep을 들어간다.
```bash
cd drowsiness&sleep
python drowsiness_sleep.py --shape-predictor shape_predictor_68_landmarks.dat --alarm alarm.wav
```
  2. 가상의 온라인 학습 창을 실행하기 위해서는 zoom_version2_pyqt 를 들어간다.
```bash
cd zoom_version2_pyqt
```
  3. python app.py
손가락을 counting 해주고 정답인지 아닌지 알려주는 코드를 실행하려면 finger_counting을 들어간다. 
```bash
cd finger_counting
python application.py
```
  4. 교수님 입장의 인터페이스를 pyqt를 통해 보여주는 코드를 실행하려면 prof를 들어간다.
```bash
cd prof
python prof.py
```
