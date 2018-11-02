from os import listdir
import pandas as pd
import numpy


def data_sifer(read_dir, write_dir, safe_distance1, safe_distance2, safe_distance3, safe_distance4, dec_distance):

    for files in listdir(read_dir):
        read_file_path = read_dir + "/" + files
        write_file_path = write_dir + "/" + files
        data = pd.read_csv(read_file_path, sep=';')
        if files == "Attention_1.csv":
            #data = data[['ParticipantID', 'Endedwithcollision', 'Changeindistance']]
            for i in range(0, data['Changeindistance'].count()):
                if data['Changeindistance'].ix[i] > 0:
                    data.set_value(i, 'Changeindistance', 0)
                else:
                    data.set_value(i, 'Changeindistance', 1)
            #for i in range(0, data['Distancefromturnothercarsignals'].count()):
            #    if data['Distancefromturnothercarsignals'].ix[i] > dec_distance:
            #        data.set_value(i, 'Distancefromturnothercarsignals', 1)
            #    else:
            #        data.set_value(i, 'Distancefromturnothercarsignals', 0)


        #if files == "Communication_1.csv":
            #data = data[['ParticipantID', 'Endedwithcollision', 'Signalled', 'Turndirection']]


        if files == "Contagion_1.csv":
            #data = data[['ParticipantID', 'Meanacceleration']]
            for i in range(0, data['Meanacceleration'].count()):
                if data['Meanacceleration'].ix[i] > 0:
                    data.set_value(i, 'Meanacceleration', 1)
                else:
                    data.set_value(i, 'Meanacceleration', 0)
                if data['Distancetocarahead'].ix[i] == numpy.Inf:
                    #print 'inf'
                    data.set_value(i, 'Distancetocarahead', -1)
                else:
                    pass
                    #data.set_value(i, 'Distancetocarahead', 0)

        if files == "Contagion_2.csv":
            #data = data[['ParticipantID', 'Meanacceleration']]
            for i in range(0, data['Meanacceleration'].count()):
                if data['Meanacceleration'].ix[i] > 0:
                    data.set_value(i, 'Meanacceleration', 0)
                else:
                    data.set_value(i, 'Meanacceleration', 1)
                if data['Distancetocarbehind'].ix[i] == numpy.Inf:
                    #print 'inf'
                    data.set_value(i, 'Distancetocarbehind', -1)

        if files == "Cooperation_1.csv":
            for i in range(0, data['Accelerationrate'].count()):
                if data['Accelerationrate'].ix[i] > 0:
                    data.set_value(i, 'Accelerationrate', 0)
                else:
                    data.set_value(i, 'Accelerationrate', 1)

        # if files == "Cooperation_2.csv":

        #if files == "Cooperation_3.csv":
            #data = data[['ParticipantID', 'Othercarletin', 'Endedwithcollision']]

        if files == "Trust_1.csv":
            #data = data[['ParticipantID', 'Distancetocarbehind']]
            for i in range(0, data['Distancetocarbehind'].count()):
                if data['Distancetocarbehind'].ix[i] > safe_distance1:
                    data.set_value(i, 'Distancetocarbehind', 1)
                else:
                    data.set_value(i, 'Distancetocarbehind', 0)

        if files == "Trust_2.csv":
            #data = data[['ParticipantID', 'Distancetocarbehind', 'Distancetocarahead']]
            for i in range(0, data['Distancetocarbehind'].count()):
                if data['Distancetocarbehind'].ix[i] > safe_distance2:
                    data.set_value(i, 'Distancetocarbehind', 1)
                else:
                    data.set_value(i, 'Distancetocarbehind', 0)
            for i in range(0, data['Distancetocarahead'].count()):
                if data['Distancetocarahead'].ix[i] > safe_distance2:
                    data.set_value(i, 'Distancetocarahead', 1)
                else:
                    data.set_value(i, 'Distancetocarahead', 0)

        #if files == "Trust_3.csv":
            #data = data[['ParticipantID', 'Signalled']]

        if files == "Trust_4.csv":
            #data = data[['ParticipantID', 'Signalled', 'Distancetocarinadjacentlane']]
            for i in range(0, data['Distancetocarinadjacentlane'].count()):
                if data['Distancetocarinadjacentlane'].ix[i] > safe_distance3:
                    data.set_value(i, 'Distancetocarinadjacentlane', 1)
                else:
                    data.set_value(i, 'Distancetocarinadjacentlane', 0)

        if files == "Trust_5.csv":
            #data = data[['ParticipantID', 'Signalled', 'Distancetocarbehind']]
            for i in range(0, data['Distancetocarbehind'].count()):
                if data['Distancetocarbehind'].ix[i] > safe_distance4:
                    data.set_value(i, 'Distancetocarbehind', 1)
                else:
                    data.set_value(i, 'Distancetocarbehind', 0)

        data.to_csv(write_file_path, index=False)
