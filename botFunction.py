import discord
import botCommands
from discord import app_commands

# reminder to create a database per server connection.

def runDiscordBot():
    # operations to connect to discord's bot gateway
    TOKEN="BOT_TOKEN_HERE"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client) # assigns a command tree object
    
    # this is cool as shit, for this to be dynamic dont fill
    # the guild paramater "guild=discord.Object(1127808438114717817)""
    @tree.command(name="commands", description="Shows the description of every command implemented")
    async def first_command(interaction):
        print("Processing Command: [ \"commands\", For Guild: \"" + str(interaction.guild.id) + "\" ]")
        await botCommands.commandsList(interaction)

    @tree.command(name="add_account", description="Adds a Valorant account for your discord")
    async def first_command(interaction):
        print("Processing Command: [ \"add_account\", For Guild: \"" + str(interaction.guild.id) + "\" ]")
        await botCommands.addAccount(client, interaction)

    @client.event
    async def on_ready():
        # dynamic syncing
        await tree.sync()
        print(str(client.user) + " is now running")

    @client.event
    async def on_message(message):
        if message.author != client.user:
            print("Message Recieved: [ User: " + str(message.author) + "  ID: " 
                  + str(message.author.id) + "  Channel: " + str(message.channel.id) + "  Guild: " 
                  + str(message.guild.id) + "  Message: \"" + str(message.content) + "\" ]")

    client.run(TOKEN)
