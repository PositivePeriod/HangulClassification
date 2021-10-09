# HangulClassification
KSA Graduation Research

## PIP
pip install numpy  
pip install scikit-learn  
pip install Pillow
pip install matplotlib
pip install autopep8
pip install pandas
pip install seaborn
pip freeze > requirements.txt

## REFERENCE
### SVM
https://bskyvision.com/851  
https://jeongmin-lee.tistory.com/87  
https://yeoulcoding.tistory.com/106s  
https://namu.wiki/w/%EC%99%84%EC%84%B1%ED%98%95/%ED%95%9C%EA%B8%80%20%EB%AA%A9%EB%A1%9D/KS%20X%201001  
https://hoony-gunputer.tistory.com/entry/opencv-python-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%B3%80%ED%99%94%EC%A3%BC%EA%B8%B0

### Confusion Matrix
[Scikit Docs](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)  
[Confusion Matrix](https://datascienceschool.net/03%20machine%20learning/09.04%20%EB%B6%84%EB%A5%98%20%EC%84%B1%EB%8A%A5%ED%8F%89%EA%B0%80.html)  
Horizontal sum - #True / Vertical sum - #Prediction  

## TODO
"가" 보여줘도 "환" 폰트 맞추기 -> 이를 위해 image용 str 효율적으로 잘 설정해야 할 것 Ex) 팬그램  
폰트 지원 안 되서 image 깨지는 경우 check하기  
애초에 같은 font family는 힘든가? 사람 눈으로도 하기 어렵나? -> 해상도 올리기  
feature는 사진에서도 뽑아내기 쉬운 걸로 할수록 실용성 증가 -> 회전이나 평행성 고려하기  
수학적, 이론적 배경 가능한지 SVM 배워보기  
오차율의 범위를 안정화! -> 실제로는 글자 여러 개를 볼 수 있음 / 증명 가능?  
폰트 100개 이상, KSX1001 2350자 - 정확성 (overall)  
각 글리프에 대해서도 하한선 필요  
colab 가능? GPU나 학교에 있는 좋은 컴퓨터 쓸 수 있는지 알아보기

어떤 문자에 대해서 정확하지 않은가  
상관분석 -> feature 개수 줄이기 -> time 적게 걸리기 
정확도 기준? - 제가 원하는 
오차에서 비슷한 폰트 나오는 거 확인 - 학습 안 시켜도 비슷한 거 찾아가는지?, 완전히 다른 폰트 찾아가는지?
폰트의 비슷함을 반영할 수 있는 방법!, similarity 정량화 가능?, family 반영 Ex) 고딕, 명조 -> 실용성
학습 안 시킨 폰트 넣어서 확인해보기

## SamsungHumanTech
사용한 기술은 명시하되 (출처 표기) 기술 그 자체에 대해 다룰 필요는 없다  
내가 한 것 위주로 ex) 기술의 적용, feature extraction 알고리즘  
기술의 조합, 가져다쓰는 것도 중요  
목표 지정 및 성취, 논리적 proof가 가능하다면 더 좋고 불가능하다면 시뮬레이션 결과로 verify  
적용 및 응용 사례 -> 진취적 목표? 태도?, 기술의 미래, 확장성(향후 연구)  
기술의 부족한 부분을 파악하고 연구 도중에 고치는 것도 중요