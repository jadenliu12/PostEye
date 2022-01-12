import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import skmultilearn
from sklearn.model_selection import train_test_split
# ML Pkgs
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.metrics import accuracy_score,hamming_loss,classification_report
from skmultilearn.problem_transform import BinaryRelevance
# Multi Label Pkgs


url = "Posteye_data.csv"
dataset = pd.read_csv(url)

class binary_relevance:
    def __init__(self, url, dataset):
        self.url = url
        self.dataset = dataset
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data()
        self.model = self.train_model()
    def split_data(self):
        X = self.dataset.iloc[:,0].values
        Y = self.dataset.iloc[:,1:3].values
        X = np.array(X)
        Y = np.array(Y)
        X = X.reshape(-1,1)
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size = 0.4,random_state=1)
        return X_train, X_test, y_train, y_test

    def train_model(self):
        binary_rel_clf = BinaryRelevance(GaussianNB())
        model = binary_rel_clf.fit(self.X_train,self.y_train)
        return model
        
    def predict(self,input):
        br_prediction = self.model.predict(input)
        # print(br_prediction.toarray())
        # print(accuracy_score(y_test,br_prediction))
        # print(hamming_loss(y_test,br_prediction))
        return br_prediction.toarray()
br = binary_relevance(url, dataset)
X_train, X_test, y_train, y_test = br.split_data()

print(br.predict(np.array(20).reshape(-1,1)))