import discord
from discord.ext import commands
import asyncio
import time

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    #clear command deletes messages
    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'**Purged {amount} Messages**') 
        await ctx.message.delete()
    
    #on error command list for a error and awaits 
    @commands.Cog.listener() #Listens for errors and prints out a error to discord if a command is not found
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'> **Error Command Not Found.**')
    
    #clear error event
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**Specify an amount of messages to delete.**')


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'> User {member} has been kicked!')
    
    #kick error event
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**You must specify a user to kick.**')


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'> User {member} has been banned!.')

    #kick error event
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**You must specify a user to ban.**')

    @commands.command(aliases=["stop", "logout", "exit"])
    @commands.is_owner()
    async def quit(self, ctx):
        await self.client.logout()
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member, time: int=15):
        '''Mute a member in the guild'''
        secs = time * 60
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=False)
        await ctx.send(f"{user.mention} has been muted for {time} minutes.")
        await asyncio.sleep(secs)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} has been unmuted from the guild.')  


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmute a member in the guild'''
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} has been unmuted from the guild.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        '''Warn a member via DMs'''
        warning = f'You have been warned in **{ctx.guild}** by **{ctx.author}** for {reason}'
        if not reason:
            warning = f'You have been warned in **{ctx.guild}** by **{ctx.author}**'
        try:
            await user.send(warning)
        except discord.Forbidden:
            return await ctx.send('The user has disabled DMs for this guild or blocked the bot.')
        await ctx.send(f'**{user}** has been **warned**')

    @commands.command()
    async def baninfo(self, ctx, *, name_or_id):
        '''Check the reason of a ban from the audit logs.'''
        ban = await ctx.get_ban(name_or_id)
        em = discord.Embed()
        em.color = await ctx.get_dominant_color(ban.user.avatar_url)
        em.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
        em.add_field(name='Reason', value=ban.reason or 'None')
        em.set_thumbnail(url=ban.user.avatar_url)
        em.set_footer(text=f'User ID: {ban.user.id}')

        await ctx.send(embed=em)



    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put **{channel.name}** on lockdown.")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put **{channel.name}** on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have removed **{channel.name}** from lockdown.")





def setup(client):
    client.add_cog(Mod(client))
