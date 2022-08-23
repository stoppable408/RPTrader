from datetime import datetime

def formatTransactions(transactionList):
    block = "```"
    spacing = 2
    string_array = []
    #getting column lengths
    id_column_length = max([len(x[0]) for x in transactionList]) + spacing

    name_column_length = max([len(x[1]) for x in transactionList]) + spacing
    name_column_length = name_column_length if name_column_length > 8 else 8

    amount_column_length = max([len(str(x[2])) for x in transactionList]) + spacing
    amount_column_length = amount_column_length if amount_column_length > 8 else 8

    status_column_length = max([len(x[3]) for x in transactionList]) + spacing
    status_column_length = status_column_length if status_column_length > 8 else 8


    date_column_length = max([len(formatDate(x[4])) for x in transactionList]) + spacing

    def getHeader():
        headerString = block + "\n"\
            + "+" + "-"*id_column_length\
            + "+" + "-"*name_column_length\
            + "+" + "-"*amount_column_length\
            + "+" + "-"*status_column_length\
            + "+" + "-"*date_column_length\
            + "+" + "\n"
        
        headerString += "|" + (" id " + " "*(id_column_length-4)) \
            +  "|" + (" player " + " "*(name_column_length-8))\
            +  "|" + (" amount " + " "*(amount_column_length-8))\
            +  "|" + (" status " + " "*(status_column_length-8))\
            +  "|" + (" date " + " "*(date_column_length-6))\
            +  "|" + "\n"

        headerString += "+" + "-"*id_column_length\
            + "+" + "-"*name_column_length\
            + "+" + "-"*amount_column_length\
            + "+" + "-"*status_column_length\
            + "+" + "-"*date_column_length\
            + "+" + "\n"
        return headerString

    def getFooter():
        footerString = "+" + "-"*id_column_length\
            + "+" + "-"*name_column_length\
            + "+" + "-"*amount_column_length\
            + "+" + "-"*status_column_length\
            + "+" + "-"*date_column_length\
            + "+" + "\n"
        footerString += block

        return footerString



    #Transaction data
    string = getHeader()
    for transaction in transactionList:
        transaction_id = transaction[0]
        player_name = transaction[1]
        amount = str((transaction[2]))
        status = transaction[3]
        date = formatDate(transaction[4])

        new_string = "| " + transaction_id\
               + " | " + player_name + " "*(name_column_length - (len(player_name) + spacing))\
               + " | " + amount + " "*(amount_column_length - (len(amount) + spacing))\
               + " | " + status +  " "*(status_column_length - (len(status) + spacing))\
               + " | " + date +  " "*(date_column_length - (len(date) + spacing))\
               + " | " + "\n"
        if (len(string) + len(new_string)) > (2000 - len(getFooter())):
            string += getFooter()
            string_array.append(string)
            string = getHeader()
        string += new_string

    string += getFooter()
    string_array.append(string)

    return string_array

def formatDate(datetime):
    return datetime.strftime("%m/%d/%Y, %H:%M:%S")

def formatUsers(userList):
    block = "```"
    spacing = 2
    string_array = []
    #getting column lengths
    name_column_length = max([len(x[0]) for x in userList]) + spacing
    name_column_length = name_column_length if name_column_length > 8 else 8

    amount_column_length = max([len(str(x[1])) for x in userList]) + spacing
    amount_column_length = amount_column_length if amount_column_length > 8 else 8


    def getHeader():
        headerString = block + "\n"\
            + "+" + "-"*name_column_length\
            + "+" + "-"*amount_column_length\
            + "+" + "\n"
        
        headerString += "|" + (" player " + " "*(name_column_length-8))\
            +  "|" + (" amount " + " "*(amount_column_length-8))\
            +  "|" + "\n"

        headerString += "+" + "-"*name_column_length\
            + "+" + "-"*amount_column_length\
            + "+" + "\n"
        return headerString

    def getFooter():
        footerString = "+" + "-"*name_column_length\
            + "+" + "-"*amount_column_length\
            + "+" + "\n"
        footerString += block

        return footerString


    #User data
    string = getHeader()
    for player in userList:
        player_name = player[0]
        amount = str(player[1])

        new_string = "| " + player_name + " "*(name_column_length - (len(player_name) + spacing))\
               + " | " + amount + " "*(amount_column_length - (len(amount) + spacing))\
               + " | " + "\n"
        if (len(string) + len(new_string)) > (2000 - len(getFooter())):
            string += getFooter()
            string_array.append(string)
            string = getHeader()
        string += new_string

    string += getFooter()
    string_array.append(string)

    return string_array