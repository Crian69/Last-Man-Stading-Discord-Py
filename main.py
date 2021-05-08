import discord
import os
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ext.commands import MaxConcurrencyReached

intent: discord.Intents = discord.Intents.all()
client: commands.Bot = commands.Bot(command_prefix='!', help_command=None, intent=intent)
TOKEN = os.getenv('TOKEN')


@client.event
async def on_ready():
    print('Bot Is Online')


@client.event
async def on_command_error(ctx, exc):
    if isinstance(exc, MaxConcurrencyReached):
        await ctx.reply('Contest Already Running PLease End To Start Again')
    else:
        raise exc


@client.command()
@commands.max_concurrency(1, BucketType.channel)
async def lms(ctx: discord.ext.commands.Context, channel: discord.TextChannel, timeout=10, length=3):
    def check(m: discord.Message):
        return m.channel == channel and len(m.content) >= length

    embed = discord.Embed(title='Last Man Standing Contest')
    embed.add_field(name='RULES',
                    value=f"Minimum Amount Of Letter In Message >= `{length}` \nTime For No Next Message To Win `{timeout}`secs",
                    inline=False)
    embed.add_field(value='CONTEST WILL BEGIN AFTER NEXT MESSAGE IS SENT IN THIS CHANNEL', name="​", inline=False)
    await channel.send(embed=embed)

    start_message: discord.Message = await client.wait_for('message', check=check)
    message: discord.Message = None

    while True:
        try:
            message = await client.wait_for('message', timeout=timeout, check=check)
        except Exception as E:
            if message is None:
                await start_message.reply(
                    f'CONGRATULATIONS {start_message.author.mention} You have won the LMS contest')
                return
            else:
                await message.reply(f"CONGRATULATIONS {message.author.mention} You have won the LMS contest")
                return
        else:
            continue


client.run(TOKEN)
