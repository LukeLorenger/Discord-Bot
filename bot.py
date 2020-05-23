# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:11:42 2020

@author: luke6
"""

import discord
import random
import os
# importing asyncio for sleep command
import asyncio
from discord.ext import commands
# prefix initiates bot, instance of bot created and set to client variable
client = commands.Bot(command_prefix = '!')

# function decorator
@client.event
# async-function // When bot has all info from discord, the bot puts itself into ready state(first event)
async def on_ready():
    print('Bot is ready Captain.')

@client.event
# async-function //  member is a member object, message saying member has joined server
async def on_member_join(member):
    print(f'{member} has joined the server. ')

@client.event
# async-function //  member has left or been removed from server
async def on_member_remove(member):
    print(f'{member} has left the server. ')

@client.command()
# commanding bot // ctx = context // * 1000 to get milliseconds, round() to round up//displaying latency of bot
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
# kick command, passing in ctx=context, pass in member as a member object, pass in reason for audit logs,
# asterisk is added for any additional info to be added to reason.
async def kick(ctx, member : discord.Member, *, reason=None):
    # kick member even if reason=none.
    await member.kick(reason=reason)

@client.command()
# ban command, passing in ctx=context, pass in member as a member object, pass in reason for audit logs,
# asterisk is added for any additional info to be added to reason.
async def ban(ctx, member : discord.Member, *, reason=None):
    # ban member even if reason=none.
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
# passing in ctx=context, asterisk to grab any info in relation, pass in member
async def unban(ctx, *, member):
    # goes through banned users on server and generates a list of banned entries containing user object and reason for user ban
    banned_users = await ctx.guild.bans()

    # going through all banned entries
    for ban_entry in banned_users:
        # pull user from ban entry, set to user
        user = ban_entry.user
        # uses unban method from guild
        await ctx.guild.unban(user)
        # bot sends message to server the user is unbanned.
        await ctx.send(f'Unbanned {user.mention}')


@client.command()
# ctx = content passed in//amount is amnt of messages you wanted deleted from channel, default # used when amnt is not specified
async def clear(ctx, amount=5):
    # taking context, accessing channel, on channel we are calling purge method, limit is amount
    await ctx.channel.purge(limit=amount)

@client.command(aliases=['8ball', '8b', 'eb'])
# all string aliases can be used to invoke this _8ball command function
# ctx=context, aterisk allows multiple parameters, 10 positive responses, 5 neutral, 5 negative
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                        "It is decidedly so.",
                        "Without a doubt.",
                        "Yes - definitely.",
                        "You may rely on it.",
                        "As I see it, yes.",
                        "Most likely.",
                        "Outlook good.",
                        "Yes.",
                        "Signs point to yes.",
                        "Reply hazy, try again.",
                        "Ask again later.",
                        "Better not tell you now.",
                        "Cannot predict now.",
                        "Concentrate and ask again.",
                        "Don't count on it.",
                        "My reply is no.",
                        "My sources say no.",
                        "Outlook not so good.",
                        "Very doubtful."]
    await ctx.send("Let me consider your question for a moment human...")
    await asyncio.sleep(3)
# f string for question, taking in question from user, new line for answer, random w/ choice() method to randomly choose from response list
    await ctx.send(f'Your question was: \n{question}')
    await asyncio.sleep(2)
    await ctx.send(f'\nMy answer for you is: \n{random.choice(responses)}')

@client.command()
# load command to load extension // ctx=context, extension is going to represent cog i want to load
async def load(ctx, extension):
    # method used to load extension//accesing example through cogs folder
    client.load_extension(f'cogs.{extension}')

@client.command()
# unload command to unload extension //ctx=context, extension is going to represent cog i want to unload
async def unload(ctx, extension):
    # method used to unload extension//accessing example through cogs folder
    client.unload_extension(f'cogs.{extension}')

# dir=directory//listdir() lists all files in given directory// './cogs' represents current directory, give all files within directory
for filename in os.listdir('./cogs'):
    # as we loop through directory, if it is a .py file;
    if filename.endswith('.py'):
        # load filename // splicing, cutting off last 3 characters, dont want'.py' at end of file
        client.load_extension(f'cogs.{filename[:-3]}')

# run client//insert bot token//links code to application
client.run('Your token goes here.')
