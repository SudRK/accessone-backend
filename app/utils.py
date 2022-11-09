def addZerosToDate(timestr):
    if len(timestr) == 1:
        return "0" + timestr
    return timestr


def getTime(timestr):
    if int(timestr.split(":")[0]) > 12 :
        return addZerosToDate(str(int((timestr.split(":")[0])) % 12)) + ":" + addZerosToDate(timestr.split(":")[1]) + " PM"
    elif timestr.split(":")[0] == "12":
        return timestr + " PM"
    else:
        if timestr.split(":")[0] == "00":
            timestr = "12:" + timestr.split(":")[1]
        return timestr + " AM"
            

def splitat(str):
    split_strings = ''
    list_str = []
    if len(str) <= 30:
        return str
    split_strings = split_strings + str[0:30] + "\n"
    list_str.append(split_strings)
    for index in range(0, len(str[30:]), 50):
        split_strings = split_strings + str[30:][index : index + 50] + "\n"
    return split_strings
    
