import idx2numpy
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

train_images_path = r"e:\peixun\CCNU_Python\test7\MNIST_data\train-images.idx3-ubyte"
train_labels_path = r"e:\peixun\CCNU_Python\test7\MNIST_data\train-labels.idx1-ubyte"
test_images_path = r"e:\peixun\CCNU_Python\test7\MNIST_data\t10k-images.idx3-ubyte"
test_labels_path = r"e:\peixun\CCNU_Python\test7\MNIST_data\t10k-labels.idx1-ubyte"

train_images = idx2numpy.convert_from_file(train_images_path)
train_labels = idx2numpy.convert_from_file(train_labels_path)
test_images = idx2numpy.convert_from_file(test_images_path)
test_labels = idx2numpy.convert_from_file(test_labels_path)

n_train = train_images.shape[0]
n_test = test_images.shape[0]
X_train = train_images.reshape((n_train, -1)) / 255.0
X_test = test_images.reshape((n_test, -1)) / 255.0

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

y_train = train_labels
y_test = test_labels

parameters = {"C": [0.01, 0.05, 0.1, 0.2]}
model = LogisticRegression(max_iter=5000, solver='lbfgs', multi_class='multinomial')

clf = GridSearchCV(model, parameters, cv=3, scoring='accuracy', n_jobs=-1)
clf.fit(X_train, y_train)

print("最佳参数:", clf.best_params_)

y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("测试集准确率: {:.2f}%".format(acc * 100))