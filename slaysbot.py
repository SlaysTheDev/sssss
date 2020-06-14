import discord
import os
from discord.ext import commands
import datetime
import asyncio 
import socket
import json
import ipinfo
import requests
import whois
client = commands.Bot(command_prefix ='.',case_insensitive=True) # Sets the prfix of the Bot
client.remove_command('help') #removes help command so you can customize your own
#os.chdir('/root/SlaysBotv1/cogs')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching, name="Type .help for Help"))
    print("Bot is ready.")   


@client.command()
@commands.is_owner()
async def load(ctx, extension,):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded **{extension}.py**")

@client.command()
@commands.is_owner()
async def unload(ctx, extension,):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded **{extension}.py**")

@client.command()
@commands.is_owner()
async def reload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Reloaded **{extension}.py**")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')






@client.event
async def on_member_join(member):
    embed = discord.Embed(colour=0x95efcc, description=f"Welcome to SyncloVPNs You are the {len(list(member.guild.members))} member",)
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()

    channel = client.get_channel(id=710956039876378698)

    await channel.send(embed=embed)




amounts = {}

@client.event
async def on_ready():
    global amounts
    try:
        with open('/root/ssss/amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}

@client.command(pass_context=True)
async def bal(ctx):
    id = str(ctx.message.author.id)
    if id in amounts:
        await ctx.send("You have **{}** in the bank".format(amounts[id]))
    else:
        await ctx.send("You do not have an account")

@client.command(pass_context=True)
async def register(ctx):
    id = str(ctx.message.author.id)
    if id not in amounts.keys():
        amounts[id] = 100
        await ctx.send("**You are now registered**")
        _save()
    else:
        await ctx.send("You already have an account")

@client.command(pass_context=True)
async def transfer(ctx, amount: int, other: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if primary_id not in amounts:
        await ctx.send("You do not have an account")
    elif other_id not in amounts:
        await ctx.send("The other party does not have an account")
    elif amounts[primary_id] < amount:
        await ctx.send("You cannot afford this transaction")
    else:
        amounts[primary_id] -= amount
        amounts[other_id] += amount
        await ctx.send("Transaction complete")
    _save()

def _save():
    with open('/root/ssss/amounts.json', 'w+') as f:
        json.dump(amounts, f)

@client.command()
async def save():
    _save()















client.run('TOKEN')
