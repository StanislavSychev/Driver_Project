
import copy


class Participant(object):

    def __init__(self, lst=[], names=[]):
        self.scenario_list = lst
        self.names = names

    def add_scenario(self, dct, name):
        self.scenario_list.append(dct)
        self.names.append(name)

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

    def scens_to_list(self, scenatio_number):
        lst = []
        names = []
        for i in range(len(self.scenario_list)):
            if i != scenatio_number:
                sum_lst = self.sum_scen_keys(i)
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
        for key in self.scenario_list[scenatio_number]:
            res1.append(self.scenario_list[scenatio_number][key])
            clst = copy.deepcopy(lst)
            #print len(self.scenario_list[scenatio_number])
            try:
                scen_lst = key.split()
                if flag:
                    flag = False
                    for i in range(len(scen_lst) / 2):
                        names.append(scen_lst[2 * i])
                for i in range(len(scen_lst) / 2):
                    clst.append(scen_lst[2 * i + 1])
            except AttributeError:
                pass
            #clst.append(key)
            clst = tuple(clst)
            res0.append(clst)
            res = (res0, res1, names)
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

