import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

        

    @commands.command(aliases=['si', 'server','sinfo'])
    async def serverinfo(self, ctx):
        '''Get server info'''
        guild = ctx.guild
        guild_age = (ctx.message.created_at - guild.created_at).days
        created_at = f"Server created on {guild.created_at.strftime('%b %d %Y at %H:%M')}. That\'s over {guild_age} days ago!"
        color = discord.Color.green()

        em = discord.Embed(description=created_at, color=color)
        em.add_field(name='**Online Members**', value=len({m.id for m in guild.members if m.status is not discord.Status.offline}))
        em.add_field(name='Total Members', value=len(guild.members))
        em.add_field(name='Text Channels', value=len(guild.text_channels))
        em.add_field(name='Voice Channels', value=len(guild.voice_channels))
        em.add_field(name='Roles', value=len(guild.roles))
        em.add_field(name='Owner', value=guild.owner)

        em.set_thumbnail(url=None or guild.icon_url)
        em.set_author(name=guild.name, icon_url=None or guild.icon_url)
        await ctx.send(embed=em)

    @commands.command(aliases=['uinfo'])
    async def info(self, ctx, member: discord.Member):

        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)

        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)

        embed.add_field(name="Bot?", value=member.bot)

        await ctx.send(embed=embed)






    @commands.command()
    async def about(self, ctx):

        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

        embed.set_author(name="Bot Info" ,icon_url=ctx.author.avatar_url)

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name='``Author``', value='**Slays#6689**',inline=False)
        embed.add_field(name='``Guilds``', value=len(self.client.guilds))
        embed.add_field(name="``Library``", value="**discord.py**",inline=False)
        embed.add_field(name="``Commands loaded``", value=len([x.name for x in self.client.commands]),inline=False)
        embed.add_field(name='``Discord``', value='https://discord.gg/xygFV7',inline=False)
        embed.add_field(name='``Website``', value='https://synclovpn.com/',inline=False)




        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Info(client))