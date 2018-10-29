from os import listdir, remove ,path
import pandas

read_dir = "procData2"
flag = False
for files in listdir(read_dir):
    data = pandas.read_csv(read_dir + "/" + files, delimiter=';')
    print str(len(data['ParticipantID'].unique())) + " " + files
    """
    df = data.drop(columns=['ParticipantID'])
    scenario_list = []
    for i in range(2, data['ParticipantID'].count()):
        new_scenario = df.ix[i]
        flag = True
        for seen in scenario_list:
            if new_scenario.equals(seen):
                flag = False
        if flag:
            scenario_list.append(new_scenario)
    print files
    print data['ParticipantID'].count()
    print len(scenario_list)
    #print str(sorted(data['ParticipantID'].unique())) + " " + files
    """

