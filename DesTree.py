from os import listdir
import pandas
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import ScenariosRader
from Participant import Participant
from sklearn.externals.six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz
import pydotplus


def make_id_list(dir):
    res = []
    for files in listdir(dir):
        data = pandas.read_csv(dir + "/" + files)
        ids = data['id'].unique()
        for id in ids:
            if id not in res:
                res.append(id)
    return res


def make_part_list():
    flag = True
    part_list = {}
    scen_list = []
    sourse_dir = "ParsedData"
    ScenariosRader.scen_read("ScenariosFiles", "procData", sourse_dir, 1.5, 1.5, 1.5, 1.5, 20)
    uniqe_id = make_id_list(sourse_dir)
    for files in listdir("ParsedData"):
        name = files[:-4:]
        scen_list.append(name)
        res = {}
        data = pandas.read_csv("ParsedData/" + files)
        lst_len = data['out'].unique().shape[0]
        for un in uniqe_id:
            if flag:
                part_list[un] = Participant([], [])
            res[un] = {}
            #for con in data['con'].unique():
            #    res[un][con] = [0] * lst_len
        if flag:
            flag = False
        for i in range(data.shape[0]):
            if data['con'].ix[i] not in res[data['id'].ix[i]]:
                res[data['id'].ix[i]][data['con'].ix[i]] = [0] * lst_len
            res[data['id'].ix[i]][data['con'].ix[i]][data['out'].ix[i]] += 1
        for key in res:
            part_list[key].add_scenario(res[key], name)
    for key in part_list:
        part_list[key].normolise()
    return {'data': part_list, 'scen': scen_list}


data = make_part_list()
scens = data['scen']
data = data['data']
X_dict = {}
Y_dict = {}
feat_imp = {}
for i in range(len(scens)):
    accuracy = 0
    ac_list = []
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
        #for lst_it in X_train:
        #    print len(lst_it)
        #print len(names)
        #print len(X_test[0])
        #X_train = pandas.DataFrame.from_records(X_train, columns=names)
        #dtr = DecisionTreeRegressor()
        dtr = DecisionTreeClassifier()
        dtr.fit(X_train, Y_train)
        ac = 0
        for x_test, y_test in zip(X_test, Y_test):
            ac += dtr.score([x_test], [y_test])
        ac = ac / len(X_test)
        ac_list.append(ac)
        accuracy += ac
    accuracy = accuracy / len(X_dict)
    err = 0.0
    for item in ac_list:
        err += (item - accuracy) ** 2
    err = (err ** 0.5) / len(X_dict)
    print scens[i] + ': ' + '%.2f' % accuracy + '\t%.2f' % err
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
    #print scens[i]
    if sum(importance_list):
        lst = [(k, imp_dct[k]) for k in imp_dct]
        lst.sort(key=lambda x: x[1], reverse=True)
        #for item in lst:
            #print "\t" + item[0] + ": " + '%.2f' % item[1]
        feat_imp[scens[i]] = lst
    else:
        feat_imp[scens[i]] = []
        #print "No tree"

for keys in feat_imp:
    print keys
    for item in feat_imp[keys]:
        print "\t" + item[0] + ": " + '%.2f' % item[1]
    #print dtr.feature_importances_
    #dot_data = StringIO()
    #eg = export_graphviz(dtr,   out_file=dot_data,
    #                            filled=True, rounded=True,
    #                            special_characters=True,
    #                            feature_names=names)
    #graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    #graph.write_png(scens[i] + 'ID3.png')
