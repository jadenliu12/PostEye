import numpy as np
from sklearn.model_selection import train_test_split
# ML Pkgs
from sklearn.naive_bayes import GaussianNB
from skmultilearn.problem_transform import BinaryRelevance
# Multi Label Pkgs

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
        return br_prediction.toarray()
    