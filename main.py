from typing import Final
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import weather
import xlwings as xw
import Karten
import lecturedata
import minigames
from datetime import date, datetime, timedelta
import random
import discord.utils
from discord.ext import commands,tasks
message = int

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

# lecture command for getting todays lecture plan
@bot.tree.command(name="lecture",description="Check the lecture plan!")
async def lecture(interaction: discord.ui.Button):
    global lecturecounter
    lecturecounter = 0
    printing_lecture = lecturedata.lecture_data(date.today())
    global message    
    message = await interaction.response.send_message(embed=printing_lecture, view = lecturedata.embed_buttons())

# roll-a-dice
@bot.tree.command(name="roll-a-dice",description="You have a gambling addiction and love discord? Try both at the same time!")
async def rolladice(interaction:discord.Interaction):
  await interaction.response.send_message(embed=minigames.dice_embed(minigames.roll()))

# password generator with user input
@bot.tree.command(name="generate_password",description="Generate a password with the length of your choice!")
async def generatepassword(interaction: discord.Interaction,length :int):
    member = interaction.user
    try: 
            await member.send(minigames.password(length))
            await interaction.response.send_message(f"Password has been sent to {member.global_name}.", ephemeral=True)
    except:
            await interaction.response.send_message(f"Wished password-length is too long, sorry :(",ephemeral = True)

# counting game
@bot.tree.command(name="start_counting",description="Count up but stay concentrated :)")
async def start_counting(interaction:discord.Interaction):
        global exit2
        exit2 = 0
        # getting channel
        channel_id = interaction.channel.id
        channel = bot.get_channel(channel_id)
        global author
        author = interaction.user
        await interaction.response.send_message("Count up from **1**. *Wrong answers have consequences...*")
        def check(message):
             return message.author and message.channel and message.content.isdigit()
        preNumber = 1
        # checking for next number
        while True:
                user_guess = await bot.wait_for('message', check=check,timeout=None)
                number = int(user_guess.content)
                if user_guess.author != author:
                    if number == preNumber + 1:
                        await user_guess.add_reaction("✅")
                        preNumber = number
                        author = user_guess.author
                    else:
                        await user_guess.add_reaction("❌")
                        preNumber = preNumber - 5
                        await channel.send(f"Uh ohhh, new number is **{preNumber}**. Fix your mistake <@{user_guess.author.id}> 😉")
                        if preNumber <= 0:
                            await channel.send(f"You lost...try again 😭")
                            exit2 = 1
                    if exit2 == 1:
                        break
                else: 
                     await channel.send("Not so greedy! This is a team-game.")
                        

# guess the number game
@bot.tree.command(name="guess_the_number",description="Guess a number between 'start' and 'length'!")
async def guess_the_number(interaction:discord.Interaction,start: int, end:int):
        global exit 
        exit = 0
        channel_id = interaction.channel.id
        channel = bot.get_channel(channel_id)
        randNumber = random.randint(start, end)
        await interaction.response.send_message(f"Guess the number between {start} and {end}!")
        def check(message):
             return message.author and message.channel and message.content.isdigit()
        # checking for next number
        while True:
            try:
                user_guess = await bot.wait_for('message', check=check,timeout=30)
                guess = int(user_guess.content)
                if guess == randNumber:
                    await user_guess.add_reaction("✅")
                    exit = 1
                else:
                    await user_guess.add_reaction("❌")
                if exit == 1:
                    break
            except TimeoutError:
                await channel.send(f"You lose...the number was {randNumber}.")
                break

# printing lecture plan of the next day ever 24 hours
@tasks.loop(hours=24)
async def regular_lecture():
    # Get the current time
    now = datetime.now()
    # sends message if hour ist 18
    if now.hour == 11:
        channel_id = 1201958342990508043  
        channel = bot.get_channel(channel_id)
        try:    
                message = await channel.fetch_message(
                channel.last_message_id) 
                await message.delete()
        except Exception as e:
                print(e)
        await channel.send(embed=lecturedata.regular_data(date.today()))   
        print("done")

@bot.event
async def on_ready():
    print(f'{bot.user} is now ready!')
    try:
        synced =await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        regular_lecture.start()
        ws= xw.Book("plzdoc.xlsx").sheets["Sheet1"]
    except Exception as e:
        print(e)
    



#main entry point
def main()-> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()