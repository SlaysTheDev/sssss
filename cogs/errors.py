import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client


@commands.Cog.listener()
async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'**Error Command Not Found.**')



@commands.Cog.listener()
async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Specify an amount of messages to delete.**')










def setup(client):
    client.add_cog(Errors(client))