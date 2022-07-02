from modules import Player, db
import re, os, random
import discord
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
            statement = "You have received {} RP from {}. Your new total is {}".format(amount, donor.name, recipient.currentRP)
            await messageUser(recipient_user_obj, statement)
        except Exception as e:
            print(e)
            user = getUser(message.author.id, client)
            statement = user.mention + "This transaction could not be processed. You have insufficient funds."
            await sendMessage(message, statement, "❌")
        print(vars(recipient))
        print(vars(donor))


        
    # if "Helper" not in mentions:
    #     return
    # bot = botUtils.Bot()

    # permissions = checkPermissions(message, client)

    # if message.mentions[0].nick == "Helper":
        # await message.channel.send(message.content)


    # if "avail!" in message.content:
    #     msg = bot.getAvailability(message)
    #     await message.channel.send(msg)
    
    # if "prnt!" in message.content:
    #     if not permissions:
    #         await reject(message,client)
    #         return
    #     msg = bot.printSessions(message)
    #     await message.channel.send(msg)
    
    # if "create!" in message.content:
    #     if not permissions:
    #         await reject(message,client)
    #         return
    #     msg = bot.createSession(message)
    #     if msg == True:
    #         await message.add_reaction("☑")
    #     else:
    #         await message.add_reaction("❌")
    #         await message.channel.send(msg)
    
    # if "add!" in message.content:
    #     name = getName(message)
    #     msg = bot.addUser(message,name)
    #     user = getUser(message, client)

    #     await addReact(message, client,msg,user)

    # if "addmem!" in message.content and "oaddmem!" not in message.content:
    #     if not permissions:
    #         await reject(message,client)
    #         return
    #     contactobj = contactUtils.getContacts()
    #     tempMessage = re.sub(".*addmem! ","", message.content)
    #     messageArray = [x.strip() for x in tempMessage.split(",")]
    #     name = messageArray[0]
    #     userhandle = contactobj[name][1]
    #     user = getUser(message, client)
    #     del messageArray[0]
    #     msg = bot.addUser(message,name, True)
    #     await addReact(message, client,msg,user)

    # if "oaddmem!" in message.content:
    #     if not permissions:
    #         await reject(message,client)
    #         return
    #     contactobj = contactUtils.getContacts()
    #     tempMessage = re.sub(".*addmem! ","", message.content)
    #     messageArray = [x.strip() for x in tempMessage.split(",")]
    #     name = messageArray[0]
    #     userhandle = contactobj[name][1]
    #     user = getUser(message, client)
    #     del messageArray[0]
    #     msg = bot.addUser(message,name, True, True)
    #     await addReact(message, client,msg,user)

    # if "remove!" in message.content:
    #     name = getName(message)
    #     msg = bot.removeUser(message,name)
    #     user = getUser(message, client)
    #     await removeReact(message,client,msg, user)

    # if "removemem!" in message.content:
    #     if not permissions:
    #         await reject(message,client)
    #         return
    #     contactobj = contactUtils.getContacts()
    #     tempMessage = re.sub(".*removemem! ","", message.content)
    #     messageArray = [x.strip() for x in tempMessage.split(",")]
    #     name = messageArray[0]
    #     userhandle = contactobj[name][1]
    #     user = getUser(message, client)
    #     del messageArray[0]
    #     msg = bot.removeUser(message,name, True)
    #     await removeReact(message,client,msg, user)

    # if "whereami?" in message.content:
    #     name = getName(message)
    #     msg = bot.getSessionsByUser(message, name)
    #     await message.author.send(msg)

    # if "gif!" in message.content:
    #     channel = client.get_channel(508443041476902912)    
    #     await channel.send(file=discord.File("assets/worry.gif"))

    # del bot
