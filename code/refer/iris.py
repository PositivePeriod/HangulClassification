import numpy as np
from sklearn.datasets import load_iris
 
iris_dataset = load_iris() # 붓꽃 데이터셋을 적재합니다. 
print(iris_dataset['data'].shape, iris_dataset['target'].shape)


from sklearn.model_selection import train_test_split
 
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], test_size = 0.2)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
# 데이터셋을 랜덤하게 80%의 훈련셋과 20%의 테스트셋으로 분리합니다.
# print(X_train)
# print(y_train)
print("특성1 범위: ", "[", min(X_train[:, 0]), ",", max(X_train[:, 0]), "]")
print("특성2 범위: ", "[", min(X_train[:, 1]), ",", max(X_train[:, 1]), "]")
print("특성3 범위: ", "[", min(X_train[:, 2]), ",", max(X_train[:, 2]), "]")
print("특성4 범위: ", "[", min(X_train[:, 3]), ",", max(X_train[:, 3]), "]")
 

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
print("표준화된 특성1 범위: ", "[", min(X_train_std[:, 0]), ",", max(X_train_std[:, 0]), "]")
print("표준화된 특성2 범위: ", "[", min(X_train_std[:, 1]), ",", max(X_train_std[:, 1]), "]")
print("표준화된 특성3 범위: ", "[", min(X_train_std[:, 2]), ",", max(X_train_std[:, 2]), "]")
print("표준화된 특성4 범위: ", "[", min(X_train_std[:, 3]), ",", max(X_train_std[:, 3]), "]")
 

from sklearn.svm import SVC
 
svm_model = SVC(kernel='rbf', C=8, gamma=0.1)
svm_model.fit(X_train_std, y_train) # SVM 분류 모델 훈련
y_pred = svm_model.predict(X_test_std) # 테스트
print("predicted    라벨:", y_pred)
print("ground-truth 라벨:", y_test)
print("accuracy: {:.2f}".format(np.mean(y_pred == y_test))) # 예측 정확도
 
