from os import listdir
import pandas
import ScenariosRader
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


def make_part_list():
    flag = True
    part_list = {}
    scen_list = []
    sourse_dir = "ParsedData"
    ScenariosRader.scen_read("ScenariosFiles", "procData2", sourse_dir, 20, 20, 10, 20)
    uniqe_id = make_id_list(sourse_dir)
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
    return {'data': part_list, 'scen': scen_list}