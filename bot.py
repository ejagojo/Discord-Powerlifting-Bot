import discord
from discord.ext import commands, tasks
from user import User
import json
from itertools import cycle
import asyncio

config_path = 'config.json'
with open(config_path) as f:
    data = json.load(f)
    token = data["TOKEN"]

BOT_PREFIX = ">>"
client = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all())

bot_status = cycle(["Squat", "Bench", "Deadlift", "Rest"])

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    print("Success: Connection Successful @discord")
    change_status.start()

@client.command()
async def test(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! Welcome to the server!!!! Please type '>>start' to proceed.")

@client.command(aliases=['Start'])
async def start(ctx):
    user = User(ctx.author.id)
    if user.is_existing_user():
        await ctx.author.send(f"Welcome back, {ctx.author.mention}! Are you here to change your prs? Type `>>yes` to update your PRs.")
    else:
        await ctx.author.send(f"Hello {ctx.author.mention}, let's set up your PRs. Please type `>>setPR` to begin.")

@client.command()
async def yes(ctx):
    await ctx.send(f"Great, {ctx.author.mention}! Let's update your PRs.")
    await setPR(ctx)

@client.command()   
async def setPR(ctx):
    dm_channel = await ctx.author.create_dm()

    await dm_channel.send(f"{ctx.author.mention} provide your squat personal record:")
    
    def check(message):
        # Check if the message is from the same author and in the same channel
        return message.author == ctx.author and message.channel == dm_channel
    
    try:
        squat_response = await client.wait_for('message', check=check, timeout=60)
        await dm_channel.send(f"{ctx.author.mention}, now provide your bench personal record:")
        bench_response = await client.wait_for('message', check=check, timeout=60)
        await dm_channel.send(f"{ctx.author.mention}, now provide your deadlift personal record:")
        deadlift_response = await client.wait_for('message', check=check, timeout=60)

        user = User(ctx.author.id)
        user.set_records(squat_response.content, bench_response.content, deadlift_response.content)

        await dm_channel.send("Records updated successfully")
    except asyncio.TimeoutError:
        await dm_channel.send("You took too long to respond.")


client.run(token)
