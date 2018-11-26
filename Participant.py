import copy
import numpy as np


class Participant(object):

    def __init__(self, lst=[], names=[], leng=[], driver_data={}):
        self.scenario_list = lst
        self.names = names
        self.scenario_len = leng
        self.driver_data = driver_data.copy()

    def set_data(self, data):
        self.driver_data = data.copy()

    def add_scenario(self, dct, name, len_dtc):
        self.scenario_list.append(dct)
        self.names.append(name)
        self.scenario_len.append(len_dtc)

    def sum_scen_keys(self, scenario_number):
        flag = True
        if not self.scenario_list[scenario_number]:
            return None
        s = float(len(self.scenario_list[scenario_number]))
        for keys in self.scenario_list[scenario_number]:
            if flag:
                flag = False
                res = copy.deepcopy(self.scenario_list[scenario_number][keys])
            else:
                for i in range(len(self.scenario_list[scenario_number][keys])):
                    res[i] += self.scenario_list[scenario_number][keys][i]
        for i in range(len(res)):
            res[i] = res[i] / s
        return res

    def merge_scen_keys(self, scenario_number):
        res = []
        for key in self.scenario_list[scenario_number]:
            for item in self.scenario_list[scenario_number][key]:
                res.append(item)
        return res

    def scens_to_list(self, scenatio_number):
        lst = []
        names = []
        for i in range(len(self.scenario_list)):
            if i != scenatio_number:
                sum_lst = self.sum_scen_keys(i)
                if not sum_lst:
                    sum_lst = [-1] * self.scenario_len[i]
                if len(sum_lst) != self.scenario_len[i]:
                    print "wtf"
                #print len(sum_lst)
                j = 0
                for items in sum_lst:
                    lst.append(items)
                    names.append(self.names[i] + ": " + str(j) + "/" + str(len(sum_lst) - 1))
                    j += 1
        number_of_contexts = len(self.scenario_list[scenatio_number]) - 1

        #names.append("context " + str(number_of_contexts))
        #res = ([], [], names)
        res0 = []
        res1 = []
        flag = True
        for name_key in self.driver_data:
            names.append(name_key)
            lst.append(self.driver_data[name_key])
        for key in self.scenario_list[scenatio_number]:
            if sum(self.scenario_list[scenatio_number][key]):
                res1.append(self.scenario_list[scenatio_number][key])
                clst = copy.deepcopy(lst)
                try:
                    scen_lst = key.split()
                    if flag:
                        flag = False
                        for i in range(len(scen_lst) / 2):
                            names.append(scen_lst[2 * i])
                    for i in range(len(scen_lst) / 2):
                        clst.append(float(scen_lst[2 * i + 1]))
                except AttributeError:
                    pass
                res0.append(clst)
        res = (res0, res1, names)
        if not res1:
            return None
        if not res0:
            return None
        return res

    def normolise(self):
        for dct in self.scenario_list:
            for keys in dct:
                s = float(sum(dct[keys]))
                if s != 0:
                    for i in range(len(dct[keys])):
                        dct[keys][i] = dct[keys][i] / s

    def most_prob(self, scenario_number):
        res = self.scens_to_list(scenario_number)
        if not res:
            return res
        for i in range(len(res[1])):
            res[1][i] = res[1][i].index(max(res[1][i]))
        return res
