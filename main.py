from typing import Final
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import weather

#load token
load_dotenv()
TOKEN: Final[str]= os.getenv('DISCORD_TOKEN')

#BOT SETUP
intents = discord.Intents.default()
intents.message_content = True #NOQA
bot= commands.Bot(command_prefix="pythia",intents=intents)
#client.remove_command("help")

#Commands 


@bot.tree.command(name="temperatur")
async def temperatur(interaction: discord.Interaction):
    temp=weather.getweather()
    await interaction.response.send_message(f"Hallo {interaction.user.mention}! Die max und min Temperaturen in Mosbach für die nächste Woche lauten: {temp} ")

@bot.event
async def on_ready():
    print(f'{bot.user} is now purring!')
    try:
        synced =await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

 

#main entry point
def main()-> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()