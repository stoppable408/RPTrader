
Welcome to RP Bot. A Bot that allows for an automated management of RP for Players in the Game of Banners.



## **GameMaster Only Commands:**
| Command | Description |
| --- | --- |
| `!please make` | Adds all players to the database and sets their RP count to 0. If a player is already in the database, this command will skip that player and their RP count will not be affected. <br/><br/> Once this command has added all players to the database, it will print (in the channel the command was used) "All Players have been added to database"  <br/><br/> Note: "player" is defined as a person with the "Count", "Baron", or "King" role. |
| `!please add4`| Adds 4 RP to all players accounts. <br/><br/> Once this command has completed. It will print (in the channel the command was used) "All current players have had their RP increased by 4" |
| `!please lock` | Locks Player-to-Player transactions <br/><br/> Once this command has run, it will print  (in the channel the command was used) "RP transactions between players is currently locked"  |
| `!please unlock` | Unlocks Player-to-Player transactions <br/><br/> Once this command has run, it will print  (in the channel the command was used) "RP transactions between players is currently unlocked"  |
| `!please approve <transaction ID>`| Will try to approve the individual pending transaction provided to the bot. <br/><br/> If the transaction is not pending, it will send an error saying that the transaction is no longer pending. <br/><br/> If the player no longer has enough RP, it will throw an error that says the player doesn't have enough RP <br/><br/> If there is nothing wrong with the transaction. It will be approved and the player will be sent a private message informing them that it has been approved| 
| `!please approveall` | Approves all pending transactions. <br/><br/> Has the same error handling for the `approve` command. |
| `!please deny <transaction ID>` | Denies the individual pending transaction.  <br/><br/> Once the transaction is denied. The Player will be sent a private message informing them that their transaction was denied. |
| `!please pending`| Prints all pending transactions (in the channel that the message was sent to) | 
| `!please history <mention_user or user_id> <lookback (optional)> `| Prints the player's transaction history with an optional lookback window in days. <br/><br/> This can be called by either mentioning the player (using @player_name) or using the player's Discord ID.  <br/><br/> The lookback window is optional. if no lookback is provided, it will retreive the last 30 days of a user's transaction history | 
| `!please getall`| Prints all players current RP amounts |
| `!please add <number> <mention_user>`| Adds &lt;number&gt; to players RP total|
| `!please subtract <number> <mention_users>`| Subtracts &lt;number&gt; from players RP total|




## **Player Only Commands:**
| Command    | Description |
| --- | --- |
| `!please spend <amount>`| Submits a transaction for &lt;amount&gt; to the GMs for approval. This command will send you a private message confirming that your transaction was sent to the GMs, and it will contain a transaction ID for reference|
| `!please howmuch`| Privately messages the user with how much RP they currently have. |
| `!please getid  <mention_user>`| The bot will privately message the user_id of a player. <br/><br/> The bot will delete the invoking message to preserve anonymity |
| `!please give <amount> <mention_user or user_id>` | Gives &lt;amount&gt; to player. <br/><br/> Will send a message to the receiving user once completed. Only works when trading is unlocked | 


## **Caexan Republic Player Only Commands:**
| Command    | Description |
| --- | --- |
| `!please tax <amount>`| Pays &lt;amount&gt; in taxes. Adds that amount to the treasury. |



**Note:** All these commands will work if you privately message the bot. Allowing you to have anonymity when spending RP or giving RP. 
