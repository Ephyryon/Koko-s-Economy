import discord
import os
import json
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