from typing import Final
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import weather
import xlwings as xw
import Karten


load_dotenv()
TOKEN: Final[str]= os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True #NOQA
bot= commands.Bot(command_prefix="pythia",intents=intents)
#client.remove_command("help")


@bot.tree.command(name="temperatur", description="What is the weather forcast?")
@app_commands.describe(plz="What is the postcode of your town?")
async def temperatur(interaction: discord.Interaction,plz: str):
    print(f"User: {interaction.user.name}, Plz: {plz}, Guild: {interaction.guild}, Channel: {interaction.channel}")
    x=weather.feature(plz)
    await interaction.response.send_message (f'Postalcode: {plz}', ephemeral=True)
    await interaction.channel.send(embed=x)
    
@bot.tree.command(name="tarot",description="Whats your destiny?") 
@app_commands.describe(amount="How many cards do you want to pull?")
async def tarot(interaction: discord.Interaction,amount:int):
    x= Karten.feature(amount)
    await interaction.response.send_message (f'You pulled {amount} cards ', ephemeral=True)
    await interaction.channel.send(embed=x)

@bot.tree.command(name="tarot_with_cards",description="Whats your destiny (pictured)?") 
@app_commands.describe(amount="Pull between 1 and 3 cards")
async def tarot_with_cards(interaction: discord.Interaction,amount:int):
    if amount==1:
        await interaction.response.send_message (f'You pulled {amount} card ', ephemeral=True)
        x= Karten.featureone(amount)
        await interaction.channel.send(embeds=x)
    elif amount==2:
        await interaction.response.send_message (f'You pulled {amount} cards ', ephemeral=True)
        x= Karten.featuretwo(amount)
        await interaction.channel.send(embeds=x)
    elif amount==3:
        await interaction.response.send_message (f'You pulled {amount} cards ', ephemeral=True)
        x= Karten.featurethree(amount)
        await interaction.channel.send(embeds=x)
    else:
        await interaction.response.send_message (f'Please choose between 1 and 3 cards', ephemeral=True)
@bot.event
async def on_ready():
    print(f'{bot.user} is now ready!')
    try:
        synced =await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    ws= xw.Book("plzdoc.xlsx").sheets["Sheet1"]
#main entry point
def main()-> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()