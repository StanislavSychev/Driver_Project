from sklearn.tree import DecisionTreeClassifier
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.impute import SimpleImputer
from DataPreparator import make_part_list
from ScenariosRader import make_files
from sklearn.model_selection import KFold


def run_des_tree(to_print, to_quest=False, needed_quest=None, save_tree=False):
    data = make_part_list(to_quest, needed_quest)
    scens = data['scen']
    quest_names = data['quest']
    data = data['data']
    quest_importance = {}
    for name in quest_names:
        quest_importance[name] = 0
    feat_imp = {}
    acc_res = {}
    av_ac = 0
    av_ci = 0
    for i in range(len(scens)):
        accuracy = 0
        ac_list = []
        feat_dict = {}
        res_dict = {}
        names = []
        for keys in data:
            # feat_res = data[keys].scens_to_list(i)
            feat_res = data[keys].most_prob(i)
            if feat_res:
                feat_dict[keys] = feat_res[0]
                res_dict[keys] = feat_res[1]
                names = feat_res[2]
        driver_keys = feat_dict.keys()
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        kf.get_n_splits(driver_keys)
        dtr = DecisionTreeClassifier()
        for train, test in kf.split(driver_keys):
            # test_keys = [driver_keys[i_test] for i_test in test.tolist()]
            train_keys = [driver_keys[i_train] for i_train in train.tolist()]
            feat_train = []
            res_train = []
            feat_test = []
            res_test = []
            for keys in feat_dict:
                if keys in train_keys:
                    for lst in feat_dict[keys]:
                        feat_train.append(lst)
                    for lst in res_dict[keys]:
                        res_train.append(lst)
                else:
                    for lst in feat_dict[keys]:
                        feat_test.append(lst)
                    for lst in res_dict[keys]:
                        res_test.append(lst)

            imp = SimpleImputer(missing_values=-1, strategy='mean')
            feat_train.append([0] * len(feat_train[0]))
            imp.fit(feat_train)
            feat_train = imp.transform(feat_train)
            feat_train = feat_train[:-1:]
            feat_test = imp.transform(feat_test)
            dtr = DecisionTreeClassifier()
            dtr.fit(feat_train, res_train)
            ac = 0
            for x_test, y_test in zip(feat_test, res_test):
                ac += dtr.score([x_test], [y_test])
            if len(feat_test) == 0:
                print scens[i]
                print res_test
            ac = ac / len(feat_test)
            ac_list.append(ac)
            accuracy += ac
        if not len(feat_dict):
            print scens[i]
            print feat_dict
        accuracy = accuracy / 10
        err = 0.0
        for item in ac_list:
            err += (item - accuracy) ** 2
        err = (err ** 0.5) / 10
        if save_tree:
            dot_data = StringIO()
            export_graphviz(dtr,
                            out_file=dot_data,
                            filled=True,
                            rounded=True,
                            special_characters=True,
                            feature_names=names)
            graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
            graph.write_png(scens[i] + 'ID3.png')
        acc_res[scens[i]] = scens[i] + ': ' + '%.2f' % accuracy + '\t%.2f' % err
        av_ac += accuracy
        av_ci += err
        importance_list = dtr.feature_importances_
        imp_dct = {}
        for name, imp in zip(names, importance_list):
            if name in quest_importance.keys():
                quest_importance[name] += imp
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
    av_ac = av_ac / 12
    av_ci = av_ci / 12
    for name in quest_importance:
        quest_importance[name] = quest_importance[name] / 12
    quest_importance = [(k, quest_importance[k]) for k in sorted(quest_importance,
                                                                 key=quest_importance.get,
                                                                 reverse=True)]
    if to_print:
        for keys in acc_res:
            print acc_res[keys]
        for keys in feat_imp:
            print keys
            for item in feat_imp[keys]:
                print "\t" + item[0] + ": " + '%.2f' % item[1]
    return av_ac, av_ci, quest_importance


if __name__ == '__main__':
    make_files("procData2", 20, 20, 10, 20)
    run_des_tree(True, True)
