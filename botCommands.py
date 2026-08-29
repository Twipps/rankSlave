import valorantFunction

# known bugs: Commands can be called even during a command cycle
#           : Account mismatch checking doesn't work, discord will sometimes read it own

# For processing any commands
async def commandsList (interaction):
    print("commands | [ Displaying Command List ]")
    await interaction.response.send_message("```cs\n# Commands:\n\n# /addAccount: Adds and assigns a Valorant account to the user."
                               + " (A user can only have one account assigned)\n"
                               + "# /deleteAccount: Removes and unassigns the user's Valorant account."
                               + " (A user can only remove their own account)\n" 
                               + "# /updateRole: Updates the Valorant rank role of the discord user.\n"
                               + "# /updateAll: Forces the Valorant rank role of every user in the server to be updated."
                               + " (Runs on a clock otherwise)\n"
                               + "# /currentRoles: Generates a list showing the current accounts and there roles.\n"
                               + "# /commands: Well you just used this one didn't you?\n```")
    
async def addAccount(client, interaction):
    # after the first interaction response you need to have another type of reference
    # for sending, so im using the reply object here
    await interaction.response.send_message("```cs\n# Please enter a Valorant account (Name #ID):```")
    print("add_account | Awaiting User Response: [ From Guild: \"" + str(interaction.guild.id) 
          + "\" Channel: \"" + str(interaction.channel.id) +  "\" ]")

    # should prevent the bot from reading itself for checking 
    # and should prevent clashing from multiple channels/servers
    # this was originally gonna be for one server, this is just patch work
    # I would probably handle multiple server processes differently in this scenario
    reply = None
    while (reply == None or str(reply.author.id) == "1132010219661185054" or str(reply.channel.id) != str(interaction.channel.id)):
        reply = await client.wait_for('message')

    print("add_account | Recieved User Response: [ From Guild: \"" + str(interaction.guild.id) 
          + "\" Channel: \"" + str(interaction.channel.id) +  "\" ]")
  
    # make sure to include server checking here
    if (interaction.user.id == reply.author.id):   
         await reply.channel.send("```cs\n# Verifying account...```")

         # not the best to use an array here but im lazy [0] is the verified bool,
         # [1] is the account URL, [2] is the current rank of the account
         # I just dont want to ping the web server more then once per add
         verifiedAccount = valorantFunction.accountVerify(reply.content)
         if (verifiedAccount[0] == True):
              await reply.channel.send("```diff\n! Verified, adding account... !```")
              print("add_account | [ Account Verified ]")
              valorantFunction.addAccount(interaction.guild.id, interaction.user.id, verifiedAccount)
         else:
              await reply.channel.send("```diff\n- Verification failed, account not found -```")
              print("add_account | [ Account Verification Failed ]")
    else:
        await reply.channel.send("```diff\n- User mismatch, only one user per command call -```")
        print("add_account | [ User Mismatch ]")