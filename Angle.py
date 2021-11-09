import discord
import requests
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import random
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix="_")
from itertools import count
import discord
import aiofiles
from discord import embeds
from discord import message
from discord import guild
from discord import member
from discord import colour
from discord.ext import commands, tasks
import json   
from discord.ext.commands.converter import clean_content
from discord.utils import get, resolve_invite
import asyncio
import glob
import os.path




@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=""
        )
    )

@client.event
async def on_member_join(member):

    mbed = discord.Embed(
        color = discord.Color.magenta(),
        title = 'Welcome Message',
        description = f'Welcome {member.mention}, enjoy your stay!'
    )
    await member.send(embed=mbed)
    await member.guild.system_channel.send(f"Welcome, {member.mention} we hope you will like this server, enjoy! :D")
    

@client.event
async def on_member_leave(self):
  
    await member.guild.system_channel.send(f"bye, {self} we hope you enjoyed this server")


@client.command()
async def meme(ctx):
    r = requests.get("https://memes.blademaker.tv/api?lang=en")
    res = r.json()
    title = res["title"]
    ups = res["ups"]
    downs = res["downs"]
    sub = res["subreddit"]
    m = discord.Embed(title=f"{title}")
    m.set_image(url=res["image"])
    m.set_footer(text=f"upvotes: {ups} downvotes: {downs}")
    await ctx.send(embed=m)



@client.command(name="hello", help="This command returns a random welcome message")
async def hello(ctx):
    responses = [
        "***grumble*** Why did you wake me up?",
        "Top of the morning to you lad!",
        "Hello, how are you?",
        "Hi",
        "**Wasssuup!**",
    ]
    await ctx.send(random.choice(responses))

@client.command(name="nice", help="This command returns a random welcome message")
async def nice(ctx):
    responses = [
        "nice",
        
    ]
    await ctx.send(random.choice(responses))


@client.command(name="die", help="This command returns a random last words")
async def die(ctx):
    responses = [
        "why have you brought my short life to an end",
        "i could have done so much more",
        "i have a family, kill them instead",
        "hahhaha nerd angle never dieesss"




    ]
    await ctx.send(random.choice(responses))


@client.command(name="credits", help="This command returns the credits")
async def credits(ctx):
    await ctx.send("Made by `Trilogical`")



client.load_extension("music")
load_dotenv("token.env")
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
client.run(os.environ["TOKEN"])
