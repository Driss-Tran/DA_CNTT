from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif


class MachineLearning():

    def __init__(self):
        print("Loading dataset ...")

        self.counter = 0

        self.flow_dataset = pd.read_csv('FlowStatsfile.csv')

        self.flow_dataset.iloc[:, 2] = self.flow_dataset.iloc[:, 2].str.replace('.', '')
        self.flow_dataset.iloc[:, 3] = self.flow_dataset.iloc[:, 3].str.replace('.', '')
        self.flow_dataset.iloc[:, 5] = self.flow_dataset.iloc[:, 5].str.replace('.', '')

        self.X_flow = self.flow_dataset.iloc[:, :-1].values
        self.X_flow = self.X_flow.astype('float64')

        self.y_flow = self.flow_dataset.iloc[:, -1].values

        self.X_flow_train, self.X_flow_test, self.y_flow_train, self.y_flow_test = train_test_split(self.X_flow, self.y_flow, test_size=0.25, random_state=0)

        # Apply Univariate Feature Selection
        self.selector = SelectKBest(score_func=f_classif, k=10)
        self.X_flow_train = self.selector.fit_transform(self.X_flow_train, self.y_flow_train)
        self.X_flow_test = self.selector.transform(self.X_flow_test)

        # Get the list of selected feature indices
        self.selected_features = self.selector.get_support(indices=True)

        # Print the names of the selected features
        print("Selected features: ", self.flow_dataset.columns[self.selected_features])


    def LR(self):

        print("------------------------------------------------------------------------------")
        print("Logistic Regression ...")

        self.classifier = LogisticRegression(solver='liblinear', random_state=0)

        self.Confusion_matrix()

    def KNN(self):

        print("------------------------------------------------------------------------------")
        print("K-NEAREST NEIGHBORS ...")

        self.classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)

        self.Confusion_matrix()

    def NB(self):

        print("------------------------------------------------------------------------------")
        print("NAIVE-BAYES ...")

        self.classifier = GaussianNB()

        self.Confusion_matrix()


    def DT(self):

        print("------------------------------------------------------------------------------")
        print("DECISION TREE ...")

        self.classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)

        self.Confusion_matrix()

    def RF(self):

        print("------------------------------------------------------------------------------")
        print("RANDOM FOREST ...")

        self.classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=0)

        self.Confusion_matrix()

    def Confusion_matrix(self):
        self.counter += 1

        self.flow_model = self.classifier.fit(self.X_flow_train, self.y_flow_train)

        self.y_flow_pred = self.flow_model.predict(self.X_flow_test)

        print("------------------------------------------------------------------------------")

        print("confusion matrix")
        cm = confusion_matrix(self.y_flow_test, self.y_flow_pred)
        print(cm)

        acc = accuracy_score(self.y_flow_test, self.y_flow_pred)

        print("succes accuracy = {0:.2f} %".format(acc*100))
        fail = 1.0 - acc
        print("fail accuracy = {0:.2f} %".format(fail*100))
        print("------------------------------------------------------------------------------")

        x = ['TP','FP','FN','TN']
        x_indexes = np.arange(len(x))
        width = 0.10
        plt.xticks(ticks=x_indexes, labels=x)
        plt.title("Algorithm Results")
        plt.xlabel('Predicted Class')
        plt.ylabel('Number of Flows')
        plt.tight_layout()
        if self.counter == 1:
            y1 = [cm[0][0],cm[0][1],cm[1][0],cm[1][1]]
            plt.bar(x_indexes-2*width,y1, width=width, color="#1b7021", label='LR')
            plt.legend()
        if self.counter == 2:
            y2 = [cm[0][0],cm[0][1],cm[1][0],cm[1][1]]
            plt.bar(x_indexes-width,y2, width=width, color="#e46e6e", label='KNN')
            plt.legend()
        if self.counter == 3:
            y3 = [cm[0][0],cm[0][1],cm[1][0],cm[1][1]]
            plt.bar(x_indexes,y3, width=width, color="#0000ff", label='NB')
            plt.legend()
        if self.counter == 4:
            y4 = [cm[0][0],cm[0][1],cm[1][0],cm[1][1]]
            plt.bar(x_indexes+width,y4, width=width, color="#e0d692", label='DT')
            plt.legend()
        if self.counter == 5:
            y5 = [cm[0][0],cm[0][1],cm[1][0],cm[1][1]]
            plt.bar(x_indexes+2*width,y5, width=width, color="#000000", label='RF')
            plt.legend()
            plt.show()

    def BMA(self):
        print("------------------------------------------------------------------------------")
        print("Bayesian Model Average ...")

        self.add_model('Logistic Regression', LogisticRegression(solver='liblinear', random_state=0))
        self.add_model('K-NEAREST NEIGHBORS', KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2))

        best_model = self.select_best_model()

    def add_model(self, name, model):
        self.models[name] = model

    def select_best_model(self):
        # Fit all models and compute their scores
        scores = {}
        for name, model in self.models.items():
            model.fit(self.X_flow_train, self.y_flow_train)
            scores[name] = model.score(self.X_flow_test, self.y_flow_test)

        # Select the model with the highest score
        best_model_name = max(scores, key=scores.get)
        best_model = self.models[best_model_name]

        print(f"Best model: {best_model_name}")

        return best_model

def main():

    start_script = datetime.now()

    ml = MachineLearning()

    start = datetime.now()
    ml.LR()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    start = datetime.now()
    ml.KNN()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    start = datetime.now()
    ml.NB()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    start = datetime.now()
    ml.DT()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    start = datetime.now()
    ml.RF()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    end_script = datetime.now()
    print("Script Time: ", (end_script-start_script))

main()