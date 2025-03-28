import discord
from discord import app_commands
from discord.ui import View, Button
from discord.ext import commands, tasks
import os
import json
import random
import time
import asyncio
import Source_code.loc_code as loc_code
import Source_code.status_check as status_check
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load user data from a JSON file
if os.path.exists('Data/user_data.json'):
    with open('Data/Data/user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

def user_dump():
    with open('Data/Data/user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

if os.path.exists('Data/Data/item_data.json'):
    with open('Data/Data/item_data.json', 'r') as e:
        item_data = json.load(e)
else:
    item_data = {}

def item_dump():
    with open('Data/item_data.json', 'w') as file:
        json.dump(item_data, file, indent=4)

if os.path.exists('Data\job_data.json'):
    with open('Data/job_data.json', 'r') as t:
        job_data = json.load(t)
else:
    job_data = {}

def job_dump():
    with open('Data/job_data.json', 'w') as file:
        json.dump(job_data, file, indent=4)

if os.path.exists('Data/bot_data.json'):
    with open('Data/bot_data.json', 'r') as q:
        bot_data = json.load(q)
else:
    bot_data = {}

def bot_dump():
    with open('Data/bot_data.json', 'w') as file:
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
    status_tasks = [status_check.user_status(member, "Jail-Time") for member in guild.members] + [status_check.user_status(member, "Heal-Time") for member in guild.members] + [status_check.user_status(member, "Job-Cooldown") for member in guild.members] + [status_check.user_status(member, "Rob-Cooldown") for member in guild.members] + [status_check.user_status(member, "Fish-Cooldown") for member in guild.members] + [status_check.user_status(member, "Search-Cooldown") for member in guild.members] + [status_check.user_status(member, "Hunt-Cooldown") for member in guild.members] + [status_check.user_status(member, "Ronald") for member in guild.members] + [status_check.user_status(member, "Doctor") for member in guild.members] + [status_check.user_status(member, "Dina") for member in guild.members] + [status_check.user_status(member, "Ronald-Ques") for member in guild.members]
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
            await status_check.check_health(member)

@tasks.loop(minutes=15)
async def user_check():
    guild = bot.get_guild(guild_id)
    user_checks = [status_check.user_has(member, "cooldowns", False, True) for member in guild.members] + [status_check.user_has(member, "fauna", True, True) for member in guild.members] + [status_check.user_has(member, "Characters", False, True) for member in guild.members]
    await asyncio.gather(*user_checks)

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

            view = loc_code.MemberView(members_with_role, jailbreak_callback)
            await interaction.response.send_message("Select a member:", view=view, ephemeral=True)
        elif action == "B":
            members_with_role = [member for member in interaction.guild.members if jail_role in member.roles]
            if not members_with_role:
                await interaction.response.send_message("No members found with that role.", ephemeral=True)
                return

            view = loc_code.MemberView(members_with_role, jailbreak_callback)
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
            view = loc_code.MyOptions()
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
    view1 = loc_code.locView(loc=loc)
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