import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
from DataPreparator import make_part_list
# from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold


def get_score(predictor, x_train, y_train, x_test, y_test):
    if len(np.unique(y_train)) == 1:
        return -1
    predictor.fit(x_train, y_train)
    ac_score = 0
    for x, y in zip(x_test, y_test):
        ac_score += pred.score([x], [y])
    return ac_score / len(x_test)


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
        # XY = data[keys].scens_to_list(i)
        XY = data[keys].most_prob(i)
        if XY:
            X_dict[keys] = XY[0]
            Y_dict[keys] = XY[1]
            names = XY[2]
    driver_keys = X_dict.keys()
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    kf.get_n_splits(driver_keys)
    dtr = DecisionTreeClassifier()
    for train, test in kf.split(driver_keys):
        test_keys = [driver_keys[i_test] for i_test in test.tolist()]
        train_keys = [driver_keys[i_train] for i_train in train.tolist()]
        X_train = []
        Y_train = []
        X_test = []
        Y_test = []
        for keys in X_dict:
            if keys in train_keys:
                for lst in X_dict[keys]:
                    X_train.append(lst)
                for lst in Y_dict[keys]:
                    Y_train.append(lst)
            else:
                for lst in X_dict[keys]:
                    X_test.append(lst)
                for lst in Y_dict[keys]:
                    Y_test.append(lst)

        # print scens[i]
        # print len(X_test[0])
        imp = SimpleImputer(missing_values=-1, strategy='mean')
        X_train.append([0]*len(X_train[0]))
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        X_train = X_train[:-1:]
        # imp.fit(X_test)
        X_test = imp.transform(X_test)
        # pred = SVC()
        pred = GaussianNB()
        ac = get_score(pred, X_train, Y_train, X_test, Y_test)
        ac_list.append(ac)
        accuracy += ac
    accuracy = accuracy / 10
    err = 0.0
    for item in ac_list:
        err += (item - accuracy) ** 2
    err = (err ** 0.5) / 10
    acc_res[scens[i]] = scens[i] + ': ' + '%.2f' % accuracy + '\t%.2f' % err

for keys in acc_res:
    print acc_res[keys]
