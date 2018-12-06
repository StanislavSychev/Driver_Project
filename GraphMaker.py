import matplotlib.pyplot as plt
import numpy as np
from DesTree import run_des_tree
from Predictor import run_predict
from ScenariosRader import make_files


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
    make_files("procData2", 20, 20, 10, 20)
    _, _, quest_list = run_des_tree(False, True)
    if tree:
        max_res, err, _ = run_des_tree(False, False)
        name = 'ID3'
    else:
        max_res, err = run_predict(False, False)
        name = 'SVM'
    max_num = 0
    res_list = [max_res]
    err_list = [err]
    num_list = [0]
    j = 0
    needed = []
    while j < len(quest_list):
        needed.append(quest_list[j][0])
        print j
        if quest_list[j][1] == 0:
            break
        if tree:
            res, err, _ = run_des_tree(False, True, needed)
        else:
            res, err = run_predict(False, True, needed)
        j += 1
        if res > max_res:
            max_res = res
            max_num = j
        num_list.append(j)
        res_list.append(res)
        err_list.append(err)

    make_graph(num_list, res_list, err_list, name)
