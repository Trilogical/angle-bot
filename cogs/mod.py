import aiofiles

import json   


import discord
from discord.ext import commands

#client.event -> commands.Cog.listener()
#client.commands -> commands.command()

filterd_words = ["fuck","fuk","bitch","shit"]
laugh_words = ["lmao","lol","rofl","lul","XD"]

thonk_words=["hmm","thonk"]

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}

class Mods(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.warnings = {}

    @commands.Cog.listener()
    async def on_ready(self):
        
            print("mod cog loaded")

    #delete bad messages
    @commands.Cog.listener()
    async def on_message(self,msg):
        for word in filterd_words:
            if word in msg.content:
                await msg.delete()
        for word in laugh_words:
            if word in msg.content:
                await msg.add_reaction("😂")  

        for word in thonk_words:
            if word in msg.content:
                await msg.add_reaction("🤔")  



    @commands.command(aliases=['del'])
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount = 5):
        await ctx.channel.purge(limit=amount)

    #kick members
    @commands.command(aliases=["Kick","k"])
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx, member: discord.Member,*,reason="No reason provided"):
        embed = discord.Embed(
            title="",
            description=f"{member.name} ❌ __**has been kicked from the server**__",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

    #ban member
    @commands.command(aliases=['Ban',"b"])
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx, member: discord.Member,*,reason="No reason provided"):
        embed = discord.Embed(
            title="",
            description=f"{member.name} ❌ __**has been banned from the server**__",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
        await member.ban(reason=reason)


    #unban members
    @commands.command(aliases=['un'])
    @commands.has_permissions(ban_members = True)
    async def unban(self,ctx,*,member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

            if(user.name, user.discriminator)==(member_name,member_disc):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="",
                    description=f"__**{member_name}**__" +" | ✅ __**Has Been Unbanned**__",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
                return

    #mute member        
    @commands.command(aliases=['mu'])
    @commands.has_permissions(kick_members = True)
    async def mute(self,ctx, member: discord.Member):
        try:
            muted_role = ctx.guild.get_role(862733232629481483)
            await member.add_roles(muted_role)
            await ctx.send(f"__**{member.mention}**__"+" | 🔇 User Has Been Muted")
        except:
            await ctx.send("You dont have permission u noob !!")

    #umute member
    @commands.command(aliases=['unm'])
    @commands.has_permissions(kick_members = True)
    async def unmute(self,ctx, member: discord.Member):
        muted_role = ctx.guild.get_role(862733232629481483)
        await member.remove_roles(muted_role)
        await ctx.send(f"__**{member.mention}**__"+" | ✅ User Has Been Unmuted")

    #warn member
    @commands.command(aliases=['wa'])
    @commands.has_permissions(kick_members = True)
    async def warn(self,ctx, member: discord.Member, *, reason=None):
        if member is None:
            return await ctx.send("The Member You Told Couldn't Be Found, or You Didnt Mention One.")

        if reason is None:
            return await ctx.send("Please Provide a Reason, No Reason Provided")

        try:
            first_warning = False
            self.client.warnings[ctx.guild.id][member.id][0] += 1
            self.client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

        except KeyError:
            first_warning = True
            self.client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

        count =  self.client.warnings[ctx.guild.id][member.id][0]

        async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
            await file.write(f"{member.id} {ctx.author.id} {reason}\n")

        await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

    #clear warnings
    @commands.command(aliases=['chw'])
    @commands.has_permissions(kick_members = True)
    async def check_warning(self,ctx, member: discord.Member=None):
        if member is None:
            return await ctx.send("The Member You Told Couldn't Be Found, or You Didnt Mention One.")

        embed = discord.Embed(title=f"Displaying Warnings For {member.name}", description="", colour=discord.Color.green())
        try:
            i = 1
            for admin_id, reason in self.client.warnings[ctx.guild.id][member.id][1]:
                admin = ctx.guild.get_member(admin_id)
                embed.description += f"**Warnings {i}** Given By: {admin.mention} for: *'{reason}'*.\n"

            await ctx.send(embed=embed)
        
        except KeyError:
            await ctx.send("This User Has No Warnings")


def setup(client):
    client.add_cog(Mods(client))