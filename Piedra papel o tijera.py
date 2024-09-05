import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
async def ppt(ctx):
    """Juega Piedra, Papel o Tijera con el bot."""
    opciones = ["piedra", "papel", "tijera"]
    jugar = True

    while jugar:
        await ctx.send("Piedra, Papel o Tijera? (escribe 'salir' para terminar)")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)

        if msg.content.lower() == "salir":
            await ctx.send("Adiós! Fue divertido jugar contigo.")
            jugar = False
        elif msg.content.lower() in opciones:
            eleccion_bot = random.choice(opciones)
            await ctx.send(f"Has elegido {msg.content.lower()}. El bot ha elegido {eleccion_bot}.")

            if msg.content.lower() == eleccion_bot:
                await ctx.send("Empate!")
            elif (msg.content.lower() == "piedra" and eleccion_bot == "tijera") or \
                 (msg.content.lower() == "papel" and eleccion_bot == "piedra") or \
                 (msg.content.lower() == "tijera" and eleccion_bot == "papel"):
                await ctx.send("Has ganado!")
            else:
                await ctx.send("Has perdido!")
        else:
            await ctx.send("Opción inválida. Por favor, escribe 'piedra', 'papel', 'tijera' o 'salir'.")

bot.run("")


