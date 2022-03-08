import numpy as np
import matplotlib.pyplot as plt
import csv
from operator import itemgetter

with open('CTC DomEx Case Study Data.csv', 'r') as csv_file:
    #This reads the CVS file with the carton data
    csv_reader = csv.reader(csv_file)
    id_count = 1
    delivery_data = []
    #This loops through all the lines in the csv file and makes a list for each row
    for line in csv_reader:
        cur_list = []
        #the first number in the cartons list is the ID
        cur_list.append(id_count)
        id_count += 1
        dc_location = line[1]
        store_code = line[2]
        mins_late = float(line[5])
        carrier = line[6]
        reason_code = line[8]
        #it will be easier to manipulate this later if its boolean
        if line[7] == "On Time":
            ontime = 0
        else:
            ontime = 1
        cur_list.extend((dc_location, store_code, mins_late, carrier, ontime, reason_code))
        delivery_data.append(cur_list)

print(delivery_data[0])
print(delivery_data[16])
print(delivery_data[64240])

with open('Destination Store Location.csv', 'r') as csv_file:
    #This reads the CVS file with the carton data
    csv_reader = csv.reader(csv_file)
    id_count = 1
    destination_data = []
    #This loops through all the lines in the csv file and makes a list for each row
    for line in csv_reader:
        cur_list = []
        #the first number in the cartons list is the ID
        cur_list.append(id_count)
        id_count += 1
        store_num = line[0]
        store_location = line[1]
        store_prov = line[2]
        count = int(0)
        cur_list.extend((store_num, store_location, store_prov, count))
        destination_data.append(cur_list)

print("this is the destination data: " + str(destination_data[2]))

with open('Reason Codes.csv', 'r') as csv_file:
    #This reads the CVS file with the carton data
    csv_reader = csv.reader(csv_file)
    id_count = 1
    reasoncode_data = []
    #This loops through all the lines in the csv file and makes a list for each row
    for line in csv_reader:
        cur_list = []
        #the first number in the cartons list is the ID
        cur_list.append(id_count)
        id_count += 1
        reacode = line[0]
        rea_category = line[1]
        cur_list.extend((reacode, rea_category))
        reasoncode_data.append(cur_list)

print(reasoncode_data[2])

with open('starting location.csv', 'r') as csv_file:
    #This reads the CVS file with the carton data
    csv_reader = csv.reader(csv_file)
    id_count = 1
    dc_data = []
    #This loops through all the lines in the csv file and makes a list for each row
    for line in csv_reader:
        cur_list = []
        #the first number in the cartons list is the ID
        cur_list.append(id_count)
        id_count += 1
        dc_num = line[0]
        dc_city = line[1]
        dc_prov = line[2]
        cur_list.extend((dc_num, dc_city, dc_prov))
        dc_data.append(cur_list)

print(dc_data[0])

' this function will calculate the number of late arrivals'
def latearrivals(delivery_data):
    total = len(delivery_data)
    num_late = 0
    i = 0
    for i in range(0, total):
        num_late += delivery_data[i][5]
    percent_late = round((num_late/total)*100, 2)
    percent_ontime = 100- percent_late
    labels = ['On Time', 'Late']
    sizes = [percent_ontime, percent_late]
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    return print(str(percent_ontime) + "% of deliveries are on time")

#latearrivals(delivery_data)

'this function finds the most common reasons for late deliveries '
#NOT WORKING AND IDK WHY
def reasonlate(delivery_data, reasoncode_data):
    i = 0
    j = 0
    reascodelist = []
    for j in range(0, len(reasoncode_data)):
        reascodelist.append([reasoncode_data[j][1], 0])
        j +=1

    tots = 0
    for i in range(0, len(delivery_data)):
        if delivery_data[i][5] == 1:
            tots +=1
            reason = delivery_data[i][6]
            for j in range(0, len(reasoncode_data)):
                if reason == reasoncode_data[j][1]:
                    reascodelist[j][1] += 1
        else:
            continue
    print(tots)
    ctc_count = reascodelist[0][1] + reascodelist[1][1] + reascodelist[2][1] + reascodelist[3][1] + reascodelist[4][1] + reascodelist[5][1]
    store_count = reascodelist[6][1] + reascodelist[7][1] + reascodelist[8][1]
    carrier_count = reascodelist[9][1] + reascodelist[10][1] + reascodelist[11][1] + reascodelist[12][1] + reascodelist[13][1] + reascodelist[14][1] + reascodelist[15][1] + reascodelist[16][1] + reascodelist[17][1] + reascodelist[19][1]
    rail_count = reascodelist[18][1]
    prev_carrier_count = reascodelist[20][1]
    yeet = ctc_count + store_count + carrier_count + rail_count + prev_carrier_count
    print(yeet)
    objects = ('CTC', 'Store', 'Carrier', 'Rail', 'Previous Carrier')
    y_pos = np.arange(len(objects))
    performance = [ctc_count, store_count, carrier_count, rail_count, prev_carrier_count]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.ylim([0, 5000])
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Incidents')
    plt.xlabel('Delay Category')
    plt.title("Late Deliveries by Reason Category")
    plt.show()
    return reascodelist
#reasonlate(delivery_data, reasoncode_data)

'The following function returns reason codes for w0# '
def reaslatecatbrampt(delivery_data, reasoncode_data):
    i = 0
    j = 0
    reascodelist = []
    for j in range(0, len(reasoncode_data)):
        reascodelist.append([reasoncode_data[j][1], 0])
        j +=1

    j = 0
    for i in range(0, len(delivery_data)):
        if delivery_data[i][1] == 'W04' and delivery_data[i][5] == 1:
                reason = delivery_data[i][6]
                for j in range(0, len(reasoncode_data)):
                    if reason == reasoncode_data[j][1]:
                        reascodelist[j][1] += 1
        else:
            continue
    list_sorted = sorted(reascodelist, key=itemgetter(1), reverse=True)
    objects = (list_sorted[0][0], list_sorted[1][0], list_sorted[2][0], list_sorted[3][0], list_sorted[4][0], list_sorted[5][0])
    y_pos = np.arange(len(objects))
    performance = [list_sorted[0][1], list_sorted[1][1], list_sorted[2][1], list_sorted[3][1], list_sorted[4][1], list_sorted[5][1]]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    #plt.ylim([0, 000])
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Incidents')
    plt.xlabel('Reason Type')
    plt.title("Top 6 Reason Types for Late Deliveries Bolton W04")
    plt.show()
    return

reaslatecatbrampt(delivery_data, reasoncode_data)


'THis function will graph the CTC Reason Codes '
def reslatectc(reascodelist):
    i = 0
    objects = ('CTC RELATED', 'CTC MECHANICAL', 'DELIVERY CONFLICT', 'SHIPMENT OVERWEIGHT', 'PLANNING RELATED', 'DC RELATED')
    y_pos = np.arange(len(objects))
    performance = [reascodelist[0][1], reascodelist[1][1], reascodelist[2][1], reascodelist[3][1], reascodelist[4][1], reascodelist[5][1]]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.ylim([0, 1250])
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Incidents')
    plt.xlabel('Reason Category')
    plt.title("Late Deliveries by Reason Category CTC ")
    plt.show()
    return

#reslatectc(reasonlate(delivery_data, reasoncode_data))


'THis function will find the stores with the most late deliveries '
def latedeliveries(delivery_data, destination_data):
    i = 0
    j = 0
    total = len(delivery_data)
    stores_total = len(destination_data)
    for i in range(0, total):
        if delivery_data[i][5] == 1:
            store = delivery_data[i][2]
            for j in range(0, stores_total):
                if store == destination_data[j][1]:
                    destination_data[j][4] += 1
                    j += 1
                    break
        else:
            continue
    top_ten = sorted(destination_data, key=itemgetter(4), reverse=True)
    objects = (top_ten[0][2], top_ten[1][2], top_ten[2][2], top_ten[3][2], top_ten[4][2], top_ten[5][2])
    y_pos = np.arange(len(objects))
    performance = [top_ten[0][4], top_ten[1][4], top_ten[2][4], top_ten[3][4], top_ten[4][4], top_ten[5][4]]
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Number of Late Deliveries')
    plt.ylabel('Store City')
    plt.title('Top 5 Late Deliveries by City')
    plt.show()
    return top_ten[0:]

#latedeliveries(delivery_data, destination_data)

'This function finds the number of stores per province'
def findnumstores(storedata):
    prov_list1 = [['YT', 0], ['SK', 0], ['PE', 0], ['QC', 0], ['ON', 0], ['NT', 0], ['NS', 0], ['NL', 0], ['NB', 0], ['MB', 0], ['BC', 0], ['AB', 0]]
    k = 0
    i = 0
    for k in range(0, len(storedata)):
            provin = storedata[k][3]
            for i in range(0, len(prov_list1)):
                if provin == prov_list1[i][0]:
                    prov_list1[i][1] += 1
                    i += 1
                    break
            else:
                continue
    return print("This list is the number of stores per province" + str(prov_list1))

#findnumstores(destination_data)

'This function will find the number of late deliveries per province '
def lateprov(top_ten):
    prov_list = [['YT', 0], ['SK', 0], ['PE', 0], ['QC', 0], ['ON', 0], ['NT', 0], ['NS', 0], ['NL', 0], ['NB', 0], ['MB', 0], ['BC', 0], ['AB', 0]]
    k = 0
    i = 0
    for k in range(0, len(top_ten)):
        if top_ten[k][4] >= 1:
            provin = top_ten[k][3]
            for i in range(0, len(prov_list)):
                if provin == prov_list[i][0]:
                    prov_list[i][1] += 1
                    i += 1
                    break
            else:
                continue
    sortlist = sorted(prov_list, key=itemgetter(1), reverse=True)
    objects = (sortlist[0][0], sortlist[1][0], sortlist[2][0], sortlist[3][0], sortlist[4][0], sortlist[5][0], sortlist[6][0], sortlist[7][0], sortlist[8][0], sortlist[9][0])
    y_pos = np.arange(len(objects))
    performance = [sortlist[0][1], sortlist[1][1], sortlist[2][1], sortlist[3][1], sortlist[4][1], sortlist[5][1], sortlist[6][1], sortlist[7][1], sortlist[8][1], sortlist[9][1]]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Province')
    plt.ylabel('Number of Late Deliveries')
    plt.title('Number of Late Deliveries by Province')
    plt.show()
    print("late by province:  " + str(prov_list))
    return prov_list

#lateprov(latedeliveries(delivery_data, destination_data))

'This function finds the number of deliveries per province '
def delivbyprov(delivery_data, destination_data):
    prov_list = [['YT', 0], ['SK', 0], ['PE', 0], ['QC', 0], ['ON', 0], ['NT', 0], ['NS', 0], ['NL', 0], ['NB', 0], ['MB', 0], ['BC', 0], ['AB', 0]]
    i = 0
    j = 0
    k = 0
    for i in range(0, len(delivery_data)):
        storecode = delivery_data[i][2]
        for j in range(0, len(destination_data)):
            if storecode == destination_data[j][1]:
                cur_prov = destination_data[j][3]
                for k in range(0, len(prov_list)):
                    if cur_prov == prov_list[k][0]:
                        prov_list[k][1] += 1
                        k += 1
                        continue
                j+=1
                continue
            else:
                continue
    totallll = (prov_list[0][1] + prov_list[1][1] + prov_list[2][1] + prov_list[3][1] + prov_list[4][1] + prov_list[5][1] + prov_list[6][1] + prov_list[7][1] + prov_list[8][1] + prov_list[9][1] + prov_list[10][1]+ prov_list[11][1])
    print(totallll)
    print(prov_list)
    return prov_list

#delivbyprov(delivery_data, destination_data)

'this function finds the percentage of late deliveries per province '
def percentlateprov(prov_list_late, prov_list_total):
    i = 0
    percentlate = []
    for i in range(0, len(prov_list_late)):
        per = round((prov_list_late[i][1] / prov_list_total[i][1]) * 100, 2)
        percentlate.append([prov_list_late[i][0], per])
    objects = (percentlate[0][0], percentlate[1][0], percentlate[2][0], percentlate[3][0], percentlate[4][0], percentlate[5][0], percentlate[6][0], percentlate[7][0], percentlate[8][0], percentlate[9][0], percentlate[10][0])
    y_pos = np.arange(len(objects))
    performance = [percentlate[0][1], percentlate[1][1], percentlate[2][1], percentlate[3][1], percentlate[4][1], percentlate[5][1], percentlate[6][1], percentlate[7][1], percentlate[8][1], percentlate[9][1], percentlate[10][1]]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Province')
    plt.ylabel('Percent of Late Deliveries')
    plt.title('Percent Late Deliveries by Province')
    plt.show()
    return percentlate

#percentlateprov(lateprov(latedeliveries(delivery_data, destination_data)), delivbyprov(delivery_data, destination_data))

'This function counts the number of late deliveries, organized by starting location'
def latestart(delivery_data, dc_data):
    i = 0
    dclist = []
    for i in range(0, len(dc_data)):
        dclist.append([dc_data[i][0], 0])
        i +=1
    i = 0
    j = 0
    for i in range(0, len(delivery_data)):
        if delivery_data[i][5] == 1:
            startlocal = delivery_data[i][1]
            for j in range(0, len(dc_data)):
                if startlocal == dc_data[j][1]:
                    dclist[j][1] += 1
                    j += 1
            i += 1
    objects = (
    dc_data[0][1]+dc_data[0][2], dc_data[1][1]+dc_data[1][2], dc_data[2][1]+dc_data[2][2], dc_data[3][1]+dc_data[3][2], dc_data[4][1]+dc_data[4][2])
    y_pos = np.arange(len(objects))
    performance = [dclist[0][1], dclist[1][1], dclist[2][1], dclist[3][1], dclist[4][1]]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Starting Location')
    plt.ylabel('Number of Late Deliveries')
    plt.title('Number of late deliveries by Starting Location')
    plt.ylim([0, 4000])
    plt.show()
    return dclist

#latestart(delivery_data, dc_data)
def latestartpercentage(delivery_data, dc_data, dclist):
    i = 0
    j = 0
    dclisttot = []
    percentlist = []
    for i in range(0, len(dc_data)):
        dclisttot.append([dc_data[i][0], 0])
        i +=1
    i = 0
    for i in range(0, len(delivery_data)):
        startlocal = delivery_data[i][1]
        for j in range(0, len(dc_data)):
            if startlocal == dc_data[j][1]:
                dclisttot[j][1] += 1
                j += 1
        i += 1

    i = 0
    for i in range(0, len(dclist)):
        per = round((dclist[i][1] / dclisttot[i][1]) * 100, 2)
        percentlist.append([dclist[i][0], per])
        i +=1
    objects = (
        dc_data[0][1] + dc_data[0][2], dc_data[1][1] + dc_data[1][2], dc_data[2][1] + dc_data[2][2],
        dc_data[3][1] + dc_data[3][2], dc_data[4][1] + dc_data[4][2])
    y_pos = np.arange(len(objects))
    performance = [percentlist[0][1], percentlist[1][1], percentlist[2][1], percentlist[3][1], percentlist[4][1]]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Starting Location')
    plt.ylabel('Percent Late Deliveries')
    plt.title('Percent Late Deliveries by Starting Location')
    plt.ylim([0, 40])
    plt.show()
    return print(percentlist)


#latestartpercentage(delivery_data, dc_data, latestart(delivery_data, dc_data))

