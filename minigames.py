import random
import discord

def password(length):
    all = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!%&/><+-()@"
    password = ""
    for i in range(length):
        password += random.choice(all)
    return password

# creating a list with number (= dice)
dice = [1,2,3,4,5,6]

# getting random number
def roll():
    global choice
    choice = random.choice(dice)
    return choice

def dice_embed(choice):
    embed = discord.Embed(
                            title = f"**Congratulations!**",
                            
                            description="\n\n",
                            color=0xD9A4FC        
                            )
   # embed.add_field(name="┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄",value='',inline=True)
    embed.add_field(name="",value=f"You rolled a **{choice}**.", inline=False)
    embed.set_footer(text="Don't get addicted to gambling!",icon_url="https://cdn.discordapp.com/attachments/909054108235862066/1178115964152328232/guycoding.png?ex=65beccfe&is=65ac57fe&hm=e434044069bea56e66c39fd651e713d7f189e84f069ad0f9ea89c98a012eaaac&")
    if choice == 1:
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1202171813098950656/number1-removebg-preview.png?ex=65cc7cbf&is=65ba07bf&hm=31836eb32da9b1d6f80bcda940577a74b8dd17f3af5f35426ee63bbecd4791f0&")
    elif choice == 2:
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1202171830148792340/number2-removebg-preview.png?ex=65cc7cc3&is=65ba07c3&hm=f1f4cb3d6160bbbe8d29e03fcfe74b782d7c3b03e2bb8a71edb5d706d61d85bd&")
    elif choice == 3:
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1202171841477886003/number3-removebg-preview.png?ex=65cc7cc6&is=65ba07c6&hm=0afacac458988eaac37c3c35a1bbc13d93ce45e05cf21c69072b3453e8f72214&") 
    elif choice == 4:
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1202171851271311361/number4-removebg-preview.png?ex=65cc7cc8&is=65ba07c8&hm=a006d03c33b57486ed91a9ffb1198246b077b1819cfa3a77809176291b0a9618&")
    elif choice == 5:
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1202171860662362192/number5-removebg-preview.png?ex=65cc7cca&is=65ba07ca&hm=5386665b5dd676e26e82019e15bb02db01812901a00b546471cdff7bcdf2ccdd&")
    elif choice == 6:
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1202171964614262804/imagenew-removebg-preview.png?ex=65cc7ce3&is=65ba07e3&hm=e9ab0a94116d385f978c64cb95390217055ab9741a0a5251a330a612eeef4a31&")
    return embed