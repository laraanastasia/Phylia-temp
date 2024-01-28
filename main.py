from typing import Final
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import weather
from pandas import DatetimeIndex


#load token
load_dotenv()
TOKEN: Final[str]= os.getenv('DISCORD_TOKEN')

#BOT SETUP
intents = discord.Intents.default()
intents.message_content = True #NOQA
bot= commands.Bot(command_prefix="pythia",intents=intents)
#client.remove_command("help")

#Commands 


@bot.tree.command(name="temperatur", description="What is the weather forcast?")
@app_commands.describe(plz="What is the postcode of your town?")
async def temperatur(interaction: discord.Interaction,plz: str):
    print(f"User: {interaction.user.name}, Plz: {plz}, Guild: {interaction.guild}, Channel: {interaction.channel}")
    x=weather.feature(plz)
    #dataraw=weather.getcordinats(plz)
    #data=weather.getweather(dataraw[1],dataraw[2])
    await interaction.response.send_message (f'Postalcode: {plz}', ephemeral=True)
    #date_ls= data["date"].tolist()
    #max_ls=data["maximum"].tolist()
    #min_ls=data["minimum"].tolist()
        # Create an embed
    #embed = discord.Embed(title="7-Day Weather Forecast", color=0xD9A4FC)  # You can change the color as per your preference

    # Add fields to the embed
    #for i in range(len(date_ls)):
    #    embed.add_field(name=date_ls[i], value=f"Min: {min_ls[i]}°C\nMax: {max_ls[i]}°C", inline=True)

    # Send the embed to the Discord channe
    await interaction.channel.send(embed=x)
    
    

@bot.event
async def on_ready():
    print(f'{bot.user} is now ready!')
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