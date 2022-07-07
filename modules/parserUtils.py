from modules import Player, db, Transaction, formatUtils
import re, os, random
import discord
import time
from importlib import reload

database = db.db()
locked = False
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


        
async def parseMessage(message, client):
    global locked
    # print(message)
    
# we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if not message.content.startswith("!please"):
        return


    if "give" in message.content:
        if locked:
            statement = "This action is currently locked. You must wait for the GMs to unlock it."
            await sendMessage(message, statement, "❌")
            return
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
            
            donor = getUserFromDB(message.author.id)
            donor.subtract(amount)
            time.sleep(2)
            recipient = getUserFromDB(recipient_id)
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
            amount = -(abs(int(messageArray.pop())))
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


    if "howmuch" in message.content:
        #Query for a player's RP count
        player = getUserFromDB(message.author.id)
        user = getUser(message.author.id, client)
        statement = "Your currently have {} RP.".format(player.currentRP)
        await messageUser(user, statement)
    # if "drop" in message.content:
    #     database.dropTable()
    
    if "make" in message.content:
        #Command to put all players in database
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            for member in client.get_all_members():
                isPlayer = checkPlayer(member.roles)
                if isPlayer:
                    player = getUserFromDB(member.id,member)
            statement = "All Players have been added to database"
            await sendMessage(message, statement, "☑")
                

    if "add4" in message.content:
        #Adds 4 RP to each player's account
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            for member in client.get_all_members():
                isPlayer = checkPlayer(member.roles)
                if isPlayer:
                    player = getUserFromDB(member.id,member)
                    player.add(4)
                    time.sleep(1)   
            statement = "All current players have had their RP increased by 4"
            await sendMessage(message, statement, "☑")

    if "lock" in message.content and "unlock" not in message.content:
        #Locks the 'give' command and prevents it from being used.
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            locked = True
            statement = "RP Transactions between players is currently locked."
            await sendMessage(message, statement, "☑")
    if "unlock" in message.content:
        #unlocks the 'give' command and allows it to be used.
        isAdmin = checkAdmin(message.author.roles)
        if isAdmin:
            statement = "RP Transactions between players is currently unlocked."
            await sendMessage(message, statement, "☑")
            locked = False

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

    

        
