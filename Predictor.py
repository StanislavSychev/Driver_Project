from os import listdir
import pandas
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import ScenariosRader
from Participant import Participant
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.preprocessing import Imputer
from DataPreparator import make_part_list
from sklearn.svm import SVC

def get_score(predictor, x_train, y_train, x_test, y_test):
    if len(np.unique(y_train)) == 1:
        return 0
    predictor.fit(x_train, y_train)
    ac = 0
    for x, y in zip(x_test, y_test):
        ac += pred.score([x], [y])
    return ac / len(x_test)

data = make_part_list()
scens = data['scen']
data = data['data']
feat_imp = {}
acc_res = {}
for i in range(len(scens)):
    accuracy = 0
    ac_list = []
    X_dict = {}
    Y_dict = {}
    names = []
    for keys in data:
        #XY = data[keys].scens_to_list(i)
        XY = data[keys].most_prob(i)
        if XY:
            X_dict[keys] = XY[0]
            Y_dict[keys] = XY[1]
            names = XY[2]
    for key in X_dict:
        X_train = []
        Y_train = []
        for keys in X_dict:
            if keys != key:
                for lst in X_dict[keys]:
                    X_train.append(lst)
                for lst in Y_dict[keys]:
                    Y_train.append(lst)
        X_test = X_dict[key]
        Y_test = Y_dict[key]

        #print scens[i]
        #print len(X_test[0])
        imp = Imputer(missing_values=-1, strategy='mean')
        X_train.append([0]*len(X_train[0]))
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        X_train = X_train[:-1:]
        #imp.fit(X_test)
        X_test = imp.transform(X_test)

        #if scens[i] == "Trust_3":
            #print names
            #print len(names)
            #for it in X_train:
                #print it
                #print len(it)
        #print X_test[0]
        #print X_train
        #print len(names)
        #X_train = pandas.DataFrame.from_records(X_train, columns=names)
        #dtr = DecisionTreeRegressor()
        pred = SVC()
        ac = get_score(pred, X_train, Y_train, X_test, Y_test)
        ac_list.append(ac)
        accuracy += ac
    accuracy = accuracy / len(X_dict)
    err = 0.0
    for item in ac_list:
        err += (item - accuracy) ** 2
    err = (err ** 0.5) / len(X_dict)
    acc_res[scens[i]] = scens[i] + ': ' + '%.2f' % accuracy + '\t%.2f' % err

for keys in acc_res:
    print acc_res[keys]