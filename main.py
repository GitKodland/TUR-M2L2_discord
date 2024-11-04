import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Sihirbaz(author)
        elif chance == 3:
            pokemon = Dovuscu(author)
        await ctx.send(await pokemon.bilgi())
        image_url = await pokemon.resmi_goster()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokemon'un görüntüsü yüklenemedi.")
    else:
        await ctx.send("Zaten bir Pokemon oluşturdunuz.")

@bot.command()
async def saldir(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.saldir(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon'a sahip olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

@bot.command()
async def bilgi(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.bilgi())
    else:
        await ctx.send("Pokémon'un yok!")

@bot.command()
async def besle(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.besle()
        await ctx.send(response)
    else:
        await ctx.send("Pokémon'un yok!")


bot.run(token)

