import discord
from discord import app_commands
from discord.ui import View, Button, Select
from discord.ext import commands, tasks
import os
import json
import random
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load user data from a JSON file
if os.path.exists('user_data.json'):
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

def user_dump():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

if os.path.exists('item_data.json'):
    with open('item_data.json', 'r') as e:
        item_data = json.load(e)
else:
    item_data = {}

def item_dump():
    with open('item_data.json', 'w') as file:
        json.dump(item_data, file, indent=4)

if os.path.exists('job_data.json'):
    with open('job_data.json', 'r') as t:
        job_data = json.load(t)
else:
    job_data = {}

def job_dump():
    with open('job_data.json', 'w') as file:
        json.dump(job_data, file, indent=4)

if os.path.exists('bot_data.json'):
    with open('bot_data.json', 'r') as q:
        bot_data = json.load(q)
else:
    bot_data = {}

def bot_dump():
    with open('bot_data.json', 'w') as file:
        json.dump(bot_data, file, indent=4)

cooldowns = {}

token = os.getenv('DISCORD_BOT_TOKEN')
guild_id = 1301922025383661640
ROLE_NAME = 1302039248286912532
cards = ["Ace-of-Hearts", "Ace-of-Spades", "Ace-of-Diamonds", "Ace-of-Clovers", "King-of-Hearts", "King-of-Spades", "King-of-Diamonds", "King-of-Clovers", "Queen-of-Hearts", "Queen-of-Spades", "Queen-of-Diamonds", "Queen-of-Clovers", "Jack-of-Hearts", "Jack-of-Spades", "Jack-of-Diamonds", "Jack-of-Clovers", "Ten-of-Hearts", "Ten-of-Spades", "Ten-of-Diamonds", "Ten-of-Clovers", "Nine-of-Hearts", "Nine-of-Spades", "Nine-of-Diamonds", "Nine-of-Clovers", "Eight-of-Hearts", "Eight-of-Spades", "Eight-of-Diamonds", "Eight-of-Clovers", "Seven-of-Hearts", "Seven-of-Spades", "Seven-of-Diamonds", "Seven-of-Clovers", "Six-of-Hearts", "Six-of-Spades", "Six-of-Diamonds", "Six-of-Clovers", "Five-of-Hearts", "Five-of-Spades", "Five-of-Diamonds", "Five-of-Clovers", "Four-of-Hearts", "Four-of-Spades", "Four-of-Diamonds", "Four-of-Clovers", "Three-of-Hearts", "Three-of-Spades", "Three-of-Diamonds", "Three-of-Clovers", "Two-of-Hearts", "Two-of-Spades", "Two-of-Diamonds", "Two-of-Clovers"]

def calculate_hand_value(hand, card_values):
    value = sum(card_values[card.split('-')[0]] for card in hand)
    # Adjust for Aces
    num_aces = sum(1 for card in hand if card.startswith('Ace'))
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

class MyView(View):
    def __init__(self, add_hows_your_day: bool, add_bye: bool):
        super().__init__()
        if add_hows_your_day:
            button = Button(label="How's your day?", style=discord.ButtonStyle.primary)
            button.callback = self.hows_your_day
            self.add_item(button)
        if add_bye:
            button = Button(label="Bye", style=discord.ButtonStyle.danger)
            button.callback = self.bye
            self.add_item(button)

    async def hows_your_day(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_message("I'm doing great, thanks for asking!")

    async def bye(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_message("Goodbye!")

class MemberSelect(discord.ui.Select):
    def __init__(self, members, callback):
        options = [discord.SelectOption(label=member.nick, value=str(member.id)) for member in members]
        super().__init__(placeholder="Choose a member...", min_values=1, max_values=1, options=options)
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        selected_member_id = int(self.values[0])
        selected_member = interaction.guild.get_member(selected_member_id)
        await self.callback_function(interaction, selected_member)

class MemberView(discord.ui.View):
    def __init__(self, members, callback):
        super().__init__()
        self.add_item(MemberSelect(members, callback))

class subsubLocView(View):
    def __init__(self, loc, inter):
        super().__init__()
        self.add_item(subsubLocSelect(loc, inter))

class subsubLocSelect(Select):
    def __init__(self, loc, inter):
        self.loc = loc
        if loc == "B":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the bapel store."
        elif loc == "D":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the dock."
        elif loc == "Pu":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "G":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "P":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "O":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "Po":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "M":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "F":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        elif loc == "Bu":
            nam1 = "Leave"
            val1 = "L"
            desc1 = "Leave the pub."
        options = [discord.SelectOption(label=nam1, value=val1, description=desc1)]
        super().__init__(placeholder="...", min_values=1, max_values=1, options=options)
    async def subsubLoc(self, inter: discord.Interaction):
        nam = ""
        sloc = self.loc
        if sloc == "B":
            nam = "Bapel store"
        elif sloc == "D":
            nam = "Dock"
        elif sloc == "Pu":
            nam = "Pub"
        elif sloc == "G":
            nam = ""
        if self.values[0] == "L":
            v = subView(loc="S", inter=inter)
            await inter.edit_original_response(content=f"You left the {nam}.", view=v)

class SubLocationSelect(Select):
    def __init__(self, loc, inter):
        npc = ""
        npc_desc = ""
        self.loc = loc
        if loc == "S":
            print("Hi")
            nam1 = "Bapel"
            val1 = "B"
            desc1 = "A phone company. Waaaay too overpriced."
            nam2 = "Grocery store"
            val2 = "G"
            desc2 = "A store for groceries."
            if "Ronald" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Ronald']['Relation'] >= 1:
                    npc = "Ronald"
                    npc_desc = "Ronald stands by the bapel store."
            else:
                npc = "Stranger"
                npc_desc = "You notice a stranger standing by the bapel store."
            nam3 = npc
            val3 = "N"
            desc3 = npc_desc
        elif loc == "Po":
            print("Hi")
            nam1 = "Dock"
            val1 = "D"
            desc1 = "A dock with a small rowboat."
            nam2 = "Pond side"
            val2 = "P"
            desc2 = "Foxtail sprouts from the shallow water."
            if "Edvard" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Edvard']['Relation'] > 1:
                    npc = "Edvard"
                    npc_desc = "You see Edvard by the pond."
            else:
                npc = "Forester"
                npc_desc = "A man is walking by the pond."
            nam3 = npc
            val3 = "E"
            desc3 = npc_desc
        elif loc == "C":
            print("Hi")
            nam1 = ""
            val1 = ""
            desc1 = ""
            nam2 = ""
            val2 = ""
            desc2 = ""
            nam3 = ""
            val3 = ""
            desc3 = ""
        elif loc == "A":
            print("Hi")
            nam1 = "Pub"
            val1 = "Pu"
            desc1 = "A small pub. Not many go here."
            if "Dina" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Dina']['Relation'] > 7 and user_data[str(inter.user.id)]['Characters']['Dina']['Progress'] >= 1:
                    npc = "Dina"
                    npc_desc = "Dina is at her usual spot."
                elif user_data[str(inter.user.id)]['Characters']['Dina']['Relation'] > 1:
                    npc = "the Stranger."
                    npc_desc = "She's still there."
            else:
                npc = "the Stranger"
                npc_desc = "A stranger leans against a wall of the alley paying you no mind."
            nam2 = npc
            val2 = "Di"
            desc2 = npc_desc
            nam3 = ""
            val3 = ""
            desc3 = ""
        elif loc == "H":
            print("Hi")
            nam1 = "Enter"
            val1 = "O"
            desc1 = "Enter the hut."
            nam2 = "Pond"
            val2 = "Po"
            desc2 = "The water reflects the sun giving everything a golden hue."
            nam3 = ""
            val3 = ""
            desc3 = ""
        elif loc == "O":
            print("Hi")
            nam1 = "Manager"
            val1 = "M"
            desc1 = "The manager of the offices."
            if "Britney" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Britney']['Relation'] > 1:
                    npc = "Britney"
                    npc_desc = "Britney is sorting files."
            else:
                npc = "Office worker"
                npc_desc = "She's sorting files."
            nam2 = npc
            val2 = "G"
            desc2 = npc_desc
            nam3 = ""
            val3 = ""
            desc3 = ""
        elif loc == "P":
            print("Hi")
            nam1 = "Fountain"
            val1 = "F"
            desc1 = "Go to the fountain."
            if "Kevin" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Kevin']['Relation'] > 1:
                    npc = "Kevin"
                    npc_desc = "Kevin is tending to the park."
            else:
                npc = "Park keeper"
                npc_desc = "You see the park keeper tending to the park."
            nam2 = npc
            val2 = "K"
            desc2 = npc_desc
            nam3 = ""
            val3 = ""
            desc3 = ""
        elif loc == "L":
            print("Hi")
            if "John" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['John']['Relation'] > 3:
                    npc = "John"
                    npc_desc = "John seems busy."
            else:
                npc = "Lumberer"
                npc_desc = "A lumberer is sawing off branches of a log."
            nam1 = npc
            val1 = "S"
            desc1 = npc_desc
            nam2 = "Buy lumber"
            val2 = "Bu"
            desc2 = "Buy some lumber won't-cha, chap?"
            nam3 = ""
            val3 = ""
            desc3 = ""
        elif loc == "D":
            print("Hi")
            if "Garry" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Garry']['Relation'] > 1:
                    npc = "Garry"
                    npc_desc = "Garry is hard at work monitoring the servers."
            else:
                npc = "Computer guy"
                npc_desc = "A guy is monitoring all the servers."
            nam1 = npc
            val1 = "S"
            desc1 = npc_desc
            nam2 = ""
            val2 = ""
            desc2 = ""
            nam3 = ""
            val3 = ""
            desc3 = ""
        options = []
        if nam1 != "": options.append(discord.SelectOption(label=nam1, value=val1, description=desc1))
        if nam2 != "": options.append(discord.SelectOption(label=nam2, value=val2, description=desc2))
        if nam3 != "": options.append(discord.SelectOption(label=nam3, value=val3, description=desc3))
        options.append(discord.SelectOption(label="Leave", value="L", description=""))
        super().__init__(placeholder="What do you do?", max_values=1, min_values=1, options=options)
        self.callback = self.subsubloc
    async def subsubloc(self, inter: discord.Interaction):
        user_id = str(inter.user.id)
        print("Hi, subsubloc.")
        if self.values[0] == "L":
            if self.loc in ["S", "A", "P"]:
                home = "T"
                if self.loc == "S":
                    nam = "Super market"
                elif self.loc == "A":
                    nam = "Alley"
                elif self.loc == "P":
                    nam = "Park"
                view1 = locView(loc=home)
                await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
            elif self.loc in ["Po", "H", "L"]:
                home = "F"
                if self.loc == "Po":
                    nam = "Pond"
                elif self.loc == "H":
                    nam = "Hut"
                elif self.loc == "L":
                    nam = "Lumber yard"
                view1 = locView(loc=home)
                await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
            elif self.loc in ["C", "O", "D"]:
                home = "K"
                if self.loc == "C":
                    nam = "Cafeteria"
                elif self.loc == "O":
                    nam = "Offices"
                elif self.loc == "D":
                    nam = "Data room"
                view1 = locView(loc=home)
                await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "Po":
            view1 = subView(loc="Po", inter=inter)
            await inter.response.edit_message(content=f"You went to the pond.", view=view1)
        elif self.values[0] == "B":
            view1 = subsubLocView(loc="B", inter=inter)
            await inter.response.edit_message(content=f"You went to the bapel store.", view=view1)
        elif self.values[0] == "Di":
            v = Npc(inter=inter, val=3)
            if "Dina" in user_data[user_id]["Characters"]:
                if user_data[user_id]["Characters"]["Dina"]["Progress"] >= 1: nam = "Dina"
                else: nam = "the Stranger"
            else: nam = "the Stranger"
            await inter.response.edit_message(content=f"You walked over to {nam}.", view=v)
        elif self.values[0] == "Pu":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "Bu":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "O":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "N":
            npc = Npc(inter, 2)
            if "Ronald" in user_data[user_id]['Characters']: nam = "Ronald"
            else: nam = "the Stranger"
            await inter.response.edit_message(content=f"You walked over to {nam}.", view=npc)
        elif self.values[0] == "E":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "K":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "G":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)
        elif self.values[0] == "P":
            await inter.response.edit_message(content=f"You left the {nam}.", view=view1)

class subView(View):
    def __init__(self, loc, inter):
        super().__init__()
        self.add_item(SubLocationSelect(loc=loc, inter=inter))

class LocationSelect(Select):
    def __init__(self, loc):
        if loc == "T":
            name1 = "Super Market"
            desc1 = "Theres people walking from store to store."
            loc1 = "S"
            name2 = "Alley"
            desc2 = "Yeah... I wouldn't stay here for long were I you."
            loc2 = "A"
            name3 = "Park"
            desc3 = "The shadow of trees giving the temporary feeling of calm."
            loc3 = "P"
        elif loc == "F":
            name1 = "Pond"
            desc1 = "The water reflects the sun giving everything a golden hue."
            loc1 = "Po"
            name2 = "Hut"
            desc2 = "It's a hut. Not much around, but it's there."
            loc2 = "H"
            name3 = "Lumber Yard"
            desc3 = "You hear saws and axes from every direction."
            loc3 = "L"
        elif loc == "K":
            name1 = "Cafeteria"
            desc1 = "It's empty."
            loc1 = "C"
            name2 = "Offices"
            desc2 = "Rows upon rows of workers. How are they all in sync?"
            loc2 = "O"
            name3 = "Data Room"
            desc3 = "Racks upon racks of servers. Fans spinning loudly."
            loc3 = "D"
        options = [discord.SelectOption(label=name1, value=loc1, description=desc1),
                   discord.SelectOption(label=name2, value=loc2, description=desc2),
                   discord.SelectOption(label=name3, value=loc3, description=desc3),
                   discord.SelectOption(label="Leave", value="Q", description="You go home.")]
        super().__init__(placeholder="Where do you go?", min_values=1, max_values=1, options=options)
        self.callback = self.sub_loc
    async def sub_loc(self, inter: discord.Interaction):
        view1 = subView(loc=self.values[0], inter=inter)
        print(f"Selected value: {self.values[0]}")
        if self.values[0] == "S":
            await inter.response.edit_message(content="You went to the super market.", view=view1)
        elif self.values[0] == "Po":
            await inter.response.edit_message(content="You went to the pond.", view=view1)
        elif self.values[0] == "C":
            await inter.response.edit_message(content="You went to the cafeteria.", view=view1)
        elif self.values[0] == "A":
            await inter.response.edit_message(content="You went down an alley..", view=view1)
        elif self.values[0] == "H":
            await inter.response.edit_message(content="You went to a hut.", view=view1)
        elif self.values[0] == "O":
            await inter.response.edit_message(content="You went to the offices.", view=view1)
        elif self.values[0] == "P":
            await inter.response.edit_message(content="You went to the park.", view=view1)
        elif self.values[0] == "L":
            await inter.response.edit_message(content="You went to the lumber yard.", view=view1)
        elif self.values[0] == "D":
            await inter.response.edit_message(content="You went to the data room.", view=view1)

class locView(View):
    def __init__(self, loc):
        super().__init__()
        self.add_item(LocationSelect(loc=loc))

class MySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Visit Someone", description="Pay someone in the hospital a visit.", value="V"),
            discord.SelectOption(label="Full Heal", description="Heal someone to max health instantly. (Requires a medkit.)", value="F"),
            discord.SelectOption(label="Talk to Doctor", description="Talk to the doctor.", value="T")
        ]
        super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        hospital_role = interaction.guild.get_role(1308730447387164702)
        async def hospital_callback(inter: discord.Interaction, selected_member: discord.Member):
            if self.values[0] == "V":
                await inter.response.send_message(f"You visited {selected_member.nick}.")
                chance = random.randint(1,15)
                heal_time = user_data[str(selected_member.id)]['cooldowns']['Heal-Time']
                if chance == 1:
                    user_data[str(selected_member.id)]['cooldowns']['Heal-Time'] - (heal_time/2)
                    await selected_member.send(f"{inter.user.nick} visited you. Your spirit increased halving your remaining heal-time.")
                else:
                    await selected_member.send(f"{inter.user.nick} visited you while you were in the hospital.")
            elif self.values[0] == "F":
                if "medkit" in user_data[str(inter.user.id)]['Inv']['tools']:
                    await inter.response.send_message(f"You healed {selected_member.nick} to max health.", ephemeral=True)
                    await selected_member.send(f"{inter.user.nick} healed you to max health. You are no longer hospitalized.")
                    role_ids = user_data[str(selected_member.id)]['Roles']
                    roles = [inter.guild.get_role(role_id) for role_id in role_ids if inter.guild.get_role(role_id) is not None]
                    await selected_member.remove_roles(hospital_role)
                    await selected_member.add_roles(*roles)
                    user_data[str(selected_member.id)]['Health'] = 250
                    user_data[str(selected_member.id)]['Roles'].clear()
                    user_data[str(selected_member.id)]['Heal-Time'] = 0
                else:
                    await inter.response.send_message(f"You don't have any medkits to heal {selected_member.nick} with... ", ephemeral=True)
        if self.values[0] == "V":
            members_with_role = [member for member in interaction.guild.members if hospital_role in member.roles]
            if not members_with_role:
                await interaction.response.send_message("No members found with that role.", ephemeral=True)
                return

            view = MemberView(members_with_role, hospital_callback)
            await interaction.response.send_message("Who do you want to visit?", view=view, ephemeral=True)
        elif self.values[0] == "F":
            members_with_role = [member for member in interaction.guild.members if hospital_role in member.roles]
            if not members_with_role:
                await interaction.response.send_message("No members found with that role.", ephemeral=True)
                return

            view = MemberView(members_with_role, hospital_callback)
            await interaction.response.send_message("Who do you want to visit?", view=view, ephemeral=True)
        elif self.values[0] == "T":
            view = Npc(interaction, 1)
            await interaction.response.send_message(f'"Hello there. Did you need anything?"', view=view, ephemeral=True)
        user_dump()

class MyOptions(View):
    def __init__(self):
        super().__init__()
        self.add_item(MySelect())

class NPC(Select):
    def __init__(self, inter, val):
        quest = ""
        self.val = val
        if val == 1:
            quest = "Have anything you need help with?"
            if user_data[str(inter.user.id)]['Characters']['Doctor']['Progress'] == 1:
                quest = "Heres the five burgers you wanted."
            options = [
                discord.SelectOption(label="How are you doing today?", value="H"),
                discord.SelectOption(label=quest, value="A"),
                discord.SelectOption(label="Nevermind, forgot what it was about.", value="N")
            ]
        elif val == 2:
            inte = "Hey, what's your name?"
            quest = ""
            if "Ronald" in user_data[str(inter.user.id)]['Characters']:
                inte = "Ronald! How's it been."
                if user_data[str(inter.user.id)]['Characters']['Ronald']['Relation'] > 5:
                    quest = "Do you need help with anything?"
                    if user_data[str(inter.user.id)]['Characters']['Ronald']['Progress'] == 1:
                        quest = "Hey Ronald! About that erand you had me run."
        elif val == 3:
            inte = "Hello, what's your name?"
            quest = ""
            ron = ""
            if "Dina" in user_data[str(inter.user.id)]['Characters']:
                inte = "Hey, how's things been?"
                if user_data[str(inter.user.id)]['Characters']['Dina']['Relation'] > 5 and user_data[str(inter.user.id)]['Characters']['Dina']['Progress'] == 1:
                    quest = "Do you need help with anything?"
                    if user_data[str(inter.user.id)]['Characters']['Dina']['Progress'] == 1:
                        quest = ""
            if "Ronald" in user_data[str(inter.user.id)]['Characters']:
                if user_data[str(inter.user.id)]['Characters']['Ronald']['Progress'] == 1:
                    ron = "Hey, Ronald told me to get something of off you. A jammer of some kind. Do you have it?"
            else:
                ron = ""
        options = []
        if inte != "" : options.append(discord.SelectOption(label=inte, value="H"))
        if quest != "" : options.append(discord.SelectOption(label=quest, value="A"))
        if val == 2 : options.append(discord.SelectOption(label="Nevermind...", value="N"))
        if ron != "": options.append(discord.SelectOption(label=ron, value="R"))
        super().__init__(placeholder="Speak...", min_values=1, max_values=1, options=options)
    async def callback(self, inter: discord.Interaction):
        chars = user_data[str(inter.user.id)]['Characters']
        if self.val == 1:
            if "Doctor" in chars:
                rel = chars['Doctor']['Relation']
                pro = chars['Doctor']['Progress']
                cooldown = user_data[str(inter.user.id)]['cooldowns']['Doctor']
            else:
                chars["Doctor"] = {"Relation": 0, "Progress": 0}
                user_data[str(inter.user.id)]['cooldowns']['Doctor'] = 0
                user_dump()
                rel = chars['Doctor']['Relation']
                pro = chars['Doctor']['Progress']
                cooldown = user_data[str(inter.user.id)]['cooldowns']['Doctor']
            if self.values[0] == "H":
                if cooldown <= 0:
                    smile = ":slight_smile:"
                    if rel > 5:
                        smile = ":smiley:"
                    elif rel > 15:
                        smile = ":smile:"
                    await inter.response.send_message(f"I'm doing quite well, thank you for asking. {smile}", ephemeral=True)
                    rel += 1
                    cooldown = 3600
                    user_dump()
                    while cooldown > 0:
                        await asyncio.sleep(1)
                        cooldown -= 1
                        user_dump()
            elif self.values[0] == "A":
                if (rel > 5):
                    if pro == 0:
                        await inter.response.send_message(f"Actually I do! Could you get me five burgers? Working all day makes one quite hungry.", ephemeral=True)
                        pro += 1
                        user_dump()
                    elif (pro == 1):
                        if user_data[str(inter.user.id)]['Inv']['burger'] >= 5:
                            await inter.response.send_message(f"Thanks! You're a lifesaver. Here, I don't have any cash on me right now so this'll have to do. | +1 Medkit", ephemeral=True)
                            if "medkit" in user_data[str(inter.user.id)]['Inv']['tools']:
                                user_data[str(inter.user.id)]['Inv']['tools']['medkit'] += 10
                            else:
                                user_data[str(inter.user.id)]['Inv']['tools']['medkit'] = 10
                                pro += 1
                            user_dump()
                        else:
                            await inter.response.send_message("What? You don't have five burgers. :face_with_monocle:")
                    else:
                        await inter.response.send_message("No, I don't think so. Nice seeing you, but I've got to get back to work.", ephemeral=True)
                else:
                    await inter.response.send_message("No, I don't think so. Oh well, I've got to get back to my work. Goodbye.", ephemeral=True)
            elif self.values[0] == "N":
                await inter.response.send_message(f"Mkay, goodbye then.", ephemeral=True)
        elif self.val == 2:
            if "Ronald" in chars:
                rel = chars['Ronald']['Relation']
                pro = chars['Ronald']['Progress']
                cooldown = user_data[str(inter.user.id)]['cooldowns']['Ronald']
            if self.values[0] == "H":
                ans = ""
                if "Ronald" in chars:
                    if rel >= 1:
                        ans = f"Hello, {inter.user.nick}. It's been horrible, every day more and more people turn to bapel!"
                    elif rel >= 10:
                        ans = f"Hi, {inter.user.nick}. It's been horrible... they just won't stop worshipping bapel... they don't even make good price to performance phones... it's irational!"
                    elif rel >= 25:
                        ans = f"{inter.user.nick}! Thanks for asking, but I'll have to answer no.. I've tried everything from preaching to sabota- uhh, nevermind. Just know it's been bad.."
                elif "Ronald" not in chars:
                    ans = "Hello, I'm Ronald. Did you know Bapel brainwashes people..."
                    chars['Ronald'] = {'Relation': 1, 'Progress': 0}
                    user_data[str(inter.user.id)]['cooldowns']['Ronald'] = 0
                    cooldown = user_data[str(inter.user.id)]['cooldowns']['Ronald']
                    user_dump()
                v = Npc(inter, self.val)
                await inter.response.edit_message(content=ans, view=v)
                cooldown = 3600
                while cooldown > 0:
                    await asyncio.sleep(1)
                    cooldown -= 1
                    user_dump()
            elif self.values[0] == "A":
                if rel >= 5:
                    ques = "I do actually... could you go to the alley and get me a item from Dina... it's a small electronic jammer... don't ask what it's for.. so can you get it?"
                    if pro == 1:
                        ques = "So... did you get the jammer?"
                    else:
                        ques = "Not at the moment no, but I might in the future... the fight against bapel never ends!"
                    v = SubNPC(inter=inter, val=2)
                    await inter.response.edit_message(content=ques, view=v)
            elif self.values[0] == "N":
                v = subView(loc="S", inter=inter)
                await inter.response.edit_message(content="You walked away...", view=v)
            else:
                await inter.response.send_message("You can't do that bruv.", ephemeral=True)
        elif self.val == 3:
            if "Dina" in chars:
                rel = chars["Dina"]["Relation"]
                pro = chars["Dina"]["Progress"]
            else:
                chars['Dina'] = {"Relation": 0, "Progress": 0}
                user_dump()
                rel = chars["Dina"]["Relation"]
                pro = chars["Dina"]["Progress"]
            if self.values[0] == "H":
                if "Dina" in user_data[str(inter.user.id)]['cooldowns']:
                    if user_data[str(inter.user.id)]['cooldowns']['Dina'] <= 0:
                        if "Dina" in chars:
                            if rel <= 2:
                                ans = "Hey, nothing much."
                            elif rel <= 5:
                                ans = f"Hello, nothing much. Thanks for asking."
                            elif rel <= 7 and chars["Dina"]["Progress"] == 0:
                                ans = f"Oh, hey {inter.user.nick.capitalize()}. Not much, also I haven't said this, but I'm Dina."
                                chars["Dina"]["Progress"] = 1
                            elif rel <= 15:
                                ans = f"{inter.user.nick.capitalize()}! I've been doing great."
                        else:
                            ans = "*The stranger looked you up and down before saying.* I'm not going to tell you that."
                            chars["Dina"] = {"Relation": 1, "Progress": 0}
                        v = Npc(inter=inter, val=3)
                        await inter.response.edit_message(content=ans, view=v)
                        chars['Dina']['Relation'] += 1
                        user_data[str(inter.user.id)]['cooldowns']['Dina'] = 3600
                        while user_data[str(inter.user.id)]['cooldowns']['Dina'] > 0:
                            await asyncio.sleep(1)
                            user_data[str(inter.user.id)]['cooldowns']['Dina'] -= 1
                            user_dump()
                    else:
                        v = subView("A", inter=inter)
                        await inter.response.edit_message(content="You've already talked to Dina recently.", view=v)
                else:
                    user_data[str(inter.user.id)]['cooldowns']['Dina'] = 0
                    user_dump()
                    v = subView("A", inter=inter)
                    await inter.response.edit_message(content="You've already talked to Dina recently.", view=v)
            elif self.values[0] == "A":
                e
            elif self.values[0] == "N":
                v = subView("A", inter=inter)
                await inter.response.edit_message(content="You walked away...", view=v)
            elif self.values[0] == "R":
                v = Npc(inter=inter, val=3)
                await inter.response.edit_message(content="Yeah, I do actually. Here, don't know if it's the right thing though.", view=v)
                user_data[str(inter.user.id)]['Inv']['electronic jammer'] = 1
        user_dump()

class Npc(View):
    def __init__(self, inter, val):
        super().__init__()
        self.add_item(NPC(inter, val))

class SubNPC(View):
    def __init__(self, inter, val):
        super().__init__()
        self.add_item(self.yes(inter, val))
        self.add_item(self.no(inter, val))
    
    async def yes(self, inter, val):
        user_id = inter[str(inter.user.id)]
        chars = user_data[user_id]['Characters']
        if val == 2:
            rel = chars['Ronald']['Relation']
            pro = chars['Ronald']['Progress']
            if (rel > 5):
                await inter.response.edit_message(content="Great! Thank you... I will be waiting for you here then..")
                pro = 1
                if pro == 1:
                    if "electronic jammer" in user_data[user_id]['Inv']['quest']:
                        if "Ronald-Ques" in user_data[user_id]['cooldowns']:
                            if user_data[user_id]['cooldowns']['Ronald-Ques'] > 0:
                                v = subView(loc="S", inter=inter)
                                await inter.response.edit_message(content="Bro, you just told me you didn't have it. Wastin my time. Give it here...\n-1 electronic jammer", view=v)
                                user_data[user_id]['cooldowns']['Ronald-Ques'] = 2
                                del user_data[user_id]['Inv']['electronic jammer']
                                pro = 2
                                user_dump()
                            else:
                                v = subView(loc="S", inter=inter)
                                await inter.response.edit_message(content="Thank you. Now be on your way then. I've got things to do...\n-1 electronic jammer", view=v)
                                user_data[user_id]['cooldowns']['Ronald-Ques'] = 2
                                del user_data[user_id]['Inv']['electronic jammer']
                                pro = 2
                                user_dump()
                        else:
                            v = subView(loc="S", inter=inter)
                            await inter.response.edit_message(content="Thank you. Now be on your way then. I've got things to do...\n-1 electronic jammer", view=v)
                            user_data[user_id]['cooldowns']['Ronald-Ques'] = 2
                            del user_data[user_id]['Inv']['electronic jammer']
                            pro = 2
                            user_dump()
                    else:
                        view1 = Npc(inter=inter, val=2)
                        await inter.response.edit_message(content="Soooo... where's the jammer? You don't have it? Then what are you waiting for! Go get it!", view=view1)

    async def no(self, inter, val):
        user_id = inter[str(inter.user.id)]
        chars = user_data[user_id]['Characters']
        if val == 2:
            rel = chars['Ronald']['Relation']
            pro = chars['Ronald']['Progress']
            if rel > 5:
                view1 = Npc(inter=inter, val=2)
                if pro == 0:
                    await inter.response.edit_message(content="Huh, I don't know why, but I was expecting you to say yes... to be fair I guess this was a more reasonable answer... ok.", view=view1)
                elif pro == 1:
                    if 'Ronald-Ques' in user_data[user_id]['cooldowns']:
                        if user_data[user_id]['cooldowns']['Ronald-Ques'] > 0:
                            await inter.response.edit_message(content="I know you don't have it! You just said that, so go get it!", view=view1)
                        else:
                            await inter.response.edit_message(content="Then what are you waiting for? Go get it!", view=view1)
                    else:
                        await inter.response.edit_message(content="Then what are you waiting for? Go get it!", view=view1)
                        user_data[user_id]['cooldowns']['Ronald-Ques'] = 60
                        while user_data[user_id]['cooldowns']['Ronald-Ques'] > 0:
                            await asyncio.sleep(1)
                            user_data[user_id]['cooldowns']['Ronald-Ques'] -= 1
                            user_dump()


class finditems:
    def __init__(self, user_data, item_data):
        self.user_data = user_data
        self.item_data = item_data

    async def buy_item(self, user_id, category, item, quantity, interaction):
        try:
            price = self.item_data[category][item]['Price']
        except KeyError:
            await interaction.response.send_message("Item not found.", ephemeral=True)
            return

        cost = int(price)
        if self.user_data[user_id]['Cash'] >= cost:
            self.user_data[user_id]['Cash'] -= cost
            if item in self.user_data[user_id]['Inv'][category]:
                self.user_data[user_id]['Inv'][category][item] += quantity
            else:
                self.user_data[user_id]['Inv'][category][item] = quantity
        else:
            await interaction.response.send_message(f"You don't have enough cash ({cost}) to buy {quantity} {item}(s).\nBalance: {self.user_data[user_id]['Cash']}")
            return

        await interaction.response.send_message(f"{interaction.user.nick.capitalize()} bought {quantity} {item}(s) for {cost} cash.\nBalance: {self.user_data[user_id]['Cash']}")
        self.save_user_data()

    def save_user_data(self):
        with open('user_data.json', 'w') as file:
            json.dump(self.user_data, file, indent=4)

class CardGame(discord.ui.View):
    def __init__(self, player_hand, bot_hand, deck, card_value, blackjack: bool):
        super().__init__()
        self.player_hand = player_hand
        self.bot_hand = bot_hand
        self.deck = deck
        self.card_value = card_value
        self.player_value = calculate_hand_value(player_hand, card_value)
        self.bot_value = calculate_hand_value(bot_hand, card_value)

        if blackjack:
            hit = Button(label="Hit", style=discord.ButtonStyle.primary)
            stay = Button(label="Stay", style=discord.ButtonStyle.secondary)
            hit.callback = self.hit
            stay.callback = self.stay
            self.add_item(hit)
            self.add_item(stay)


    async def hit(self, interaction: discord.Interaction):
        self.player_hand.append(self.deck.pop())
        self.player_value = calculate_hand_value(self.player_hand, self.card_value)
        if self.player_value > 21:
            await interaction.response.edit_message(content=f"Your hand: {self.player_hand} (value: {self.player_value})\nYou busted! Bot wins!", view=None)
        else:
            await interaction.response.edit_message(content=f"Your hand: {self.player_hand} (value: {self.player_value})\n\nBot's hand: {self.bot_hand[0]} and a hidden card.")

    async def stay(self, interaction: discord.Interaction):
        while self.bot_value < 17:
            self.bot_hand.append(self.deck.pop())
            self.bot_value = calculate_hand_value(self.bot_hand, self.card_value)
        result = "It's a tie!" if self.player_value == self.bot_value else "You win!" if self.player_value > self.bot_value or self.bot_value > 21 else "Bot wins!"
        await interaction.response.edit_message(content=f"Your hand: {self.player_hand} (value: {self.player_value})\nBot's hand: {self.bot_hand} (value: {self.bot_value})\n{result}", view=None)

@bot.event
async def on_ready():
    clear_channel.start()
    on_health_zero_task.start()
    user_check.start()
    print(f"Logged in as {bot.user}")
    print(f"GUILD_ID: {guild_id}")
    guild = bot.get_guild(guild_id)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    channel = bot.get_channel(1318187395807707147)
    if channel:
        await channel.purge()
        await channel.send('> # Bot Status: **Active**')
    timeout_time = 329*60
    if timeout_time > 0:
        timeout_time -= 1
        await asyncio.sleep(1)
    else:
        await channel.purge()
        await channel.send('> # Bot Status: **Inactive**')
    status_tasks = [user_status(member, "Jail-Time") for member in guild.members] + [user_status(member, "Heal-Time") for member in guild.members] + [user_status(member, "Job-Cooldown") for member in guild.members] + [user_status(member, "Rob-Cooldown") for member in guild.members] + [user_status(member, "Fish-Cooldown") for member in guild.members] + [user_status(member, "Search-Cooldown") for member in guild.members] + [user_status(member, "Hunt-Cooldown") for member in guild.members] + [user_status(member, "Ronald") for member in guild.members] + [user_status(member, "Doctor") for member in guild.members] + [user_status(member, "Dina") for member in guild.members] + [user_status(member, "Ronald-Ques") for member in guild.members]
    await asyncio.gather(*status_tasks)

@tasks.loop(minutes=10)
async def clear_channel():
    channel = bot.get_channel(1305525504572395592)
    if channel:
        await channel.purge(limit=100)

@tasks.loop(seconds=10)
async def on_health_zero_task():
    for guild in bot.guilds:
        for member in guild.members:
            await check_health(member)

async def check_health(member):
    hospital_role = discord.utils.get(member.guild.roles, id=1308730447387164702)
    if str(member.id) in user_data:
        if hospital_role not in member.roles:
            if user_data[str(member.id)]['Health'] <= 0:
                roles = member.roles[1:]  # Exclude @everyone role
                role_ids = [role.id for role in roles]
                user_data[str(member.id)]['Roles'] += role_ids
                await member.remove_roles(*roles)
                await member.add_roles(hospital_role)
                await member.send(f"You have been hospitalized. Time: 50 minutes.")
                user_data[str(member.id)]['cooldowns']['Heal-Time'] = 3000
                while user_data[str(member.id)]['cooldowns']['Heal-Time'] > 0:
                    await asyncio.sleep(1)
                    user_data[str(member.id)]['cooldowns']['Heal-Time'] -= 1
                    user_dump()
                updated_user = await member.guild.fetch_member(member.id)
                if hospital_role in updated_user.roles:
                    await member.remove_roles(hospital_role)
                    await member.add_roles(*roles)
                    user_data[str(member.id)]['Roles'].clear()
                    user_data[str(member.id)]['Health'] = 150
                    await member.send(f"You are no longer hospitalized.")
                    user_dump()
                else:
                    None

async def user_status(member: discord.Member, status):
    jail_role = discord.utils.get(member.guild.roles, id=1307363196448931850)
    message = "You are no longer in jail."
    if status == "Heal-Time":
        jail_role = discord.utils.get(member.guild.roles, id=1308730447387164702)
        message = "You are no longer hospitalized."
    if str(member.id) in user_data:
        role_ids = user_data[str(member.id)]['Roles']
        roles = [member.guild.get_role(role_id) for role_id in role_ids if member.guild.get_role(role_id) is not None]
        if jail_role in member.roles:
            if status in user_data[str(member.id)]['cooldowns']:
                while user_data[str(member.id)]['cooldowns'][status] > 0:
                    await asyncio.sleep(1)
                    user_data[str(member.id)]['cooldowns'][status] -= 1
                    user_dump()
                updated_user = await member.guild.fetch_member(member.id)
                if jail_role in updated_user.roles:
                    await member.send(message)
                    await member.remove_roles(jail_role)
                    await member.add_roles(*roles)
                    user_data[str(member.id)]['Roles'].clear()
                    if status == "Jail-Time":
                        user_data[str(member.id)]['Crime Score'] = 0
                        user_data[str(member.id)]['Bail'] = 0
                    elif status == "Heal-Time":
                        user_data[str(member.id)]['Health'] = 150
                    user_dump()
            else:
                await member.send(message)
                await member.remove_roles(jail_role)
                await member.add_roles(*roles)
                user_data[str(member.id)]['Roles'].clear()
                if status == "Jail-Time":
                    user_data[str(member.id)]['Crime Score'] = 0
                    user_data[str(member.id)]['Bail'] = 0
                elif status == "Heal-Time":
                    user_data[str(member.id)]['Health'] = 150
                user_dump()
        elif status in user_data[str(member.id)]['cooldowns']:
            while user_data[str(member.id)]['cooldowns'][status] > 0:
                await asyncio.sleep(1)
                user_data[str(member.id)]['cooldowns'][status] -= 1
                user_dump()

@tasks.loop(minutes=15)
async def user_check():
    guild = bot.get_guild(guild_id)
    user_checks = [user_has(member, "cooldowns", False, True) for member in guild.members] + [user_has(member, "fauna", True, True) for member in guild.members] + [user_has(member, "Characters", False, True) for member in guild.members]
    await asyncio.gather(*user_checks)

async def user_has(member: discord.Member, has, inv: bool, dict: bool):
    user_id = str(member.id)
    if user_id in user_data:
        if inv:
            if has not in user_data[user_id]['Inv']:
                if dict:
                    user_data[user_id]['Inv'][has] = {}
                else:
                    user_data[user_id]['Inv'][has] = 0
        else:
            if has not in user_data[user_id]:
                if dict:
                    user_data[user_id][has] = {}
                else:
                    user_data[user_id][has] = 0
    user_dump()

@bot.event
async def on_member_join(member):
        default_role = discord.utils.get(member.guild.roles, id=1302042075063255163)
        await member.add_roles(default_role)

# Decorator to check if the command is used in the specified channel
def is_in_channel(channel_name):
    def predicate(interaction: discord.Interaction):
        return interaction.channel.name == channel_name
    return app_commands.check(predicate)

@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")

@bot.tree.command(name="job_work", description="Earn cash by working")
async def job_work(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        job_name = user_data[user_id]['Job']
        if user_data[user_id]['Stamina'] >= job_data[job_name]['Stam']:
            if "Job-Cooldown" in user_data[user_id]['cooldowns']:
                if user_data[user_id]['cooldowns']['Job-Cooldown'] != 0:
                    await interaction.response.send_message(f"You can work again <t:{int(time.time())+user_data[user_id]['cooldowns']['Job-Cooldown']}:R>", ephemeral=True)
                    return
                else:
                    user_data[user_id]['cooldowns']['Job-Cooldown'] = job_data[job_name]['Work-Cooldown']
            else:
                user_data[user_id]['cooldowns']['Job-Cooldown'] = job_data[job_name]['Work-Cooldown']
            if job_name in job_data:
                pay = job_data[job_name]['Pay']
                stam = job_data[job_name]['Stam']
                user_data[user_id]['Cash'] += pay
                user_data[user_id]['Stamina'] -= stam
                user_data[user_id]['Shifts-Worked'] += 1
                await interaction.response.send_message(f'{interaction.user.mention}, you worked as a {job_name} and earned {pay} cash! You now have {user_data[user_id]["Cash"]} cash.')
                while user_data[user_id]['cooldowns']['Job-Cooldown'] > 0:
                    await asyncio.sleep(1)
                    user_data[user_id]['cooldowns']['Job-Cooldown'] -= 1
                    user_dump()
                user_dump()
            else:
                await interaction.response.send_message(f'{interaction.user.mention}, your job details could not be found.')
        else:
            await interaction.response.send_message(f"{interaction.user.mention}, you are too tired to work. Take a break once in a while.")
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="stats", description="Check your stats")
async def stats(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        stats = user_data[user_id]
        await interaction.response.send_message(f'{interaction.user.mention}, your stats are: Cash: {stats["Cash"]}, Health: {stats["Health"]}, Stamina: {stats["Stamina"]}, Job: {stats["Job"]}, Criminal Score: {stats["Crime Score"]}')
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="shop_view", description="View items in shop.")
async def shop_view(interaction: discord.Interaction):
    shop_message = "**Items available in the shop:**\n"
    commons = []
    tools = []
    for item, attributes in item_data.items():
        try:

            price = attributes["Price"]
            stamina = attributes["Stamina"]
            commons.append(f"{item.capitalize()}: {{Stamina: {stamina}, Price: {price}}}")
        except KeyError:
            pass
    for item, attributes in item_data['tools'].items():
        try:
            dur = attributes["dur"]
            price = attributes["Price"]
            tools.append(f"{item.capitalize()}: {{Durability: {dur}, Price: {price}}}")
        except KeyError:
            pass
    if commons:
        commons = "\n".join(commons)
        shop_message += f"```Commons:\n{commons}```"
    if tools:
        tools = "\n".join(tools)
        shop_message += f"```Tools:\n{tools}```"
    await interaction.response.send_message(shop_message)

@bot.tree.command(name="shop_buy", description="Buy an item available in the shop. Write max to buy as many as you can.")
async def shop_buy(interaction: discord.Interaction, item: str, quantity: str):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        if item in item_data:
            price = item_data[item]['Price']
            if quantity.lower() == "max":
                quantity = user_data[user_id]['Cash']//price
            else:
                try:
                    quantity = int(quantity)
                except ValueError:
                    await interaction.response.send_message("Please enter a valid number or 'max'.", ephemeral=True)
                    return
            cost = int(price * quantity)
            if user_data[user_id]['Cash'] >= cost:
                user_data[user_id]['Cash'] -= cost
                if item in user_data[user_id]['Inv']:
                    user_data[user_id]['Inv'][item] += quantity
                else:
                    user_data[user_id]['Inv'][item] = quantity
            else:
                await interaction.response.send_message(f"You don't have enough cash({cost}) to buy {quantity} {item}(s).\nBalance: {user_data[user_id]['Cash']}")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} bought {quantity} {item}(s)for {cost} cash.\nBalance: {user_data[user_id]['Cash']}")
            with open('user_data.json', 'w') as file:
                    json.dump(user_data, file, indent=4)
        elif item in item_data['tools']:
            quantity = 10
            shop = finditems(user_data, item_data)
            await shop.buy_item(user_id, 'tools', item, quantity, interaction)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="verify", description="Verify account")
async def verify(interaction: discord.Interaction, nickname: str, key: str):
    try:
        # Change the user's nickname
        await interaction.user.edit(nick=nickname)
        # Add the specified role to the user
        role = interaction.guild.get_role(ROLE_NAME)
        rm_role = interaction.guild.get_role(1302042075063255163)
        user_id = str(interaction.user.id)
        if user_id not in user_data:
            user_data[user_id] = {'Cash': 100, 'Health': 100, 'Stamina': 100, 'Job': 'Unemployed', 'Inv': {"tools": {}}, 'Key': key, 'Key-Fail': 0, 'Shifts-Worked': 0, 'Roles': [], 'Crime Score': 0, 'Bail': 0, 'NPC': {"Doctor": {"Progress": 0, "Relation": 0}, "Dave": 0}}
            bot_data['Unemployed'] += 1
            with open('user_data.json', 'w') as f:
                json.dump(user_data, f, indent=4)
            with open('bot_data.json', 'w') as file:
                json.dump(bot_data, file, indent=4)
        if role:
            await interaction.user.add_roles(role)
            if rm_role:
                await interaction.user.remove_roles(rm_role)
                await interaction.response.send_message(f"Changed nickname of {interaction.user.mention} to '{nickname}', added role '{role.name}' and removed '{rm_role.name}'")   
            else:
                await interaction.response.send_message(f"Role with ID {ROLE_NAME} not found.")
        else:
            await interaction.response.send_message(f"Your key: '{key}' is incorrect. >:C  No verifying for you! :joy:")
    except Exception as e:
        await interaction.response.send_message(f"Failed to modify user: {e}")

@bot.tree.command(name="job_grant", description="Grant a member a role.")
@commands.is_owner()
async def job_grant(interaction: discord.Interaction, member: discord.Member, role_id: str, key: str):
    role = interaction.guild.get_role(int(role_id))
    user_id = str(member.id)
    if role:
        await member.add_roles(role)
        if user_id not in user_data:
            user_data[user_id] = {'Cash': 100, 'Health': 100, 'Stamina': 100, 'Job': 'Unemployed', 'Inv': {}, 'Key': key, 'Key-Fail': 0, 'Shifts-Worked': 0, 'Roles': [], 'Crime Score': 0, 'Bail': 0, 'NPC': {"Doctor": {"Progress": 0, "Relation": 0}, "Dave": 0}}
        user_data[user_id]['Job'] = role.name
        if role.name in bot_data:
            bot_data[role.name] += 1
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file, indent=4)
        with open('bot_data.json', 'w') as file:
            json.dump(bot_data, file, indent=4)
        await interaction.response.send_message(f'{member.mention} has been granted the role {role.name} and their job has been updated.')
    else:
        await interaction.response.send_message(f'Role with ID {role_id} not found.')

@bot.tree.command(name="transfer_cash", description="Transfer cash to another user.")
async def transfer_cash(interaction: discord.Interaction, member: discord.Member, amount: int, key: str):
    user_id = str(interaction.user.id)
    member_id = str(member.id)
    # Check if the key is correct
    if user_id in user_data:
        if "Key-Fail" in user_data[user_id]:
            if user_data[user_id]['Key-Fail'] < 3:
                if key == user_data[user_id]['Key']:
                    if amount <= user_data[user_id]['Cash']:
                        user_data[user_id]['Cash'] -= amount
                        user_data[member_id]['Cash'] += amount
                        await interaction.response.send_message(f"{amount} transferred to {member.nick}.", ephemeral=True)
                        await member.send(f"{interaction.user.nick} has sent you {amount} cash.")
                    else:
                        await interaction.response.send_message(f"You don't have enough cash to transfer {amount}.", ephemeral=True)
                else:
                    user_data[user_id]['Key-Fail'] += 1
                    await interaction.response.send_message(f"Wrong key, you have {3 - user_data[user_id]['Key-Fail']} attempts left.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Account locked. Transfers are now impossible.", ephemeral=True)
            with open('user_data.json', 'w') as file:
                json.dump(user_data, file, indent=4)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="use_item", description="Use a item in your inventory.")
async def use_item(interaction: discord.Interaction, item: str, quantity: str):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        if item in item_data or item_data['fauna']:
            if quantity.lower() == "max":
                quantity = round((100 - user_data[user_id]['Stamina']) / item_data[item]['Stamina'])
            else:
                try:
                    quantity = int(quantity)
                except ValueError:
                    await interaction.response.send_message(f"Please enter a valid number or max.", ephemeral=True)
                    return
            stam_gain = item_data[item]['Stamina'] * quantity
            if item in user_data[user_id]['Inv']:
                if quantity <= user_data[user_id]['Inv'][item]:
                    if user_data[user_id]['Stamina'] <= 100:
                        user_data[user_id]['Inv'][item] -= quantity
                        user_data[user_id]['Stamina'] += stam_gain
                        if user_data[user_id]['Inv'][item] == 0:
                            del user_data[user_id]['Inv'][item]
                        with open('user_data.json', 'w') as file:
                            json.dump(user_data, file, indent=4)
                        await interaction.response.send_message(f"Used {quantity} of {item}. Stamina is now {user_data[user_id]['Stamina']}")
                    else:
                        await interaction.response.send_message(f"You're not hungry. Don't eat out of sadness.\nAnd if you're trying to get rid of some items then just sell them!")
                else:
                    await interaction.response.send_message(f"You don't have enough {quantity} {item}(s).")
            else:
                await interaction.response.send_message(f"You don't have any {item}'s.")
        elif item in item_data['tools']:
            if item in user_data[user_id]['Inv']['tools']:
                if item == 'shovel':
                    chance = random.randint(1, 3)
                    if chance == 1:
                        dig = random.choice(["apple", "burger"])
                        if dig in user_data[user_id]['Inv']:
                            user_data[user_id]['Inv'][dig] += 1
                        else:
                            user_data[user_id]['Inv'][dig] = 1
                        await interaction.channel.send(f"{interaction.user.nick.capitalize()} dug for items and found a(n) {dig}! :grin:")
                    else:
                        await interaction.channel.send(f"{interaction.user.nick.capitalize()} tried digging for items, but they found naught, but dirt and stone. :pensive:")
                    if user_data[user_id]['Inv']['tools']['shovel'] > 1:
                        user_data[user_id]['Inv']['tools']['shovel'] -= 1
                        await interaction.response.send_message(f"Your shovel was damaged while digging. Remaining uses: {user_data[user_id]['Inv']['tools']['shovel']}", ephemeral=True)
                    else:
                        del user_data[user_id]['Inv']['tools']['shovel']
                        await interaction.response.send_message("Your shovel broke while digging. :pensive:", ephemeral=True)
                elif item == 'car battery':
                    chance = random.randint(1, 4)
                    health = random.randint(50, 100)
                    if chance == 1:
                        user_data[user_id]['Health'] += health
                        await interaction.response.send_message(f"What? How! You can't just zap yourself! Health: {user_data[user_id]['Health']}", ephemeral=True)
                    else:
                        if health > user_data[user_id]['Health']:
                            user_data[user_id]['Health'] = 0
                        else:
                            user_data[user_id]['Health'] -= health
                        await interaction.channel.send(f"{interaction.user.nick.capitalize()} tried healing with a car battery... :zap:")
                        await interaction.response.send_message(f"Lost: {health} health. Remaining Health: {user_data[user_id]['Health']}", ephemeral=True)
                    if user_data[user_id]['Inv']['tools']['car battery'] > 1:
                        user_data[user_id]['Inv']['tools']['car battery'] -= 1
                    else:
                        await interaction.user.send("Your car battery died. :pensive:")
                        del user_data[user_id]['Inv']['tools']['car battery']
                else:
                    await interaction.response.send_message(f"{item} doesn't exist. Why are you lying to me? Nevermind, you might've just mispelled. My bad.", ephemeral=True)
            else:
                await interaction.response.send_message(f"You dont have a {item}.")
        else:
            await interaction.response.send_message(f"{item} doesn't exist. Why are you lying to me? Nevermind, you might've just mispelled. My bad.", ephemeral=True)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system, Hacking.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification, Hacking.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")
    user_dump()

@bot.tree.command(name="sell_item", description="Sell a sellable item in your inventory. Write all/max to sell all of selected item.")
async def sell_item(interaction: discord.Interaction, item: str, quantity: str):
    user_id = str(interaction.user.id)
    if quantity == "all" or "max":
        quantity = user_data[user_id]['Inv'][item]
    else:
        try:
            quantity = int(quantity)
        except ValueError:
            interaction.response.send_message(f"Please enter a valid number or all/max.", ephemeral=True)
            return
    if user_id in user_data:
        if item in item_data:
            if item in user_data[user_id]['Inv']:
                value = (item_data[item]['Price']//2)
                gain = value * quantity
                if user_data[user_id]['Inv'][item] >= quantity:
                    user_data[user_id]['Inv'][item] -= quantity
                    user_data[user_id]['Cash'] += gain
                    await interaction.response.send_message(f"Sold {quantity} {item}(s) for {gain}.\nBalance: {user_data[user_id]['Cash']}")
                    if user_data[user_id]['Inv'][item] <= 0:
                        del user_data[user_id]['Inv'][item]
                    with open('user_data.json', 'w') as file:
                        json.dump(user_data, file, indent=4)
                else:
                    await interaction.response.send_message(f"You don't have {quantity} {item}(s).")
            else:
                await interaction.response.send_message(f"You don't have any {item}'s.")
        elif item in item_data['tools']:
            if item in user_data[user_id]['Inv']:
                value = (item_data['tools'][item]['Price']//2)
                gain = value * quantity
                if user_data[user_id]['Inv'][item] >= quantity:
                    user_data[user_id]['Inv'][item] -= quantity
                    user_data[user_id]['Cash'] += gain
                    await interaction.response.send_message(f"Sold {quantity} {item}(s) for {gain}.\nBalance: {user_data[user_id]['Cash']}")
                    if user_data[user_id]['Inv'][item] <= 0:
                        del user_data[user_id]['Inv'][item]
                    with open('user_data.json', 'w') as file:
                        json.dump(user_data, file, indent=4)
                else:
                    await interaction.response.send_message(f"You don't have {quantity} {item}(s).")
            else:
                await interaction.response.send_message(f"You don't have any {item}'s.")
        else:
            await interaction.response.send_message(f"{item} doesn't exsist. It's not real. You're imagining things. It's not like we migth've removed it, nooo, that's impossible.")
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="inventory", description="Lists item(s) in your inventory and the amount of them you have.")
async def inventory(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        inv_items = []
        tools_items = []
        fauna_items = []
        for item, quantity in user_data[user_id]['Inv'].items():
            if item == "tools":
                for name, amount in user_data[user_id]['Inv']['tools'].items():
                    for title, desc in item_data['tools'].items():
                        if name == title:
                            tools_items.append(f"{name.capitalize()}: {amount}, Value: {desc['Price']//2}\nDescription: {desc['desc']}")
            elif item == "fauna":
                for name, amount in user_data[user_id]['Inv']['fauna'].items():
                    for title, desc in item_data['fauna'].items():
                        if name == title:
                            fauna_items.append(f"{name.capitalize()}: {amount}, Stamina gain: {desc['Stamina']}, Value: {desc['Price']//2}\nDescription: {desc['desc']}")
            else:
                for thing, words in item_data.items():
                    if item == thing:
                        if thing != "tools":
                            if thing != "fauna":
                                inv_items.append(f"{item.capitalize()}: {quantity}, Stamina gain: {words['Stamina']}, Value: {words['Price']//2}\nDescription: {words['desc']}")
        
        if inv_items or tools_items or fauna_items:
            response_message = "**Inventory:\n**"
            if inv_items:
                item_list = "\n".join(inv_items)
                response_message += f"```\nCommon items:\n{item_list}```"
            if tools_items:
                tools_list = "\n".join(tools_items)
                response_message += f"```\nTools:\n{tools_list}```"
            if fauna_items:
                fauna_list = "\n".join(fauna_items)
                print(fauna_list)
                response_message += f"```\nFauna:\n{fauna_list}```"
            await interaction.response.send_message(response_message, ephemeral=True)
        else:
            await interaction.response.send_message("You don't have any items in your inventory.", ephemeral=True)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="job_list", description="See a list of all possible jobs.")
async def job_list(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        available_jobs = []
        for job, details in job_data.items():
            if (user_data[user_id]['Shifts-Worked'] >= details['Shift-Req']) and job != "unemployed":
                available_jobs.append(f"**{job}**: Pay: {details['Pay']}, Stamina: {details['Stam']}")
        if available_jobs:
            job_list = "\n".join(available_jobs)
            await interaction.response.send_message(f"Available jobs:\n{job_list}")
        else:
            await interaction.response.send_message("No jobs available based on your shifts worked.", ephemeral=True)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="job_apply", description="Apply for a job you meet the requirements for.")
async def job_apply(interaction: discord.Interaction, job: str):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        if job.lower() in job_data:
            if (user_data[user_id]['Shifts-Worked'] >= job_data[job]['Shift-Req']) and user_data[user_id]['Job'] == "unemployed":
                # Here! Fix job apply funciton
                bot_data[user_data[user_id]['Job']] -= 1
                user_data[user_id]['Job'] = job
                bot_data[job] += 1
                await interaction.response.send_message(f"You are now a {job}!")
                with open('user_data.json', 'w') as file:
                    json.dump(user_data, file, indent=4)
                with open('bot_data.json', 'w') as file:
                    json.dump(bot_data, file, indent=4)
            elif user_data[user_id]['Job'] == job:
                await interaction.response.send_message(f"You are already a {job}.")
            elif user_data[user_id]['Job'] != "unemployed":
                await interaction.response.send_message(f"You can't apply to another job before quitting your current one.")
            else:
                await interaction.response.send_message(f"You don't meet the necessary requirements to apply to this job. Req: {job['Shift-Req']}")
        else:
            await interaction.response.send_message(f"{job.capitalize()} does not exist.")
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="job_resign", description="Resign from your job.")
async def job_resign(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        bot_data[user_data[user_id]['Job']] -= 1
        await interaction.response.send_message(f"You have resigned from your position as a {user_data[user_id]['Job']}. You are now Unemployed! Congrats :grin:")
        user_data[user_id]['Job'] = "unemployed"
        bot_data[user_data[user_id]['Job']] += 1
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file, indent=4)
        with open('bot_data.json', 'w') as file:
            json.dump(bot_data, file, indent=4)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="greetings", description="Greet dave!")
async def greetings(interaction: discord.Interaction):
    iview = MyView(add_hows_your_day=True, add_bye=True)
    await interaction.response.send_message("Hi, did you need anything?", view=iview)

@bot.tree.command(name="bank", description="Manage your bank account.")
@app_commands.describe(action="Select an option.")
@app_commands.choices(action=[
    app_commands.Choice(name="Deposit", value="D"),
    app_commands.Choice(name="Withdraw", value="W"),
    app_commands.Choice(name="Balance", value="B")
])
async def bank(interaction: discord.Interaction, action: str):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        if action == "D":
            await interaction.response.send_message("How much would you like to deposit?")
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()
            try:
                msg = await bot.wait_for('message', check=check, timeout=30.0)
                number = int(msg.content)
                if user_data[user_id]['Cash'] >= number:
                    await interaction.followup.send(f"Deposited {number} to bank.")
                    user_data[user_id]['Bank'] += number
                    user_data[user_id]['Cash'] -= number
                else:
                    await interaction.followup.send(f"You aint got that much. :pensive:")
            except asyncio.TimeoutError:
                await interaction.followup.send("Slow ass! You took too long. :rage:")
        elif action == "W":
            await interaction.response.send_message("How much would you like to Withdraw?")
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()
            try:
                msg = await bot.wait_for('message', check=check, timeout=30.0)
                number = int(msg.content)
                if user_data[user_id]['Bank'] >= number:
                    await interaction.followup.send(f"Withdrawn {number} to bank.")
                    user_data[user_id]['Cash'] += number
                    user_data[user_id]['Bank'] -= number
                else:
                    await interaction.followup.send(f"You aint got that much. :pensive:")
            except asyncio.TimeoutError:
                await interaction.followup.send("Slow ass! You took too long. :rage:")
        elif action == "B":
            await interaction.response.send_message(f"You currently have {user_data[user_id]['Bank']} in your bank.")
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

@bot.tree.command(name="kill_self", description="Give up.")
async def kill_self(interaction: discord.Interaction, key: str):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        if user_data[user_id]['Key'] == key:
            await interaction.response.send_message(f"Are you sure? You can never go back.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                msg = await bot.wait_for('message', check=check, timeout=30.0)
                answer = msg.content
                if answer.lower() == "yes":
                    try:
                        await interaction.user.kick(reason="You have died.")
                        await interaction.channel.send(f"Today {interaction.user.nick} committed suecide. May he never be forgotten.")
                        del user_data[user_id]
                    except discord.Forbidden:
                        await interaction.response.send_message(f"You failed. You've become too powerfull to die from suecide...")
            except asyncio.TimeoutError:
                await interaction.followup.send("Slow ass! You took too long. :rage:")
        else:
            await interaction.response.send_message(f"Wrong key bozo.", ephemeral=True)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)
    
@bot.tree.command(name="rob", description="Rob another user.")
async def rob(interaction: discord.Interaction, member: discord.Member):
    user_id = str(interaction.user.id)
    rob_id = str(member.id)
    if user_id in user_data:
        if rob_id in user_data:
            chance = random.randint(1, 6)
            if "Rob-Cooldown" in user_data[user_id]:
                if user_data[user_id]['cooldowns']['Rob-Cooldown'] > 0:
                    await interaction.response.send_message(f"You can rob someone again <t:{int(time.time())+user_data[user_id]['Rob-Cooldown']}:R>")
                    return
                else:
                    user_data[user_id]['cooldowns']['Rob-Cooldown'] = 600
            else:
                user_data[user_id]['cooldowns']['Rob-Cooldown'] = 600
            if chance == 1:
                if user_data[rob_id]['Cash'] > 0:
                    amount = random.randint(1, user_data[rob_id]['Cash'])
                    await interaction.response.send_message(f"You robbed {member.nick} for {amount} cash.", ephemeral=True)
                    user_data[user_id]['Cash'] += amount
                    user_data[rob_id]['Cash'] -= amount
                    await member.send(f"{interaction.user} has robbed you for {amount} cash. You now have {user_data[rob_id]['Cash']} cash left.")
                    while user_data[user_id]['cooldowns']['Rob-Cooldown'] > 0:
                        await asyncio.sleep(1)
                        user_data[user_id]['cooldowns']['Rob-Cooldown'] -= 1
                        user_dump()
                else:
                    await interaction.response.send_message(f"They were too poor to rob. Completely empty pockets. :pensive:", ephemeral=True)
            elif chance == 3:
                if user_data[rob_id]['Cash'] > 0:
                    amount = random.randint(1, user_data[rob_id]['Cash'])
                    await interaction.response.send_message(f"You robbed {member.nick} for {amount} cash. You were stealthy enough so that {member.nick} didn't find out you robbed them.", ephemeral=True)
                    user_data[user_id]['Cash'] += amount
                    user_data[rob_id]['Cash'] -= amount
                    while user_data[user_id]['cooldowns']['Rob-Cooldown'] > 0:
                        await asyncio.sleep(1)
                        user_data[user_id]['cooldowns']['Rob-Cooldown'] -= 1
                        user_dump()
                else:
                    await interaction.response.send_message(f"They were too poor to rob. Completely empty pockets. :pensive:", ephemeral=True)
            else:
                user_data[user_id]['Crime Score'] += 1
                if (user_data[user_id]['Crime Score']*10) <= user_data[user_id]['Cash']:
                    amount = random.randint((user_data[user_id]['Crime Score']*10), user_data[user_id]['Cash'])
                else:
                    amount = user_data[user_id]['Cash']
                user_data[rob_id]['Cash'] += amount//2
                user_data[user_id]['Cash'] -= amount
                jail_time = 120*user_data[user_id]['Crime Score']
                if interaction.user.id == interaction.guild.owner_id:
                    await interaction.response.send_message(f"Can't arrest :pensive: Damned dictator!")
                    await interaction.channel.send(f"{interaction.user.mention} has been fined {amount} for the attempted theft on {member.nick}.")
                    await member.send()(f"You have been given {amount//2} as compensation for {interaction.user.nick}'s attempted robbery of your cash. Keep your pockets safe.")
                else:
                    await interaction.channel.send(f"{interaction.user.mention} was arrested for attempted theft. They have been fined {amount}. {member.nick} has been given compensation.")
                    await member.send(f"You have been given {amount//2} as compensation for {interaction.user.nick}'s attempted robbery of your cash. Keep your pockets safe.")
                    await interaction.response.send_message(f"You tried to rob {member.nick}, but you were caught. Have fun in jail I guess. :slight_smile: Jail time: <t:{int(time.time())+jail_time}:R>", ephemeral=True)
                    jail = discord.utils.get(member.guild.roles, id=1307363196448931850)
                    roles = interaction.user.roles[1:]
                    role_ids = [role.id for role in roles]
                    user_data[user_id]['Roles'] += role_ids
                    with open('user_data.json', 'w') as file:
                        json.dump(user_data, file, indent=4)
                    user_data[user_id]['Bail'] += 50 * user_data[user_id]['Crime Score']
                    await interaction.user.remove_roles(*roles)
                    await interaction.user.add_roles(jail)
                    user_data[user_id]['cooldowns']['Jail-Time'] = jail_time
                    while user_data[user_id]['cooldowns']['Jail-Time'] > 0:
                        await asyncio.sleep(1)
                        user_data[user_id]['cooldowns']['Jail-Time'] -= 1
                        user_dump()
                    updated_user = await interaction.guild.fetch_member(interaction.user.id)
                    if jail in updated_user.roles:
                        await interaction.user.remove_roles(jail)
                        await interaction.user.add_roles(*roles)
                        user_data[user_id]['Crime Score'] = 0
                        user_data[user_id]['Bail'] = 0
                        user_data[user_id]['Roles'].clear()
                        await interaction.channel.send(f"{interaction.user.mention} is no longer in jail.")
                    else:
                        await interaction.response.send_message(f"You got out? But how...", ephemeral=True)
        else:
            await interaction.response.send_message(f"This user hasn't been registered. Essentially, they're poor.", ephemeral=True)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")
    user_dump()
    bot_dump()

@bot.tree.command(name="jail", description="Go to jail and do stuff.")
@app_commands.describe(action="Choose an option.")
@app_commands.choices(action=[
    app_commands.Choice(name="Jailbreak", value="J"),
    app_commands.Choice(name="Bail", value="B"),
    app_commands.Choice(name="Turn yourself in", value="T"),
    app_commands.Choice(name="Leave", value="L")
])
async def jail(interaction: discord.Interaction, action: str):
    user_id = str(interaction.user.id)
    jail_role = interaction.guild.get_role(1307363196448931850)

    async def jailbreak_callback(interaction: discord.Interaction, selected_member: discord.Member):
        role_ids = user_data[str(selected_member.id)]['Roles']
        roles = [interaction.guild.get_role(role_id) for role_id in role_ids if interaction.guild.get_role(role_id) is not None]
        if action == "J":
            if random.randint(1, 3) == 1:  # 1/3 chance of success
                await selected_member.remove_roles(jail_role)
                await selected_member.add_roles(*roles)
                user_data[str(selected_member.id)]['Roles'].clear()
                user_dump()
                await interaction.response.send_message(f"{selected_member.nick} has been successfully jailbroken!", ephemeral=True)
            else:
                await interaction.user.add_roles(jail_role)
                await interaction.user.remove_roles(*roles)
                user_data[user_id]['Crime Score'] += 2
                user_data[user_id]['Bail'] += 50*user_data[user_id]['Crime Score']
                await interaction.response.send_message(f"Jailbreak failed! {interaction.user.nick} is now in jail.")
                user_data[user_id]['Jail-Time'] = 120*user_data[user_id]['Crime Score']
                while user_data[user_id]['cooldowns']['Jail-Time'] > 0:
                    await asyncio.sleep(1)
                    user_data[user_id]['cooldowns']['Jail-Time'] -= 1
                    user_dump()
                updated_user = await interaction.guild.fetch_member(interaction.user.id)
                if jail_role not in updated_user.roles:
                    await interaction.response.send_message(f"Imagine not serving your sentence. Kinda cringe not gonna lie.", ephemeral=True)
                else:
                    await interaction.user.remove_roles(jail_role)
                    await interaction.user.add_roles(*roles)
                    role_ids.clear()
                user_dump()
        elif action == "B":
            if user_data[user_id]['Cash'] >= user_data[str(selected_member.id)]['Crime Score']:
                await selected_member.remove_roles(jail_role)
                await selected_member.add_roles(*roles)
                user_data[user_id]['Cash'] -= user_data[str(selected_member.id)]['Bail']
                user_data[str(selected_member.id)]['Bail'] -= user_data[str(selected_member.id)]['Bail']
                user_data[str(selected_member.id)]['Roles'].clear()
                user_dump()
                await interaction.channel.send(f"{selected_member.nick} has been bailed out of jail.")
                await selected_member.send(f"{interaction.user.nick} bailed you out of jail.")
            else:
                await interaction.response.send_message(f"You don't have enough cash to bail out {selected_member.nick}. Bail: {user_data[str(selected_member.id)]['Bail']}")
                
    if user_id in user_data:
        if action == "J":
            members_with_role = [member for member in interaction.guild.members if jail_role in member.roles]
            if not members_with_role:
                await interaction.response.send_message("No members found with that role.", ephemeral=True)
                return

            view = MemberView(members_with_role, jailbreak_callback)
            await interaction.response.send_message("Select a member:", view=view, ephemeral=True)
        elif action == "B":
            members_with_role = [member for member in interaction.guild.members if jail_role in member.roles]
            if not members_with_role:
                await interaction.response.send_message("No members found with that role.", ephemeral=True)
                return

            view = MemberView(members_with_role, jailbreak_callback)
            await interaction.response.send_message("Select a member:", view=view, ephemeral=True)
        elif action == "T":
            jail_time = 60*user_data[user_id]['Crime Score']
            if interaction.user.id == interaction.guild.owner_id:
                await interaction.response.send_message(f"You literally own me. Here, you are no longer wanted. Couldn't you just do this yourself? Jesus.")
                user_data[user_id]['Bail'] -= user_data[user_id]['Bail']
                user_data[user_id]['Roles'].clear()
                user_data[user_id]['Crime Score'] = 0
                user_dump()
            else:
                role = interaction.user.roles[1:]
                role_ids = [role.id for role in role]
                user_data[user_id]['Roles'] += role_ids
                await interaction.user.add_roles(jail_role)
                await interaction.user.remove_roles(*role)
                await interaction.response.send_message(f"You turned yourself in. The police halved your sentence time since you turned yourself in willingly. You need to stay in jail for {jail_time/60} minutes. Released <t:{int(time.time())+jail_time}:R>")
                user_dump()
                user_data[user_id]['cooldowns']['Jail-Time'] = jail_time
                while user_data[user_id]['cooldowns']['Jail-Time'] > 0:
                    await asyncio.sleep(1)
                    user_data[user_id]['cooldowns']['Jail-Time'] -= 1
                    user_dump()
                await interaction.followup.send(f"Releasing {interaction.user.nick} from jail...")
                updated_user = await interaction.guild.fetch_member(interaction.user.id)
                if jail_role in updated_user.roles:
                    await interaction.user.send(f"You are no longer in jail. Your crime score is now zero and you are no longer wanted.")
                    await interaction.user.remove_roles(jail_role)
                    await interaction.user.add_roles(*role)
                    user_data[user_id]['Crime Score'] = 0
                    user_data[user_id]['Bail'] = 0
                    role_ids.clear()
                    user_dump()
                else:
                    await interaction.user.send(f"Bro didn't serve his sentence :pensive: How disappointing.")
        elif action == "L":
            await interaction.response.send_message("Leaving jail action selected.", ephemeral=True)
        else:
            await interaction.response.send_message(f"I don't know what you're trying to do here, but I'd recommend against it.", ephemeral=True)
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

@bot.tree.command(name="attack", description="Attack another user. Why? I don't know, ask yourself.")
@app_commands.describe(action="Choose an option...")
@app_commands.choices(action=[
    app_commands.Choice(name="Punch", value="P"),
    app_commands.Choice(name="Kick", value="K"),
    app_commands.Choice(name="Assault", value="A"),
    app_commands.Choice(name="Nevermind", value="N")
])
async def attack(inter: discord.Interaction, member: discord.Member, action: str):
    user_id = str(inter.user.id)
    attack_id = str(member.id)
    reaction = ["toe", "knee", "face", "stomach", "finger", "leg"]
    if user_id in user_data:
        if member.id != inter.guild.owner_id:
            if action == "P":
                att_dam = random.randint(0, 10)
                att_hit = random.randint(1, 3)
                if att_hit == 1 or 2:
                    user_data[attack_id]['Health'] -= att_dam
                    user_data[user_id]['Crime Score'] += 1
                    await inter.channel.send(f"{inter.user.nick} punched {member.mention} in their {random.choice(reaction)} and dealt {att_dam}.")
                    await member.send(f"{inter.user.nick} punched you in your {random.choice(reaction)} dealing {att_dam}. Health is now {user_data[attack_id]['Health']}")
                    await inter.response.send_message(f"Your crime score went up by 1 point.", ephemeral=True)
                else:
                    user_data[user_id]['Health'] -= att_dam//2
                    user_data[user_id]['Crime Score'] += 1
                    await inter.response.send_message(f"You tried attacking {member.nick}, but they pushed you over dealing {att_dam//2}. Crime score went up by 1 point.", ephemeral=True)
                    await member.send(f"{inter.user} tried punching you, but you pushed them over and got away.")
            elif action == "K":
                att_dam = random.randint(0, 20)
                att_hit = random.randint(1, 2)
                if att_hit == 1:
                    user_data[attack_id]['Health'] -= att_dam
                    user_data[user_id]['Crime Score'] += 1
                    await inter.channel.send(f"{inter.user.nick} kicked {member.mention} in the {random.choice(reaction)} and dealt {att_dam}.")
                    await member.send(f"{inter.user.nick} kicked you in your {random.choice(reaction)} dealing {att_dam}. Health is now {user_data[attack_id]['Health']}")
                    await inter.response.send_message(f"Your crime score went up by 1 point.", ephemeral=True)
                else:
                    user_data[user_id]['Health'] -= att_dam//2
                    user_data[user_id]['Crime Score'] += 1
                    await inter.response.send_message(f"You tried kicking {member.nick}, but they tripped you dealing {att_dam//2}. Crime score went up by 1 point.", ephemeral=True)
                    await member.send(f"{inter.user} tried kicking you, but you tripped them and got away.")
            elif action == "A":
                success = random.randint(1, 5)
                att_dam = random.randint(15, 35)
                if success == 1:
                    user_data[attack_id]['Health'] -= att_dam//1.5
                    user_data[user_id]['Crime Score'] += 3
                    await inter.channel.send(f"{inter.user.nick} assaulted {member.mention} and dealt {att_dam}.")
                    await member.send(f"{inter.user.nick} assaulted you dealing {att_dam}. Health is now {user_data[attack_id]['Health']}")
                    await inter.response.send_message(f"Your crime score went up by 3 points.", ephemeral=True)
                elif success == 2:
                    user_data[attack_id]['Health'] -= att_dam//2
                    user_data[user_id]['Crime Score'] += 3
                    await inter.channel.send(f"{inter.user.nick} tried assaulting {member.mention}, but {member.nick} noticed. {inter.user.nick} scratched {member.nick}'s {random.choice(reaction)} dealing {att_dam//1.5}")
                    await inter.response.send_message(f"Your crime score went up by 3 points.", ephemeral=True)
                else:
                    user_data[user_id]['Health'] -= att_dam//2
                    user_data[user_id]['Crime Score'] += 2
                    await inter.channel.send(f"{inter.user.nick} tried assaulting {member.nick}, but {member.nick} kicked {inter.user.nick} in the {random.choice(reaction)}.")
                    await inter.response.send_message(f"Your crime score went up by 2 points.", ephemeral=True)
                    await member.send(f"{inter.user.nick} tried assaulting you, but you kicked them in the {random.choice(reaction)}")
            elif action == "N":
                await inter.response.send_message(f"You decided not to attack {member.nick} after all. How nice of you :smile:", ephemeral=True)
            else:
                await inter.response.send_message(f"I don't know how you did that, but thats not an option. It might become one, but now it's not an option.", ephemeral=True)
        else:
            att_dam = random.randint(20, 50)
            if inter.user.id != inter.guild.owner_id:
                if user_data[user_id]['Health'] >= att_dam:
                    user_data[user_id]['Health'] -= att_dam
                else:
                    att_dam = user_data[user_id]['Health']
                    user_data[user_id]['Health'] = 0
                await inter.response.send_message(f"You tried attacking {member.nick}, but his guards tackled you. You took {att_dam} damage. Health: {user_data[user_id]['Health']}", ephemeral=True)
            else:
                await inter.response.send_message(f"Koko... :pensive: You have more to live for than you know...", ephemeral=True)
        bot_dump()
        user_dump()
    else: 
        try:
            await inter.user.kick(reason="Bypassing verification system.")
            await inter.response.send_message(f"{inter.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await inter.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {inter.user.nick.capitalize()} is admin;")
  
@bot.tree.command(name="hospital", description="Go to the hospital.")
@app_commands.describe(action="Do something...")
@app_commands.choices(action=[
    app_commands.Choice(name="Heal", value="H"),
    app_commands.Choice(name="Visit", value="V"),
    app_commands.Choice(name="Leave", value="L")
])
async def hospital(inter: discord.Interaction, action: str):
    user_id = str(inter.user.id)
    hospital_role = inter.guild.get_role(1308730447387164702)
    if user_id in user_data:
        if action == "H":
            if user_data[user_id]['Health'] < 100:
                heal_time = (100-user_data[user_id]['Health'])*30
                await inter.response.send_message(f"You wont be able to use any commands while hospitalized. Are you sure you want to heal yourself? Say 'yes' in this channel if you wish to heal. Heal time: <t:{int(time.time())+heal_time}:R>")
                def check(m):
                    return m.author == inter.user and m.channel == inter.channel
                try:
                    msg = await bot.wait_for('message', check=check, timeout=30.0)
                    answer = msg.content
                    if answer.lower() == "yes":
                        role = inter.user.roles[1:]
                        role_ids = [role.id for role in role]
                        user_data[user_id]['Roles'] += role_ids
                        await inter.user.add_roles(hospital_role)
                        await inter.user.remove_roles(*role)
                        user_dump()
                        user_data[user_id]['cooldowns']['Heal-Time'] = heal_time
                        while user_data[user_id]['cooldowns']['Heal-Time'] > 0:
                            await asyncio.sleep(1)
                            user_data[user_id]['cooldowns']['Heal-Time'] -= 1
                            user_dump()
                        updated_user = await inter.guild.fetch_member(inter.user.id)
                        if hospital_role in updated_user.roles:
                            user_data[user_id]['Health'] = 150
                            await inter.user.add_roles(*role)
                            await inter.user.remove_roles(hospital_role)
                            user_data[user_id]['Roles'].clear()
                            await inter.user.send(f"You are no longer in the hospital.")
                except asyncio.TimeoutError:
                    await inter.followup.send("You didn't answer in time.")
            else:
                await inter.response.send_message("The doctor told you to leave as your're in perfect shape.", ephemeral=True)
        elif action == "V":
            view = MyOptions()
            await inter.response.send_message("You visit the hospital. What do you do?", view=view, ephemeral=True)
        elif action == "L":
            await inter.response.send_message(f"You left the hospital.")
    else:
        try:
            await inter.user.kick(reason="Bypassing verification system.")
            await inter.response.send_message(f"{inter.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await inter.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {inter.user.nick.capitalize()} is admin;")
    bot_dump()
    user_dump()

@bot.tree.command(name="blackjack", description="Blackjack")
async def play_cards(inter: discord.Interaction):
    user_id = str(inter.user.id)
    if user_id in user_data:
        deck = cards.copy()
        random.shuffle(deck)
        user_hand = [deck.pop(), deck.pop()]
        bot_hand = [deck.pop(), deck.pop()]
        card_value = {"Ace": 11, "King": 10, "Queen": 10, "Jack": 10, "Ten": 10, "Nine": 9, "Eight": 8, "Seven": 7, "Six": 6, "Five": 5, "Four": 4, "Three": 3, "Two": 2}
        view = CardGame(user_hand, bot_hand, deck, card_value, True)
        await inter.response.send_message(f"Your hand: {user_hand} (value: {calculate_hand_value(user_hand, card_value)})\nBot's hand: {bot_hand[0]} and a hidden card", view=view)           
    else:
        try:
            await inter.user.kick(reason="Bypassing verification system.")
            await inter.response.send_message(f"{inter.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await inter.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {inter.user.nick.capitalize()} is admin;")

@bot.tree.command(name="gather", description="Gather resources and items by using tools.")
@app_commands.describe(tool="Choose a tool...")
@app_commands.choices(tool = [
    app_commands.Choice(name="Fish", value="F"),
    app_commands.Choice(name="Hunt", value="H"),
    app_commands.Choice(name="Search", value="S")
])
async def gather(inter: discord.Interaction, tool: str):
    user_id = str(inter.user.id)
    if user_id in user_data:
        if tool == "F":
            if "fishing rod" in user_data[user_id]['Inv']['tools']:
                if "Fish-Cooldown" in user_data[user_id]['cooldowns']:
                    if user_data[user_id]['cooldowns']['Fish-Cooldown'] > 0:
                        await inter.response.send_message(f"You can fish again <t:{int(time.time())+user_data[user_id]['cooldowns']['Fish-Cooldown']}:R>")
                        return
                    else:
                        user_data[user_id]['cooldowns']['Fish-Cooldown'] = 1800
                else:
                    user_data[user_id]['cooldowns']['Fish-Cooldown'] = 1800
                user_dump()
                chance = random.randint(1,2,3)
                fish_list = ["fibsh", "carp", "red coat", "salmon", "flounder"]
                weight = [1, 20, 10, 20, 5]
                if chance in [1,3]:
                    quality = random.randint(1, 10)
                    fish = random.choices(fish_list, weights=weight, k=1)[0]
                    if fish in user_data[user_id]['Inv']['fauna']:
                        user_data[user_id]['Inv']['fauna'][fish] += 1
                    else:
                        user_data[user_id]['Inv']['fauna'][fish] = 1
                    await inter.response.send_message(f"You caught a {fish}!")
                    if user_data[user_id]['Inv']['tools']['fishing rod'] > 0:
                        user_data[user_id]['Inv']['tools']['fishing rod'] -= 1
                    else:
                        del user_data[user_id]['Inv']['tools']['fishing rod']
                    user_dump
                    while user_data[user_id]['cooldowns']['Fish-Cooldown'] > 0:
                        await asyncio.sleep(1)
                        user_data[user_id]['cooldowns']['Fish-Cooldown'] -= 1
                        user_dump
                else:
                    await inter.response.send_message("You didn't catch anything...")
            else:
                await inter.response.send_message("You don't have a fishing rod.")
                return
        elif tool == "H":
            if "hunting rifle" in user_data[user_id]['Inv']['tools']:
                if "Hunt-Cooldown" in user_data[user_id]['cooldowns']:
                    if user_data[user_id]['cooldowns']['Hunt-Cooldown'] > 0:
                        await inter.response.send_message(f"You can hunt again <t:{int(time.time())+user_data[user_id]['cooldowns']['Hunt-Cooldown']}:R>")
                        return
                    else:
                        user_data[user_id]['cooldowns']['Hunt-Cooldown'] = 1800
                else:
                    user_data[user_id]['cooldowns']['Hunt-Cooldown'] = 1800
                chance = random.randint(1, 3)
                if chance in [1, 2]:
                    if "deer" in user_data[user_id]['Inv']['fauna']:
                        user_data[user_id]['Inv']['fauna']['deer'] += 1
                    else:
                        user_data[user_id]['Inv']['fauna']['deer'] = 1
                    await inter.response.send_message("You caught one deer!", ephemeral=True)
                    user_dump()
                else:
                    await inter.response.send_message("You didn't find any deer.", ephemeral=True)
                while user_data[user_id]['cooldowns']['Hunt-Cooldown'] > 0:
                    user_data[user_id]['cooldowns']['Hunt-Cooldown'] -= 1
                    await asyncio.sleep(1)
                    user_dump()
            else:
                await inter.response.send_message("You don't have a hunting rifle to hunt with.", ephemeral=True)
                return
        elif tool == "S":
            if "Search-Cooldown" in user_data[user_id]['cooldowns']:
                if user_data[user_id]['cooldowns']['Search-Cooldown'] > 0:
                    await inter.response.send_message(f"You can search again <t:{int(time.time())+user_data[user_id]['cooldowns']['Search-Cooldown']}:R>")
                    return
                else:
                    user_data[user_id]['cooldowns']['Search-Cooldown'] = 1800
            else:
                user_data[user_id]['cooldowns']['Search-Cooldown'] = 1800
            user_dump()
            chance = random.randint(1,4)
            if chance in [1, 2, 3, 4]:
                qual = random.randint(1,5)
                if qual in [1, 2]:
                    items = ["medkit", "hunting rifle"]
                    weights = [1, 1]
                    quality = random.choices(items, weights=weights, k=1)
                    item = quality.pop()
                    user_data[user_id]['Inv']['tools'][item] = 10
                elif qual in [3, 4, 5]:
                    items = ["car battery", "shovel", "burger", "apple"]
                    weights = [1, 1, 2, 5]
                    quality = random.choices(items, weights=weights, k=1)
                    item = quality.pop()
                    if item in ["car battery", "shovel"]:
                        user_data[user_id]['Inv']['tools'][item] = 10
                    elif item in user_data[user_id]['Inv']:
                        user_data[user_id]['Inv'][item] += 1
                    else:
                        user_data[user_id]['Inv'][item] = 1

                await inter.response.send_message(f"You found a {item}!")
            else:
                await inter.response.send_message("You found... air!")
                user_dump()
            while user_data[user_id]['cooldowns']['Search-Cooldown'] > 0:
                await asyncio.sleep(1)
                user_data[user_id]['cooldowns']['Search-Cooldown'] -= 1
                user_dump()
    else:
        try:
            await inter.user.kick(reason="Bypassing verification system.")
            await inter.response.send_message(f"{inter.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await inter.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {inter.user.nick.capitalize()} is admin;")

@bot.tree.command(name="coinflip", description="Flip a coin. Casual=No bet, Competetive=Bet")
@app_commands.describe(action="...")
@app_commands.choices(action = [
    app_commands.Choice(name="Competetive", value="Co"),
    app_commands.Choice(name="Casual", value="C")
])
async def coinflip(inter: discord.Interaction, action: str, bet_on: str = "", bet: int = 0):
    user_id = str(inter.user.id)
    pos = ["Heads", "Tails"]
    result = random.choice(pos)
    if user_id in user_data:
        if action == "Co":
            if result == bet_on:
                await inter.response.send_message(f"{result}. You win!")
                user_data[user_id]['Cash'] += bet
                user_dump()
            else:
                await inter.response.send_message(f"{result}. You lost.")
                user_data[user_id]['Cash'] -= bet
                user_dump()
        elif action == "C":
            await inter.response.send_message(f"{result}.")
    else:
        try:
            await inter.user.kick(reason="Bypassing verification system.")
            await inter.response.send_message(f"{inter.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await inter.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {inter.user.nick.capitalize()} is admin;")

@bot.tree.command(name="locations", description="Travel around.")
@app_commands.describe(loc="...")
@app_commands.choices(loc = [
    app_commands.Choice(name="Town", value="T"),
    app_commands.Choice(name="Forest", value="F"),
    app_commands.Choice(name="Koko Economy Central", value="K")
])
async def locations(inter: discord.Interaction, loc: str):
    user_id = str(inter.user.id)
    view1 = locView(loc=loc)
    if user_id in user_data:
        if loc == "T":
            await inter.response.send_message("You went into town. There is many people around. It's quite loud not going to lie.", view=view1)
        elif loc == "F":
            await inter.response.send_message("You went into the forest. Not many people around, but it's very peacefull.", view=view1)
        elif loc == "K":
            await inter.response.send_message("You went to the Koko Economy Central... Why? Theres nothing to do here...", view=view1)
    else:
        try:
            await inter.user.kick(reason="Bypassing verification system.")
            await inter.response.send_message(f"{inter.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await inter.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {inter.user.nick.capitalize()} is admin;")


@bot.command(name='shutdown')
@commands.has_any_role('Koko The Economist', 'Tax Advisors')
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    print("Shutting down...")
    channel = bot.get_channel(1318187395807707147)
    if channel:
        await channel.purge()
        await channel.send('> # Bot Status: **Inactive**')
    await bot.close()

bot.run(token)