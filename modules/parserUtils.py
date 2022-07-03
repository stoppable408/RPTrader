from modules import Player, db, Transaction, formatUtils
import re, os, random
import discord
import time
from importlib import reload

database = db.db()
def checkAdmin(roles):
    for role in roles:
        if str(role) == "Gamemaster":
            return True
    return False

def checkPlayer(roles):
    for role in roles:
        if (str(role) == "King") or (str(role) == "Count") or (str(role) == "Baron"):
            return True
    return False

def getUserFromDB(member_id, member=None):
    playerList = database.getUserByID(member_id)
    if not playerList:
        print("Player does not exist in database. Initialized Database Entry for {}".format(member.name))
        database.insertNewUser(member)
    player = Player.Player(database.getUserByID(member_id)[0])
    return player

def getTransactionFromDB(transaction_id):
    db_transaction = database.getTransaction(transaction_id)[0]
    player_id = db_transaction[1]
    amount = db_transaction[2]
    status = db_transaction[3]
    created_on = db_transaction[4]
    transaction_id = db_transaction[0]
    transaction = Transaction.Transaction(player_id, amount, status, created_on, transaction_id)
    return transaction


def getUser(user_id, client):
    return client.get_user(user_id)
    
async def sendMessage(message, statement, reaction=None):
    if reaction:
        await message.add_reaction(reaction)
    await message.channel.send(statement)

async def messageUser(user, statement):
    await user.send(statement)


# def getName(message):
#     name = message.author.name
#     discriminator = message.author.discriminator
#     return name + "#" + discriminator

# def getUsers(emailList, client):
#     allUsers = client.users
#     contacts = contactUtils.getContacts()
#     userList = []
#     finalUserList = []
#     for email in emailList:
#         for contact in contacts:
#             if email == contacts[contact][0]:
#                 userList.append(contacts[contact][1])
#     for user in userList:
#         for users in allUsers:
#             name = users.name + "#" + users.discriminator
#             if user == name:
#                 finalUserList.append(users)
#     return finalUserList
    


# def checkPermissions(message, client):
#     if "Palpatine" not in message.author.name and "Alamander" not in message.author.name:
#         return False
#     else:
#         return True

# async def reject(message, client):
#         await message.add_reaction("🇳")
#         await message.add_reaction("🇴")
#         await message.add_reaction("🅿")
#         await message.add_reaction("🇪")

# async def addReact(message, client, msg, user):
#         if msg[0] == True and msg[1] != "":
#             statement = user.mention + " You have been added to the waitlist for this session, because you are in the " + msg[1]
#             await message.add_reaction("✔")
#             await message.channel.send(statement)
#         elif msg[0] == True and msg[1] == "":
#             await message.add_reaction("☑")
#         elif msg[0] == False  and msg[1] == "Full":
#             statement = user.mention + " The mission you're trying to join is full"
#             await message.add_reaction("❌")
#             await message.channel.send(statement)
#         elif msg[0] == False and msg[1] == "Double":
#             statement = user.mention + " You're already in this mission. You cannot join twice"
#             await message.add_reaction("❌")
#             await message.channel.send(statement)
#         elif msg[0] == False and msg[1] == "Invalid":
#             await message.add_reaction("❌")
#             statement = user.mention + " You did not use the correct format. Please make the format fit the following: \n\r \"Helper add! (insert name/race/class, session date (in M\D format), region)\""
#             await message.channel.send(statement)    
#         elif msg[0] == False and msg[1] == "Missing":
#             await message.add_reaction("❌")
#             statement = user.mention + " There is no session scheduled for the date and region you mentioned."
#             await message.channel.send(statement)  
#         elif msg[0] == False and msg[1] == "No Level in Description":
#             await message.add_reaction("❌")
#             statement = user.mention + " You did not include your character's level in the description. Please resubmit your request with a proper level"
#             await message.channel.send(statement)      
#         elif msg[0] == False and isinstance(msg[1],list):
#             await message.add_reaction("❌")
#             Lennon = client.get_user(399383747746725899)
#             userList = getUsers(msg[1], client)
#             statement = user.mention + " Your character is out of tier. Please gather consent from the following members: \n\n"
#             for person in userList:
#                 statement += person.mention + "\n"
#             statement += "\n and then message " + Lennon.mention + " and he will add you later"
#             await message.channel.send(statement)    
            
# async def removeReact(message, client, msg, user):
#         if msg[0] == False and msg[1] == "Invalid":
#             await message.add_reaction("❌")
#             statement = user.mention + " You did not use the correct format. Please review the correct format and try again. "
#             await message.channel.send(statement)    
#         if msg[0] == False and msg[1] == "Empty":
#             await message.add_reaction("❌")
#             statement = user.mention + " You are not in this mission. You cannot leave a mission you aren't in."
#             await message.channel.send(statement)      
#         if msg[0] == True:
#             date = msg[1][0]
#             region = msg[1][1]
#             await message.add_reaction("☑")      
#             statement = user.mention + " You have been removed from the {region} session scheduled for {date}".format(region=region,date=date)
#             await message.channel.send(statement)   
        
async def parseMessage(message, client):
    # print(message)
    
# we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if not message.content.startswith("!please"):
        return

    if "drop" in message.content:
        database.dropTable()
    
    if "make" in message.content:
        for member in client.get_all_members():
            isPlayer = checkPlayer(member.roles)
            if isPlayer:
                player = getUserFromDB(member.id,member)
                print(member.name, member.id)
            

    if len(message.mentions):
        if "add" in message.content or "subtract" in message.content:
            isAdmin = checkAdmin(message.author.roles)
            if isAdmin:
                print("----------------------")
                messageArray = message.content.split(" ")
                mention = messageArray.pop()
                try:
                    number = int(messageArray.pop())
                except Exception as e:
                    user = getUser(message.author.id, client)
                    statement = user.mention + " You did not use the proper format. Please use the following format: \n\n !please add <amount> <user>"
                    await sendMessage(message, statement, "❌")
                    return
                action = messageArray.pop()
                try:
                    player = getUserFromDB(message.mentions[0].id)
                    if action == 'subtract':
                        player.subtract(number)
                        term = "removed from"
                    else:
                        player.add(number)
                        term = "added for"
                    statement = "RP successfully {} {}. New RP total: {}".format(term, player.name, player.currentRP)
                    await sendMessage(message, statement, "☑")
                except Exception as e:
                    user = getUser(message.author.id, client)
                    statement = user.mention + " I've encountered an Error. details: {}".format(e)
                    await sendMessage(message, statement, "❌")
                    return

    if "give" in message.content:
        messageArray = message.content.split(" ")
        try:
            recipient_id = int(re.sub("<|@|>","", messageArray.pop()))
            amount = int(messageArray.pop())
        except:
            user = getUser(message.author.id, client)
            statement = user.mention + " You did not use the proper format. Please use the following format: \n\n !please give <amount> <user>"
            await sendMessage(message, statement, "❌")
            return  
        try:
            recipient = getUserFromDB(recipient_id)
            donor = getUserFromDB(message.author.id)
            donor.subtract(amount)
            recipient.add(amount)

            user = getUser(message.author.id, client)
            statement = "{} RP successfully transferred to {}.".format(amount, recipient.name)
            await sendMessage(message, statement,  "☑")
            recipient_user_obj = getUser(recipient_id, client)
            statement = "\n\nYou have received {} RP from {}. Your new total is {}".format(amount, donor.name, recipient.currentRP)
            await messageUser(recipient_user_obj, statement)
        except Exception as e:
            print(e)
            user = getUser(message.author.id, client)
            statement = user.mention + "This transaction could not be processed. You have insufficient funds."
            await sendMessage(message, statement, "❌")

    if "spend" in message.content:
        messageArray = message.content.split(" ")
        player_id = message.author.id
        status = "Pending"
        user = getUser(player_id, client)
        try:
            amount = -(int(messageArray.pop()))
        except:
            statement = user.mention + " You did not use the proper format. Please use the following format: \n\n !please spend <amount>"
            await sendMessage(message, statement, "❌")
            return  
        current_rp = getUserFromDB(message.author.id).currentRP
        if current_rp < -(amount):
            statement = user.mention + " This transaction could not be processed. You have insufficient funds. \n\nYour current RP total: {}\nYour transaction amount: {}".format(current_rp, -amount)
            await sendMessage(message, statement, "❌")
            return 
        transaction = Transaction.Transaction(player_id, amount, status)
        transaction.addTransaction()
        statement = user.mention + " You have successfully submitted a transaction. The transaction is now pending.\n\
                                     \rPlease wait for the GMs to approve it.\n\nYour transaction ID is: {}".format(transaction.transaction_id)
        await sendMessage(message, statement, "☑")


    if "approveall" in message.content:
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
           transactions = [getTransactionFromDB(x[0]) for x in database.listPendingTransactions()]
           
           for transaction in transactions:
                player = getUserFromDB(transaction.player_id)
                user = getUser(player.player_id, client)

                #Denies the transaction if the player no longer has the appropriate amount of RP to finish it.
                current_rp = player.currentRP
                if current_rp < -(transaction.amount):
                    user = getUser(message.author.id, client)
                    statement = user.mention + " The transaction with ID: {} could not be approved. {} has insufficient funds.\
                                \n\nCurrent RP total for {}: {}\nTransaction amount: {}\
                                \n\nPlease have the player submit another transaction when they have more RP".format(transaction.transaction_id, player.name, player.name, current_rp, -(transaction.amount))
                    await sendMessage(message, statement, "❌")
                    statement = "\n\nYour transaction with ID: {} for amount: {}\
                                \nhas been denied by the GMs. You have {} RP".format(transaction.transaction_id, -(transaction.amount), player.currentRP)
                    await messageUser(user, statement)
                    transaction.status = "Denied"
                    transaction.update()
                    time.sleep(1)
                    continue

                #Approves a transaction if the player has enough RP and the transaction is still pending
                transaction.status = 'Approved'
                player.add(transaction.amount, transaction)
                statement = "This transaction with ID: {} has been Approved. {} has been notified.".format(transaction.transaction_id, player.name)
                await sendMessage(message, statement, "☑")
                statement = "\n\nYour transaction for amount {} has been approved by the GMs. You now have {} RP remaining".format(-(transaction.amount), player.currentRP)
                await messageUser(user, statement)
                time.sleep(2)
                
        return


    if "approve" in message.content:
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            messageArray = message.content.split(" ")
            transaction_id = messageArray.pop()
            transaction = getTransactionFromDB(transaction_id)
            #Rejects the approval if you try to approve a non-pending transaction
            if "Pending" not in transaction.status:
                statement = "This transaction's status is {}. You can only approve pending transactions".format(transaction.status)
                await sendMessage(message, statement, "❌")
                return

            player = getUserFromDB(transaction.player_id)

            #Denies the transaction if the player no longer has the appropriate amount of RP to finish it.
            current_rp = player.currentRP
            if current_rp < -(transaction.amount):
                statement = "The transaction could not be approved. {} has insufficient funds. \n\nCurrent RP total for {}: {}\nTransaction amount: {}\n\nPlease have the player submit another transaction when they have more RP".format(player.name, player.name, current_rp, -(transaction.amount))
                await sendMessage(message, statement, "❌")
                transaction.status = "Denied"
                transaction.update()
                return 

            #Approves a transaction if the player has enough RP and the transaction is still pending
            transaction.status = 'Approved'
            player.add(transaction.amount, transaction)
            user = getUser(player.player_id, client)
            statement = "This transaction has been Approved. {} has been notified.".format(player.name)
            await sendMessage(message, statement, "☑")
            statement = "\n\nYour transaction for amount {} has been approved by the GMs. You now have {} RP remaining".format(-(transaction.amount), player.currentRP)
            await messageUser(user, statement)
            return

    if "deny" in message.content:
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            messageArray = message.content.split(" ")
            transaction_id = messageArray.pop()
            transaction = getTransactionFromDB(transaction_id)  

            player = getUserFromDB(transaction.player_id)
            user = getUser(player.player_id, client)

            #Denies the transaction 
            statement = " The transaction with ID: {} has been denied. {} will be informed".format(transaction.transaction_id, player.name)
            await sendMessage(message, statement, "❌")
            statement = "\n\nYour transaction with ID: {} for amount: {}\
                        \nhas been denied by the GMs. You have {} RP".format(transaction.transaction_id, -(transaction.amount), player.currentRP)
            await messageUser(user, statement)
            transaction.status = "Denied"
            transaction.update()
            time.sleep(1)

    if "pending" in message.content:
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            transactions = database.listPendingTransactions()
            if transactions:
                statements = formatUtils.formatTransactions(transactions)
                for statement in statements:
                    await sendMessage(message, statement)
            else:
                statement = "☑ There are no pending transactions ☑"
                await sendMessage(message, statement)
    

    if "history" in message.content:
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            messageArray = message.content.split(" ")
            try:
                player_id = int(re.sub("<|@|>","", messageArray[2]))
                player = getUserFromDB(player_id)
                try:
                    lookback = int(messageArray[3])
                except:
                    lookback = 30
            except:
                user = getUser(message.author.id, client)
                statement = user.mention + " You did not use the proper format. Please use the following format: \n\n !please history <mention_user or user_id> <lookback (optional)>"
                await sendMessage(message, statement, "❌")
                return  
            transactions = database.listUserTransactionHistory(player_id, lookback)
            if transactions:
                statements = formatUtils.formatTransactions(transactions)
                for statement in statements:
                    await sendMessage(message, statement)
            else:
                statement = "{} has no transaction history for this time period".format(player.name)
                await sendMessage(message, statement)

    

        
