import numpy as np
from sklearn.impute import SimpleImputer
from DataPreparator import make_part_list
from ScenariosRader import make_files
from sklearn.svm import SVC
# from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold


def get_score(predictor, x_train, y_train, x_test, y_test):
    if len(np.unique(y_train)) == 1:
        return -1
    predictor.fit(x_train, y_train)
    ac_score = 0
    for x, y in zip(x_test, y_test):
        ac_score += predictor.score([x], [y])
    return ac_score / len(x_test)


def run_predict(to_print, to_quest=False, needed_quest=None):
    data = make_part_list(to_quest, needed_quest)
    scens = data['scen']
    data = data['data']
    # feat_imp = {}
    acc_res = {}
    av_ac = 0
    av_ci = 0
    for i in range(len(scens)):
        accuracy = 0
        ac_list = []
        feat_dict = {}
        res_dict = {}
        # names = []
        for keys in data:
            # feat_res = data[keys].scens_to_list(i)
            feat_res = data[keys].most_prob(i)
            if feat_res:
                feat_dict[keys] = feat_res[0]
                res_dict[keys] = feat_res[1]
                # names = feat_res[2]
        driver_keys = feat_dict.keys()
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        kf.get_n_splits(driver_keys)
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

            # print scens[i]
            # print len(feat_test[0])
            imp = SimpleImputer(missing_values=-1, strategy='mean')
            feat_train.append([0] * len(feat_train[0]))
            imp.fit(feat_train)
            feat_train = imp.transform(feat_train)
            feat_train = feat_train[:-1:]
            # imp.fit(feat_test)
            feat_test = imp.transform(feat_test)
            pred = SVC(gamma='scale')
            # pred = GaussianNB()
            ac = get_score(pred, feat_train, res_train, feat_test, res_test)
            ac_list.append(ac)
            accuracy += ac
        accuracy = accuracy / 10
        err = 0.0
        for item in ac_list:
            err += (item - accuracy) ** 2
        err = (err ** 0.5) / 10
        acc_res[scens[i]] = scens[i] + ': ' + '%.2f' % accuracy + '\t%.2f' % err
        av_ac += accuracy
        av_ci += err
    if to_print:
        for keys in acc_res:
            print acc_res[keys]
    av_ci = av_ci / 12
    av_ac = av_ac / 12
    return av_ac, av_ci


if __name__ == '__main__':
    # make_files("procData2", 20, 20, 10, 20)
    run_predict(True, True)
