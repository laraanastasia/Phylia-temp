#############################################################################################################
#############################################################################################################
#############################################################################################################
######                                                                                                 ###### 
######      For questions concerning the lecture plan pls contact @alex1401 on discord                 ######
######                                                                                                 ######
#############################################################################################################
#############################################################################################################
#############################################################################################################


# imports and extensions
from icalendar import Calendar
from datetime import date, datetime, timedelta
import discord
import discord.utils
from discord.ui import Button, View
import discord.utils
import pytz
import requests

# declaring global variables
global counter
counter = 0
lecturecounter = 0
currentdate = date.today()
message = ''
week = 1
month = 1
year = date.today().year
select = None
day = 1

# function for getting the first day of a month 
def get_firstofmonth(month):
      firstofmonth = datetime(int(year), month, 1, 12, 0, 0, 0)
      return firstofmonth

# function for chaning the month (global)
def set_month(input):
       global month
       month = input
       return month

# function called by buttonsclass (semi-copied)
def lecture_data(date_entry):
    cal_url = "https://stuv.app/MOS-TINF23A/ical"
    target_date = date_entry #style 2023, 12, 20
    response = requests.get(cal_url)
    if response.status_code == 200:
                # parsing the iCal data
                cal_data = response.text
                # parse the iCal data using the icalendar library
                cal = Calendar.from_ical(cal_data)
                target_date_events = []
                for event in cal.walk('VEVENT'):
                        start_time = event.get('dtstart').dt
                        # comparing entry date with ALL dates
                        if start_time.date()== target_date:
                            global lecturecounter
                            lecturecounter += 1
                            summary = event.get('summary')
                            end_time = event.get('dtend').dt
                            room = event.get('location')
                            # converting UTC+0 to UTC+1
                            target_timezone = pytz.timezone('Europe/Paris')  # Replace with your target timezone
                            start_time = start_time.astimezone(target_timezone)
                            end_time = end_time.astimezone(target_timezone)
                            # adding data to target_date_events
                            target_date_events.append({
                                'summary': summary,
                                'start_time': start_time.strftime("%H:%M" + ' Uhr'),
                                'end_time': end_time.strftime("%H:%M" + ' Uhr'),
                                'room': room
                            })

    lecture_lists = []
    # printing out all lectures for the fitting date through discord-embeds
    for event in (target_date_events):
                            embed = discord.Embed(
                            title = f"**Vorlesung vom *{date_entry.strftime("%d.%m.%Y")}***",
                            
                            description="\n\n",
                            color=0xD9A4FC        
                            )
                            # creating a list with all the lecture data and adding it to the "big list"
                            lecture_info = [
                                event['summary'],
                                event['start_time'],
                                event['end_time'],
                                event['room']
                            ]
                            lecture_lists.append(lecture_info)
                 
    # adding the lecture data to the embed
    try:    
        for i in range(lecturecounter):
            embed.add_field(name="┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄",value='',inline=True)
            embed.add_field(name="__"+lecture_lists[i][0]+"__:",value="- Beginn: "+"*"+lecture_lists[i][1]+"*"+ "   ┃   Ende: *"+lecture_lists[i][2]+"*"+ "\n"+"- Raum: *"+lecture_lists[i][3]+"*", inline=False)
            embed.set_footer(text="‎ ",icon_url="https://cdn.discordapp.com/attachments/909054108235862066/1178115964152328232/guycoding.png?ex=65beccfe&is=65ac57fe&hm=e434044069bea56e66c39fd651e713d7f189e84f069ad0f9ea89c98a012eaaac&")
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1200276858088988682/541px-DHBW-Logo-2-2.webp?ex=65c597ef&is=65b322ef&hm=d04afcf8052adc2620286cc74f3fd58512542d6ce186ab5dd60d98f088335a9a&")
        
        return embed
    except Exception as e:
         embed2 = discord.Embed(
                            title = f"**An diesem Tag gibt es keine Vorlesung!!**",
                            
                            description="\n\n",
                            color=0xD9A4FC        
                            )
        # Creating a list with all the lecture data and adding it to the "big list"               
         embed2.add_field(name="┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄",value="*Glückwunsch :)*")
         embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/909054108235862066/1201514069161681026/sun-48213-removebg-preview.png?ex=65ca182d&is=65b7a32d&hm=ca6aa089f7f7b200e1a6cf63b24158d131524f7a18ae23208c0f9ef81d77342a&")
         embed2.set_footer(text="Enjoy the weather!",icon_url="https://cdn.discordapp.com/attachments/909054108235862066/1178115964152328232/guycoding.png?ex=65beccfe&is=65ac57fe&hm=e434044069bea56e66c39fd651e713d7f189e84f069ad0f9ea89c98a012eaaac&")
         embed2.set_image(url="https://cdn.discordapp.com/attachments/1179494047153389579/1201512263606079488/semesterferien1200x600.png?ex=65ca167e&is=65b7a17e&hm=d6c48c8298891637f99b48f7fb6ce4c28299346e48d0630319078453d7980b39&")
         return embed2
    
# function for printing regular lecture plan
def regular_data(date_entry2):
    global lecturecounter
    lecturecounter = 0
    cal_url = "https://stuv.app/MOS-TINF23A/ical"
    target_date2 = date_entry2 #style 2023, 12, 20
    response = requests.get(cal_url)
    if response.status_code == 200:
                # parsing the iCal data
                cal_data = response.text
                # parse the iCal data using the icalendar library
                cal2 = Calendar.from_ical(cal_data)
                target_date_events2 = []
                for event in cal2.walk('VEVENT'):
                        start_time2 = event.get('dtstart').dt
                        # comparing entry date with ALL dates
                        if start_time2.date()== target_date2:
                            lecturecounter += 1
                            summary2 = event.get('summary')
                            end_time2 = event.get('dtend').dt
                            room2 = event.get('location')
                            # converting UTC+0 to UTC+1
                            target_timezone2 = pytz.timezone('Europe/Paris')  # Replace with your target timezone
                            start_time2 = start_time2.astimezone(target_timezone2)
                            end_time2 = end_time2.astimezone(target_timezone2)
                            # adding data to target_date_events
                            target_date_events2.append({
                                'summary': summary2,
                                'start_time': start_time2.strftime("%H:%M" + ' Uhr'),
                                'end_time': end_time2.strftime("%H:%M" + ' Uhr'),
                                'room': room2
                            })

    lecture_lists2 = []
    # printing out all lectures for the fitting date through discord-embeds
    for event in (target_date_events2):
                            embed = discord.Embed(
                            title = f"**Vorlesung vom *{date_entry2.strftime("%d.%m.%Y")}***",
                            
                            description="\n\n",
                            color=0xD9A4FC        
                            )
                            # creating a list with all the lecture data and adding it to the "big list"
                            lecture_info2 = [
                                event['summary'],
                                event['start_time'],
                                event['end_time'],
                                event['room']
                            ]
                            lecture_lists2.append(lecture_info2)
                 
    # adding the lecture data to the embed
    try:    
        for i in range(lecturecounter):
            embed.add_field(name="┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄",value='',inline=True)
            embed.add_field(name="__"+lecture_lists2[i][0]+"__:",value="- Beginn: "+"*"+lecture_lists2[i][1]+"*"+ "   ┃   Ende: *"+lecture_lists2[i][2]+"*"+ "\n"+"- Raum: *"+lecture_lists2[i][3]+"*", inline=False)
            embed.set_footer(text="‎ ",icon_url="https://cdn.discordapp.com/attachments/909054108235862066/1178115964152328232/guycoding.png?ex=65beccfe&is=65ac57fe&hm=e434044069bea56e66c39fd651e713d7f189e84f069ad0f9ea89c98a012eaaac&")
        embed.set_image(url="https://cdn.discordapp.com/attachments/909054108235862066/1200276858088988682/541px-DHBW-Logo-2-2.webp?ex=65c597ef&is=65b322ef&hm=d04afcf8052adc2620286cc74f3fd58512542d6ce186ab5dd60d98f088335a9a&")
        
        return embed
    except Exception as e:
         embed2 = discord.Embed(
                            title = f"**An diesem Tag gibt es keine Vorlesung!!**",
                            
                            description="\n\n",
                            color=0xD9A4FC        
                            )
                            # Creating a list wie all the lecture data and adding it to the "big list"
                       
         embed2.add_field(name="┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄",value="*Glückwunsch :)*")
         embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/909054108235862066/1201514069161681026/sun-48213-removebg-preview.png?ex=65ca182d&is=65b7a32d&hm=ca6aa089f7f7b200e1a6cf63b24158d131524f7a18ae23208c0f9ef81d77342a&")
         embed2.set_footer(text="Enjoy the weather!",icon_url="https://cdn.discordapp.com/attachments/909054108235862066/1178115964152328232/guycoding.png?ex=65beccfe&is=65ac57fe&hm=e434044069bea56e66c39fd651e713d7f189e84f069ad0f9ea89c98a012eaaac&")
         embed2.set_image(url="https://cdn.discordapp.com/attachments/1179494047153389579/1201512263606079488/semesterferien1200x600.png?ex=65ca167e&is=65b7a17e&hm=d6c48c8298891637f99b48f7fb6ce4c28299346e48d0630319078453d7980b39&")
         return embed2

# class for creating embed_buttons
class embed_buttons(discord.ui.View):
    interaction=discord.Interaction
    # days-button on embed
    @discord.ui.button(custom_id = f"{interaction.id}~days_button",label="ay", style=discord.ButtonStyle.gray,row=1,emoji="🇩")
    async def days_callback(self, interaction:discord.Interaction, button):
            await interaction.response.defer()
            await interaction.message.edit(view=buttons(interaction,week,month,datetime.today().strftime("%Y")))
    # weeks-button on embed
    @discord.ui.button(custom_id = f"{interaction.id}~week_button",label="eek", style=discord.ButtonStyle.gray,row=1,emoji="🇼")
    async def weeks_callback(self, interaction:discord.Interaction, button):
        await interaction.response.defer()
        global message
        message = await interaction.message.edit(view=WeekSelectionView(interaction))
    # months-button on embed
    @discord.ui.button(custom_id = f"{interaction.id}~month:button",label="onth", style=discord.ButtonStyle.gray,row=1,emoji="🇲")
    async def month_callback(self, interaction:discord.Interaction, button):
        await interaction.response.defer()
        await interaction.message.edit(view=MonthSelection())

# function for creating all buttons
def buttons(interaction:discord.Interaction,week,month,year):
            global day
            day = 1
            days = day + 7*(week-1)
            global currentdate
            currentdate = datetime(int(year), month, days, 0, 0, 0, 0)
            buttons_view = View()
            for j in range(0,5):
                    if j % 2 != 0:
                        temp2 = j
                        j = (Button(custom_id = f"{interaction.id}~{currentdate+timedelta(days=temp2)}",style=discord.ButtonStyle.green, label=str((currentdate+timedelta(days=j)).strftime("%d.%m")),row=1))
                        buttons_view.add_item(j)                             
                        j.callback = lambda j: buttons_callback(j)   # lambda: one-line function that points to the callback (when clicking button) in a fast anonymous way                  
                    else:
                        temp2 = j
                        j = (Button(custom_id = f"{interaction.id}~{currentdate+timedelta(days=temp2)}",style=discord.ButtonStyle.blurple, label=str((currentdate+timedelta(days=j)).strftime("%d.%m")),row=1))
                        buttons_view.add_item(j)
                        j.callback = lambda j: buttons_callback(j)
            return buttons_view

# reaction for clicking a button is initialized by this function
async def buttons_callback(interaction: discord.Interaction):
                      date = interaction.data['custom_id'].split('~')[1]
                      global lecturecounter
                      lecturecounter = 0
                      global currentdate
                      currentdate = interaction.data['custom_id'].split('~')[1]
                      global day
                      await interaction.response.defer()
                      await interaction.message.edit(embed = lecture_data(datetime.strptime(date,"%Y-%m-%d %H:%M:%S").date()),view = embed_buttons())
                         
# creating a selecting menu for the weeks
class WeekSelectionView(discord.ui.View):
    def __init__(self,interaction:discord.Interaction):
        super().__init__()
        self.select = WeekSelection()
        self.add_item(self.select)
# creating the data for selection and adding it to discord selection menu
def WeekSelection():
                global select
                options = []
                for i in range(1, 5 + 1):
                    first_day = get_firstofmonth(month)+timedelta(days=7*(i-1))
                    last_day = first_day+timedelta(days=4)

                    option = discord.SelectOption(
                        label=f"Week {i}",
                        description=f"{first_day.strftime('%d.%m')} - {last_day.strftime('%d.%m')}",
                    )
                    options.append(option) 
                    
                select_options = options
                select = discord.ui.Select(placeholder="Choose a week!",
                        min_values=1,
                        max_values=1,
                        options=select_options,)
                select.callback = my_callback
                return select

# reaction for clicking on a week triggers this function
async def my_callback(interaction):
                    global week
                    for i in range(1,6):
                        if select.values[0] == f"Week {i}":
                            week = i
                            break
                    global counter
                    counter = 1   
                    await interaction.message.edit(view=buttons(interaction,week,month,year))
                    await interaction.response.defer()
            
# function to generate selecting menu for months
class MonthSelection(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.select = Months()
        self.add_item(self.select) 

# creating the actual menu
def Months():
        global months
        months = ["January","February","March","April","May","June","July","August","September","October","November","Dezember"]
        options = []
        for element in months:
                option = discord.SelectOption(
                    label = f"{element}",
                    description = f"{str(int(months.index(element))+1)}. month"
                    )
                options.append(option)
        select_options2 = options
        global select2
        select2 = discord.ui.Select(
                    placeholder = "Choose a month!",
                    min_values = 1,
                    max_values = 1,
                    options = select_options2
                    )
        select2.callback = my_callback2
        return select2

# function for answering to the reaction of clicking on a select option       
async def my_callback2(interaction):
        for i in range(len(months)):
            if select2.values[0] == months[i]:
                set_month(i+1)
                await interaction.message.edit(embed = lecture_data(currentdate), view = embed_buttons())
                await interaction.response.defer()
                    