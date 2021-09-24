import discord
from discord.ext import commands
from io import BytesIO
import requests
import json
import pyjokes

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

       
    

    @commands.command()
    async def joke(self,ctx):
        joke=pyjokes.get_joke()
        await ctx.send(joke)
        await ctx.message.add_reaction("👍")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send("pong")
    
    @commands.command(name="msg", help="This command to msg a specific person")
    async def msg(self,ctx,p1: discord.Member,msg:str):

        await p1.send(f"{msg} , this message was sent by {ctx.author.mention} to you")

  
    

        


def setup(client):
    client.add_cog(General(client))