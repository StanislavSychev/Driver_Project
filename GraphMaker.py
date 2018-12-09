import matplotlib.pyplot as plt
import numpy as np
from DesTree import run_des_tree
from Predictor import run_predict
from ScenariosRader import make_files
from DataPreparator import make_part_list


def make_graph(x_list, y_list, e_list, pred_name):
    x = np.array(x_list)
    y = np.array(y_list)
    e = np.array(e_list)

    fig, ax = plt.subplots()
    ax.errorbar(x, y, yerr=e, fmt="ok", capsize=5)
    ax.plot(x, y, 'k')

    ax.set(xlabel='number of questionnaire features', ylabel='accuracy',
           title='Accuracy for ' + pred_name)
    # ax.grid()

    fig.savefig(pred_name + ".png")
    plt.show()


if __name__ == '__main__':
    tree = False
    data = make_part_list(True)
    # make_files("procData2", 20, 20, 10, 20)
    _, _, quest_list = run_des_tree(data)
    if tree:
        max_res, err, _ = run_des_tree(data, quest_list, 1)
        name = 'ID3_sep'
    else:
        max_res, err = run_predict(data, quest_list, 1)
        name = 'SVM_sep'
    max_num = 0
    res_list = [max_res]
    err_list = [err]
    num_list = [1]
    j = 2
    needed = []
    while j < 40:
        # needed.append(quest_list[j][0])
        print j
        # if quest_list[j][1] == 0:
        #     break
        if tree:
            res, err, _ = run_des_tree(data, quest_list, j)
        else:
            res, err = run_predict(data, quest_list, j)
        if res > max_res:
            max_res = res
            max_num = j
        num_list.append(j)
        res_list.append(res)
        err_list.append(err)
        j += 1

    make_graph(num_list, res_list, err_list, name)
