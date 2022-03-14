
import os
import pickle
import numpy as np
import pandas as pd
#import catboost
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

class TRAIN(object):
    def __init__(self):
        self.a = None
        self.data_path = '../data/big_table/'
        self.algorithm_name = 'DecisionTree'

    def sub_train(self):
        algorithm = str(self.algorithm_name + '.csv')
        algorithm = os.path.join(self.data_path, algorithm)
        data = pd.read_csv(algorithm)

        X = data.iloc[:, 1:61]
        y = data.iloc[:, 62]
        # normalize the data attributes
        normalized_X = preprocessing.normalize(X)
        # standardize the data attributes
        standardized_X = preprocessing.scale(X)

        events_name = X.columns
        X = np.array(X)
        y = np.asarray(y, dtype="|S6")
        print(X[0])

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # model = LogisticRegression()
        # model.fit(X_train, y_train)
        #
        # expected = y_test
        # predicted = model.predict(X_test)
        # print(predicted)
        # print(expected)
        # print(metrics.classification_report(expected, predicted))
        # print(metrics.confusion_matrix(expected, predicted))

        #model = ExtraTreesClassifier()
        #model.fit(X, Y)
        # display the relative importance of each attribute
        #print(model.feature_importances_)


        # Build a forest and compute the feature importances
        # std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
        forest = ExtraTreesClassifier(n_estimators=250,
                                      random_state=0)
        forest = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0)
        for _ in range(6):
            print('the %s th training' % (_+1))
            assert len(X) == len(y)
            forest.fit(X, y)
            importances = forest.feature_importances_
            indices = np.argsort(importances)[::-1]

            # Print the feature ranking
            print("Feature ranking:")
            for f in range(X.shape[1]):
                print("%d. feature %d  %s (%f)" % (f + 1, indices[f], events_name[indices[f]], importances[indices[f]]))
            X = pd.DataFrame(X)
            X[X.columns[indices[-10*(_+1):]]] = 0
            print(X[X.columns[-10*(_+1):-10*(_+1)+1]])
            X = np.array(X)
        return indices


    def sub_train2(self):
        algorithm = str(self.algorithm_name + '.csv')
        algorithm = os.path.join(self.data_path, algorithm)
        data = pd.read_csv(algorithm)

        X = data.iloc[:, 1:61]
        y = data.iloc[:, 62]
        # X = X[:500]
        # y = y[:500]
        events_name = X.columns
        X = np.array(X)
        y = np.asarray(y, dtype="|S6")

        Err = []
        Importances = []
        Indices = []
        Events_Name = []
        Itera = 6
        for _ in range(Itera):
            print('the %s th training' % (_ + 1))
            assert len(X) == len(y)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            forest = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0)
            forest.fit(X_train, y_train)
            predicted = forest.predict(X_test)

            assert len(predicted) == len(y_test)
            y_test = np.asarray(y_test).astype(float)
            predicted = np.asarray(predicted).astype(float)
            err = np.mean(np.abs(y_test - predicted)/y_test)
            importances = forest.feature_importances_
            indices = np.argsort(importances)[::-1]

            Err.append(err)
            Indices.append(indices)
            events_Name = []
            importanceS = []
            print("Feature ranking:")
            for f in range(X.shape[1]):
                events_Name.append(events_name[indices[f]])
                importanceS.append(importances[indices[f]])
                print("%d. feature %d  %s (%f)" % (f + 1, indices[f], events_name[indices[f]], importances[indices[f]]))
            Events_Name.append(events_Name)
            Importances.append(importanceS)
            if _ < Itera-1:
                X = pd.DataFrame(X)
                X[X.columns[indices[-10*(_+1):]]] = 0
                #print(X[X.columns[-10*(_+1):-10*(_+1)+1]])
                X = np.array(X)
            print('Error: ', err*100, '%')

        Min_index = Err.index(min(Err))
        for f in range(X.shape[1]):
            print("%d. lowest error feature %d  %s (%f)" % (f + 1, Indices[Min_index][indices[f]],
                                               events_name[Indices[Min_index][f]], Importances[Min_index][f]))
        res = {}
        res['result'] = [Err, Indices, Events_Name, Importances]

        output = open('result_'+self.algorithm_name+'.pkl', 'wb')
        pickle.dump(res, output)
        return res


    def delete_col(self, data, being_del_col):
        data = data.drop(data.columns[being_del_col])
        return data

    def train(self):
        #being_del_col = self.sub_train()
        res = self.sub_train2()

        return self.a

    def build(self):
        a = self.train()


if __name__ == '__main__':
    train = TRAIN()
    train.__init__()
    train.build()