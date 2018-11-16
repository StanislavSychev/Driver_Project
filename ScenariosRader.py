import DataSifer
from os import listdir
import pandas

def scen_read(scen_dir, read_dir, write_dir, safe_distance1, safe_distance2, safe_distance3, safe_distance4):
    temp_dir = "tmp"
    DataSifer.data_sifer(read_dir, temp_dir, safe_distance1, safe_distance2, safe_distance3, safe_distance4)
    for files in listdir(scen_dir):
        f = open(scen_dir + "/" +files, "r")
        outputs = f.readline().split()
        context = f.readline().split()
        data = pandas.read_csv(temp_dir + "/" + files + ".csv")
        out_data = data[outputs]
        con_data = data[context]
        un_out = out_data.drop_duplicates()
        un_out.index = range(un_out.shape[0])
        if context:
            un_con = con_data.drop_duplicates()
            un_con.index = range(un_con.shape[0])
        pid = data['ParticipantID']
        w = open(write_dir + "/" + files + ".csv", "w")
        w.write("id,con,out\n")
        for i in range(con_data.shape[0]):
            if context:
                s_con = ""
                for item in context:
                    s_con = s_con + item + " " + str(con_data[item].ix[i]) + " "
                w.write(str(pid.ix[i]) + "," + s_con + ",")
            else:
                w.write(str(pid.ix[i]) + ",0,")
            for j in range(un_out.shape[0]):
                if out_data.ix[i].equals(un_out.ix[j]):
                    w.write(str(j) + "\n")
