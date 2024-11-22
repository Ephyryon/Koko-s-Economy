import discord
from discord import app_commands
from discord.ui import View, Button
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

class MyModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Input Modal")
        self.text_input = discord.ui.TextInput(label="Enter your text", style=discord.TextStyle.short)
        self.add_item(self.text_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You entered: {self.text_input.value}")

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

@bot.event
async def on_ready():
    clear_channel.start()
    on_health_zero_task.start()
    print(f"Logged in as {bot.user}")
    print(f"GUILD_ID: {guild_id}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

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
                await member.remove_roles(*roles)
                await member.add_roles(hospital_role)
                await member.send(f"You have been hospitalized. Time: 50 minutes.")
                await asyncio.sleep(3000)
                await member.remove_roles(hospital_role)
                await member.add_roles(*roles)
                user_data[str(member.id)]['Health'] = 150
                user_dump()
                await member.send(f"You are no longer hospitalized.")

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

@bot.tree.command(name="work", description="Earn cash by working")
async def work(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_data:
        job_name = user_data[user_id]['Job']
        if user_data[user_id]['Stamina'] >= job_data[job_name]['Stam']:
            current_time = time.time()
            cooldown_time = job_data[job_name]['Work-Cooldown']
            if user_id in cooldowns:
                elapsed_time = current_time - cooldowns[user_id]
                if elapsed_time < cooldown_time:
                    remaining_time = cooldown_time - elapsed_time
                    await interaction.response.send_message(f'{interaction.user.mention}, you need to wait {int(remaining_time)} seconds before using this command again.')
                    return
            cooldowns[user_id] = current_time
            if job_name in job_data:
                pay = job_data[job_name]['Pay']
                stam = job_data[job_name]['Stam']
                user_data[user_id]['Cash'] += pay
                user_data[user_id]['Stamina'] -= stam
                user_data[user_id]['Shifts-Worked'] += 1
                with open('user_data.json', 'w') as file:
                    json.dump(user_data, file, indent=4)
                await interaction.response.send_message(f'{interaction.user.mention}, you worked as a {job_name} and earned {pay} cash! You now have {user_data[user_id]["Cash"]} cash.')
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
        await interaction.response.send_message(f'{interaction.user.mention}, your stats are: Cash: {stats["Cash"]}, Health: {stats["Health"]}, Stamina: {stats["Stamina"]}, Job: {stats["Job"]}')
    else:
        try:
            await interaction.user.kick(reason="Bypassing verification system.")
            await interaction.response.send_message(f"{interaction.user.nick.capitalize()} has been kicked for bypassing verification.")
        except discord.Forbidden:
            await interaction.response.send_message(f"CommandError: user not in registry: user not verified; KickFail: PermissionError: {interaction.user.nick.capitalize()} is admin;")

@bot.tree.command(name="shop_view", description="View items in shop.")
async def shop_view(interaction: discord.Interaction):
    shop_message = "Items available in the shop:\n"
    for item, attributes in item_data.items():
        try:
            price = attributes["Price"]
            stamina = attributes["Stamina"]
            shop_message += f"{item.capitalize()}: {{Stamina: {stamina}, Price: {price}}}\n"
        except KeyError:
            for item, attributes in item_data['tools'].items():
                try:
                    dur = attributes["dur"]
                    price = attributes["Price"]
                    shop_message += f"{item.capitalize()}: {{Durability: {dur}, Price: {price}}}\n"
                except KeyError:
                    None
    
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
            user_data[user_id] = {'Cash': 100, 'Health': 100, 'Stamina': 100, 'Job': 'Unemployed', 'Inv': {"tools": {}}, 'Key': key, 'Key-Fail': 0, 'Shifts-Worked': 0, 'Roles': {}}
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
            user_data[user_id] = {'Cash': 100, 'Health': 100, 'Stamina': 100, 'Job': 'Unemployed', 'Inv': {}, 'Key': key, 'Key-Fail': 0, 'Shifts-Worked': 0, 'Roles': {}}
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
        if item in item_data:
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
        for item, quantity in user_data[user_id]['Inv'].items():
            if item != "tools":
                for thing, words in item_data.items():
                    if thing in user_data[user_id]['Inv']:
                        if thing != "tools":
                            if item == thing:
                                inv_items.append(f"{item.capitalize()}: {quantity}, Stamina gain: {words['Stamina']}, Value: {words['Price']//2}\nDescription: {words['desc']}")
            else:
                for name, amount in user_data[user_id]['Inv']['tools'].items():
                    for title, desc in item_data['tools'].items():
                        if title in user_data[user_id]['Inv']['tools']:
                            if name == title:
                                tools_items.append(f"{name.capitalize()}: {amount}, Value: {desc['Price']//2}, Description: {desc['desc']}")
        
        if inv_items or tools_items:
            item_list = "\n".join(inv_items)
            tools_list = "\n".join(tools_items)
            response_message = "**Inventory:\n**"
            if item_list:
                response_message += f"```\nCommon items:\n{item_list}```"
            if tools_list:
                response_message += f"```\nTools:\n{tools_list}```"
            await interaction.response.send_message(response_message)
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
            current_time = time.time()
            cooldown_time = 600
            if user_id in cooldowns:
                elapsed_time = current_time - cooldowns[user_id]
                if elapsed_time < cooldown_time:
                    remaining_time = cooldown_time - elapsed_time
                    await interaction.response.send_message(f'{interaction.user.mention}, you need to wait {int(remaining_time)} seconds before using this command again.')
                    return
                cooldowns[user_id] = current_time
            if chance == 1:
                if user_data[rob_id]['Cash'] > 0:
                    amount = random.randint(1, user_data[rob_id]['Cash'])
                    await interaction.response.send_message(f"You robbed {member.nick} for {amount} cash.", ephemeral=True)
                    user_data[user_id]['Cash'] += amount
                    user_data[rob_id]['Cash'] -= amount
                    await member.send(f"{interaction.user} has robbed you for {amount} cash. You now have {user_data[rob_id]['Cash']} cash left.")
                else:
                    await interaction.response.send_message(f"They were too poor to rob. Completely empty pockets. :pensive:", ephemeral=True)
            elif chance == 3:
                if user_data[rob_id]['Cash'] > 0:
                    amount = random.randint(1, user_data[rob_id]['Cash'])
                    await interaction.response.send_message(f"You robbed {member.nick} for {amount} cash. You were stealthy enough so that {member.nick} didn't find out you robbed them.", ephemeral=True)
                    user_data[user_id]['Cash'] += amount
                    user_data[rob_id]['Cash'] -= amount
                else:
                    await interaction.response.send_message(f"They were too poor to rob. Completely empty pockets. :pensive:", ephemeral=True)
            else:
                if user_id in bot_data['User Crimes']:
                    bot_data['User Crimes'][user_id] += 1
                else:
                    bot_data['User Crimes'][user_id] = 1
                bot_dump()
                if (bot_data['User Crimes'][user_id]*10) <= user_data[user_id]['Cash']:
                    amount = random.randint((bot_data['User Crimes'][user_id]*10), user_data[user_id]['Cash'])
                else:
                    amount = user_data[user_id]['Cash']
                user_data[rob_id]['Cash'] += amount//2
                user_data[user_id]['Cash'] -= amount
                jail_time = 120*bot_data['User Crimes'][user_id]
                if interaction.user.id == interaction.guild.owner_id:
                    await interaction.response.send_message(f"Can't arrest :pensive: Damned dictator!")
                    await interaction.channel.send(f"{interaction.user.mention} has been fined {amount} for the attempted theft on {member.nick}.")
                    await member.send()(f"You have been given {amount//2} as compensation for {interaction.user.nick}'s attempted robbery of your cash. Keep your pockets safe.")
                else:
                    await interaction.channel.send(f"{interaction.user.mention} was arrested for attempted theft. They have been fined {amount}. {member.nick} has been given compensation.")
                    await member.send(f"You have been given {amount//2} as compensation for {interaction.user.nick}'s attempted robbery of your cash. Keep your pockets safe.")
                    await interaction.response.send_message(f"You tried to rob {member.nick}, but you were caught. Have fun in jail I guess. :slight_smile: Jail time: {jail_time/120} minutes.", ephemeral=True)
                    jail = discord.utils.get(member.guild.roles, id=1307363196448931850)
                    roles = interaction.user.roles[1:]
                    role_ids = [role.id for role in roles]
                    user_data[user_id]['Roles'] += role_ids
                    with open('user_data.json', 'w') as file:
                        json.dump(user_data, file, indent=4)
                    if user_id in bot_data['User Bail']:
                        bot_data['User Bail'][user_id] += 50 * bot_data['User Crimes'][user_id]
                    else:
                        bot_data['User Bail'][user_id] = 50
                    with open('bot_data.json', 'w') as file:
                        json.dump(bot_data, file, indent=4)
                    await interaction.user.remove_roles(*roles)
                    await interaction.user.add_roles(jail)
                    await asyncio.sleep(jail_time)
                    updated_user = await interaction.guild.fetch_member(interaction.user.id)
                    if jail in updated_user.roles:
                        await interaction.user.remove_roles(jail)
                        await interaction.user.add_roles(*roles)
                        bot_data['User Crimes'][user_id] = 0
                        bot_data['User Bail'][user_id] = 0
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
                if user_id in bot_data['User Crimes']:
                    bot_data['User Crimes'][user_id] += 2
                    if user_id in bot_data['User Bail']:
                        bot_data['User Bail'][user_id] += 50*bot_data['User Crimes'][user_id]
                    else:
                        bot_data['User Bail'][user_id] = 50*bot_data['User Crimes'][user_id]
                else:
                    bot_data['User Crimes'][user_id] = 2
                    if user_id in bot_data['User Bail']:
                        bot_data['User Bail'][user_id] += 50*bot_data['User Crimes'][user_id]
                    else:
                        bot_data['User Bail'][user_id] = 50*bot_data['User Crimes'][user_id]
                bot_dump()
                await interaction.response.send_message(f"Jailbreak failed! {interaction.user.nick} is now in jail.", ephemeral=True)
                asyncio.sleep(120*bot_data['User Crimes'][user_id])
                if jail_role not in interaction.user.roles:
                    await interaction.response.send_message(f"Imagine not serving your sentence. Kinda cringe not gonna lie.", ephemeral=True)
                else:
                    await interaction.user.remove_roles(jail_role)
                    await interaction.user.add_roles(*roles)
                    role_ids.clear()
                user_dump()
        elif action == "B":
            if user_data[user_id]['Cash'] >= bot_data['User Bail'][str(selected_member.id)]:
                await selected_member.remove_roles(jail_role)
                await selected_member.add_roles(*roles)
                user_data[user_id]['Cash'] -= bot_data['User Bail'][str(selected_member.id)]
                bot_data['User Bail'][str(selected_member.id)] -= bot_data['User Bail'][str(selected_member.id)]
                user_data[str(selected_member.id)]['Roles'].clear()
                bot_dump()
                user_dump()
                await interaction.channel.send(f"{selected_member.nick} has been bailed out of jail.")
                await selected_member.send(f"{interaction.user.nick} bailed you out of jail.")
            else:
                await interaction.response.send_message(f"You don't have enough cash to bail out {selected_member.nick}. Bail: {bot_data['User Bail'][str(selected_member.id)]}")
                
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
            if user_id in bot_data['User Crimes']:
                jail_time = 60*bot_data['User Crimes'][user_id]
                if interaction.user.id == interaction.guild.owner_id:
                    await interaction.response.send_message(f"You literally own me. Here, you are no longer wanted. Couldn't you just do this yourself? Jesus.")
                    bot_data['User Bail'][user_id] -= bot_data['User Bail'][user_id]
                    user_data[user_id]['Roles'].clear()
                    bot_data['User Crimes'][user_id] = 0
                    bot_dump()
                    user_dump()
                else:
                    role = interaction.user.roles[1:]
                    role_ids = [role.id for role in role]
                    user_data[user_id]['Roles'] += role_ids
                    await interaction.user.add_roles(jail_role)
                    await interaction.user.remove_roles(*role)
                    await interaction.response.send_message(f"You turned yourself in. The police halved your sentence time since you turned yourself in willingly. You need to stay in jail for {jail_time/60} minutes.")
                    bot_dump()
                    user_dump()
                    await asyncio.sleep(jail_time)
                    await interaction.followup.send(f"Releasing {interaction.user.nick} from jail...")
                    updated_user = await interaction.guild.fetch_member(interaction.user.id)
                    if jail_role in updated_user.roles:
                        await interaction.user.send(f"You are no longer in jail. Your crime score is now zero and you are no longer wanted.")
                        await interaction.user.remove_roles(jail_role)
                        await interaction.user.add_roles(*role)
                        bot_data['User Crimes'][user_id] = 0
                        bot_data['User Bail'][user_id] = 0
                        role_ids.clear()
                        bot_dump()
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
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 1
                    else:
                        bot_data['User Crimes'][user_id] = 1
                    await inter.channel.send(f"{inter.user.nick} punched {member.mention} and dealt {att_dam}.")
                    await member.send(f"{inter.user.nick} punched you dealing {att_dam}. Health is now {user_data[attack_id]['Health']}")
                    await inter.response.send_message(f"Your crime score went up by 1 point.", ephemeral=True)
                else:
                    user_data[user_id]['Health'] -= att_dam//2
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 1
                    else:
                        bot_data['User Crimes'][user_id] = 1
                    await inter.response.send_message(f"You tried attacking {member.nick}, but they pushed you over dealing {att_dam//2}. Crime score went up by 1 point.", ephemeral=True)
                    await member.send(f"{inter.user} tried punching you, but you pushed them over and got away.")
            elif action == "K":
                att_dam = random.randint(0, 20)
                att_hit = random.randint(1, 2)
                if att_hit == 1:
                    user_data[attack_id]['Health'] -= att_dam
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 1
                    else:
                        bot_data['User Crimes'][user_id] = 1
                    await inter.channel.send(f"{inter.user.nick} kicked {member.mention} and dealt {att_dam}.")
                    await member.send(f"{inter.user.nick} kicked you dealing {att_dam}. Health is now {user_data[attack_id]['Health']}")
                    await inter.response.send_message(f"Your crime score went up by 1 point.", ephemeral=True)
                else:
                    user_data[user_id]['Health'] -= att_dam//2
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 1
                    else:
                        bot_data['User Crimes'][user_id] = 1
                    await inter.response.send_message(f"You tried kicking {member.nick}, but they tripped you dealing {att_dam//2}. Crime score went up by 1 point.", ephemeral=True)
                    await member.send(f"{inter.user} tried kicking you, but you tripped them and got away.")
            elif action == "A":
                success = random.randint(1, 5)
                att_dam = random.randint(15, 35)
                if success == 1:
                    user_data[attack_id]['Health'] -= att_dam//1.5
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 3
                    else:
                        bot_data['User Crimes'][user_id] = 3
                    await inter.channel.send(f"{inter.user.nick} assaulted {member.mention} and dealt {att_dam}.")
                    await member.send(f"{inter.user.nick} assaulted you dealing {att_dam}. Health is now {user_data[attack_id]['Health']}")
                    await inter.response.send_message(f"Your crime score went up by 3 points.", ephemeral=True)
                elif success == 2:
                    user_data[attack_id]['Health'] -= att_dam//2
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 3
                    else:
                        bot_data['User Crimes'][user_id] = 3
                    await inter.channel.send(f"{inter.user.nick} tried assaulting {member.mention}, but {member.nick} noticed. {inter.user.nick} scratched {member.nick}'s {random.choice(reaction)} dealing {att_dam//1.5}")
                    await inter.response.send_message(f"Your crime score went up by 3 points.", ephemeral=True)
                else:
                    user_data[user_id]['Health'] -= att_dam//2
                    if user_id in bot_data['User Crimes']:
                        bot_data['User Crimes'][user_id] += 2
                    else:
                        bot_data['User Crimes'][bot_data] = 2
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
                await inter.response.send_message(f"You wont be able to use any commands while hospitalized. Are you sure you want to heal yourself? Say 'yes' in this channel if you wish to heal. Heal time: {heal_time}")
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
                        await asyncio.sleep(heal_time)
                        user_data[user_id]['Health'] = 150
                        await inter.user.add_roles(*role)
                        await inter.user.remove_roles(hospital_role)
                        user_data[user_id]['Roles'].clear()
                        await inter.user.send(f"You are no longer in the hospital.")
                except asyncio.TimeoutError:
                    await inter.followup.send("You didn't answer in time.")
            else:
                await inter.response.send_message("The doctor told you to leave as your're in perfect shape.", ephemeral=True)
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

@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    print("Shutting down...")
    await bot.close()

bot.run(token)