
import copy


class Participant(object):

    def __init__(self, lst=[]):
        self.scenario_list = lst

    def add_scenario(self, dct):
        self.scenario_list.append(dct)

    def sum_scen_keys(self, scenario_number):
        flag = True
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

    def scens_to_list(self, scenatio_number, sum=True):
        lst = []
        for i in range(len(self.scenario_list)):
            if i != scenatio_number:
                if sum:
                    sum_lst = self.sum_scen_keys(i)
                else:
                    sum_lst = self.merge_scen_keys(i)
                for items in sum_lst:
                    lst.append(items)
        res = ([], [])
        for key in self.scenario_list[scenatio_number]:
            res[1].append(self.scenario_list[scenatio_number][key])
            clst = copy.deepcopy(lst)
            clst.append(key)
            res[0].append(clst)
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
        for i in range(len(res[1])):
            res[1][i] = res[1][i].index(max(res[1][i]))
        return res

