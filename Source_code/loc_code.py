import discord
from discord.ui import View, Select
import os
import json
import random
import asyncio
from dotenv import load_dotenv

load_dotenv()

if os.path.exists('user_data.json'):
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

def user_dump():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

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