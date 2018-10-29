from os import listdir, remove, path
import numpy as np

def check_ID( id):
    try:
        id_num = float(id)
        if id_num > 100:
            return False
        return True
    except ValueError:
        return False

read_dir = "rawData2"
write_dir = "procData2"
open_write_files = {}
scenario_titles = {}
files_list = listdir(read_dir)
for files in listdir(write_dir):
    remove(write_dir+'/'+files)
print files_list
for files in files_list:
    dataf = open(read_dir + "/" + files, "r")
    s = dataf.readline()
    s = s.split('\t')
    current_ent = int(s[0])
    string_list = []
    while s:
        if (s[len(s)-1] == "(Aspect)") or \
                (s[len(s)-1] == "(UnityEngine.GameObject)"):
            s.pop()
        if current_ent == int(s[0]):
            string_list.append(s)
        else:
            if (string_list[1][2] == "Completed"):
                if check_ID(ParticipantID):
                    if string_list[1][1] == "2Scenario":
                        string_list[1][1] = "Scenario"
                    Scenario = string_list[1][3]
                    value_dict = {}
                    string_list = string_list[3:]
                    for lists in string_list:
                        last = lists.pop()
                        key = ''.join(lists[1:])
                        if (key == "Other"):
                            key = "Othercollider"
                            last = "nothing"
                        if (key == "Car"):
                            if (Scenario == "Trust_1") or (Scenario == "Contagion_2"):
                                key = "Carbehind"
                                last = "nothing"
                            else:
                                key = "Carahead"
                                last = "nothing"
                        if (key == "Carinadjacent"):
                            key = "Carinadjacentlane"
                            last = "nothing"
                        value_dict[key] = last
                    scenario_file = write_dir + "/" + Scenario + ".csv"
                    value_dict.pop("time")
                    not_interesting_values = ["Othercollider", "Othercar", "Carahead", "Carbehind"]
                    for value in not_interesting_values:
                        if value in value_dict:
                            value_dict.pop(value)

                    if path.exists(scenario_file):
                        writef = open_write_files[Scenario]
                    else:
                        writef = open(scenario_file, "w")
                        open_write_files[Scenario] = writef
                        writef.write("ParticipantID")
                        scenario_titles[Scenario] = []
                        for column_names in value_dict:
                            writef.write(";" + column_names)
                            scenario_titles[Scenario].append(column_names)
                    writef.write('\n')
                    writef.write(ParticipantID)
                    for column_names in value_dict:
                        column_val = value_dict[column_names].replace(',', '')
                        if column_val == "True":
                            column_val = "1"
                        if column_val == "False":
                            column_val = "0"
                        if column_val == "Right":
                            column_val = "1"
                        if column_val == "Left":
                            column_val = "0"
                        if column_val == "Infinity":
                            column_val = str(np.Inf)
                        if Scenario == "Cooperation_2":
                            if (column_names == "Whowentfirst") or (column_names == "Whoshouldgofirst"):
                                if (column_val.find('Human') != -1):
                                    column_val = "1"
                                else:
                                    column_val = "0"
                        writef.write(";" + column_val)
            elif (current_ent == 2):
                ParticipantID = string_list[3][2]
            string_list = [s]
            current_ent = int(s[0])
        s = dataf.readline()
        if s:
            s = s.split()
