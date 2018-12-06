from os import listdir
import pandas
# import ScenariosRader
from Participant import Participant


def make_id_list(drc):
    res = []
    for files in listdir(drc):
        df = pandas.read_csv(drc + "/" + files)
        ids = df['id'].unique()
        for id_item in ids:
            if id_item not in res:
                res.append(id_item)
    return res


def make_part_list(qest_data, neded_keys=None):
    # qest_data = True
    flag = True
    part_list = {}
    scen_list = []
    # ScenariosRader.scen_read("ScenariosFiles", "procData2", sourse_dir, 20, 20, 10, 20)
    uniqe_id = make_id_list("ParsedData")
    for files in listdir("ScenariosFiles"):
        name_list = files
        scen_list.append(name_list)
        res = {}
        data = pandas.read_csv("ParsedData/" + files + ".csv")
        lst_len = data['out'].unique().shape[0]
        for un in uniqe_id:
            if flag:
                part_list[un] = Participant([], [], [])
            res[un] = {}
        #   for con in data['con'].unique():
        #   res[un][con] = [0] * lst_len
        if flag:
            flag = False
        for i in range(data.shape[0]):
            if data['con'].ix[i] not in res[data['id'].ix[i]]:
                res[data['id'].ix[i]][data['con'].ix[i]] = [0] * lst_len
            res[data['id'].ix[i]][data['con'].ix[i]][data['out'].ix[i]] += 1
        for key in res:
            part_list[key].add_scenario(res[key], name_list, lst_len)
    for key in part_list:
        part_list[key].normolise()
    quest_names = []
    if qest_data:
        driver_data = pandas.read_csv("questionnaireData/preQuestionnaire.csv", index_col=0)
        quest_names = driver_data.columns.values.tolist()
        driver_data = driver_data.fillna(0)
        driver_data = driver_data.replace({'gender': r'^[f|F].*'}, {'gender': 1}, regex=True)
        driver_data = driver_data.replace({'gender': r'^[m|M].*'}, {'gender': 2}, regex=True)
        driver_data = driver_data.replace({'gender': r'^h.*'}, {'gender': 0}, regex=True)
        # neded_keys = ['drive_exp', 'drive_freq']
        for key in part_list:
            id_data = driver_data[driver_data.ID == key]
            id_data = id_data.drop(columns=['ID'])
            dct = id_data.to_dict(orient='index')
            dct = dct[dct.keys()[0]]
            need_val = {}
            if neded_keys:
                for n_key in neded_keys:
                    need_val[n_key] = dct[n_key]
                part_list[key].set_data(need_val)
            else:
                part_list[key].set_data(dct)
    return {'data': part_list, 'scen': scen_list, 'quest': quest_names}


if __name__ == '__main__':
    make_part_list(True)
