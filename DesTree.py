from sklearn.tree import DecisionTreeClassifier
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.impute import SimpleImputer
from DataPreparator import make_part_list
from sklearn.model_selection import KFold


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

        imp = SimpleImputer(missing_values=-1, strategy='mean')
        X_train.append([0]*len(X_train[0]))
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        X_train = X_train[:-1:]
        X_test = imp.transform(X_test)
        dtr = DecisionTreeClassifier()
        dtr.fit(X_train, Y_train)
        ac = 0
        for x_test, y_test in zip(X_test, Y_test):
            ac += dtr.score([x_test], [y_test])
        if len(X_test) == 0:
            print scens[i]
            print Y_test
        ac = ac / len(X_test)
        ac_list.append(ac)
        accuracy += ac
    if not len(X_dict):
        print scens[i]
        print X_dict
    accuracy = accuracy / 10
    err = 0.0
    for item in ac_list:
        err += (item - accuracy) ** 2
    err = (err ** 0.5) / 10

    dot_data = StringIO()
    eg = export_graphviz(dtr, out_file=dot_data,
                         filled=True, rounded=True,
                         special_characters=True,
                         feature_names=names)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(scens[i] + 'ID3.png')
    acc_res[scens[i]] = scens[i] + ': ' + '%.2f' % accuracy + '\t%.2f' % err
    importance_list = dtr.feature_importances_
    imp_dct = {}
    for name, imp in zip(names, importance_list):
        if name[-2] == '/':
            key = name[:-5:]
            if key not in imp_dct.keys():
                imp_dct[key] = 0
            imp_dct[key] += imp

        else:
            imp_dct[name] = imp
    if sum(importance_list):
        lst = [(k, imp_dct[k]) for k in imp_dct]
        lst.sort(key=lambda x: x[1], reverse=True)
        feat_imp[scens[i]] = lst
    else:
        feat_imp[scens[i]] = []
for keys in acc_res:
    print acc_res[keys]
for keys in feat_imp:
    print keys
    for item in feat_imp[keys]:
        print "\t" + item[0] + ": " + '%.2f' % item[1]
