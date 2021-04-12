"""
(Check for discord updates) If error "deny-new", cmd prompt pip install -U discord.py
"""

import discord
import random
import os
import asyncio
from discord.ext import commands, tasks
from itertools import cycle

# prefix initiates bot
client = commands.Bot(command_prefix='!')

status = cycle(['No Games', 'With Your Emotions', 'For The W'])

# When bot has all info from discord, the bot puts itself into ready state(first event)
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('The Game Of Life'))
    change_status.start()
    print('Bot is online.')


# Create task // Loop that updates status of bot every 10 sec
@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server. ')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server. ')

# checks if missing required argument is raised
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')

@client.command()
async def info(ctx, *, member: discord.Member):
    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
    await ctx.send(fmt.format(member, len(member.roles)))

@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')


@client.command()
async def bottles(ctx, amount: [int] = 99, *, liquid="beer"):
    await ctx.send('{} bottles of {} on the wall!'.format(amount, liquid))


# Take users input and repeat it
@client.command()
async def copycat(ctx, *, arg):
    await ctx.send(arg)


# Converter argument
@client.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@client.command()
async def insult(ctx, *, member):
    insults = ["Silly Goose",
                 "Peanut Butter Man",
                 "Jelly Belly",
                 "Burger Boy",
                 "Wicked Witch of The West",
                 "Novice",
                 "Rookie",
                 "Too Old",
                 "Grumpy",
                 "scum guzzler"]
    await ctx.send(f'\nThis person? \n{random.choice(insults)}')


@client.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped {}'.format(slapped, reason))


@client.command()
async def bot_ping(ctx):
    await ctx.send(f'bot_Pong! {round(client.latency * 1000)}ms')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
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
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

# event only triggered when clear command has error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify amount of messages to delete. ')

# all string aliases can be used to invoke this _8ball command function
@client.command(aliases=['8ball', '8b', 'eb'])
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
    await asyncio.sleep(2)
    await ctx.send(f'Your question was: \n{question}')
    await asyncio.sleep(2)
    await ctx.send(f'\nMy answer for you is: \n{random.choice(responses)}')


@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cog is loaded.')
    except:
        await ctx.send('Cog is already loaded.')



@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('Cog is unloaded.')
    except:
        await ctx.send('Cog is already unloaded.')


# dir=directory//listdir() lists all files in given directory// './cogs' represents current directory, give all files within directory
for filename in os.listdir('./cogs'):
    # as we loop through directory, if it is a .py file;
    if filename.endswith('.py'):
        # load filename // splicing, cutting off last 3 characters, don't want'.py' at end of file
        client.load_extension(f'cogs.{filename[:-3]}')

# run client//insert bot token//links code to application
# Change key before uploading to git
client.run('Discord Bot Key Here')
