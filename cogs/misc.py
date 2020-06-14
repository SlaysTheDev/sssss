import discord
from discord.ext import commands
import random
import secrets
import nmap
from io import BytesIO


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")
            await ctx.message.delete()



    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """Returns an invite for the bot (not really)"""
        return await ctx.send("**fuck off, you can't invite me to your server.**")
        await ctx.message.delete()



    @commands.command()
    async def uptime(self, ctx):
        """Shows SyncloVPNs Bot's uptime"""
        up = abs(self.bot.uptime - int(time.perf_counter()))
        up = str(datetime.timedelta(seconds=up))
        await self.bot.say("`Uptime: {}`".format(up))
        await ctx.message.delete()


    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails','Your Gay']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")
        await ctx.message.delete()


 
    @commands.command(pass_context=True)
    async def gay(self, ctx):
        username = ctx.message.author.display_name
        gayness = random.randint(1, 100)
        embed=discord.Embed(title="Are you gay?", color=0xff69b4)
        embed.add_field(name= 'You are...', value= '**{}% gay**'.format(gayness), inline=True)
        embed.set_footer(text="Requested by " + username )
        await ctx.send(embed=embed)


    @commands.command(aliases=['answer'])
    async def choice(self, ctx):
        """ Yes or No Choice! """
        choices = ['Yes', 'No','Stop Asking me questions Skid']
        await ctx.send(f"**{ctx.author.name}** Here's your answer **{random.choice(choices)}**!")
        await ctx.message.delete()
        




    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you
        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f":white_check_mark: **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")











    






def setup(client):
    client.add_cog(Misc(client))