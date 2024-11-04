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
    if author not in Pokemon.pokemonlar:
        sans = random.randint(1, 3)
        if sans == 1:
            pokemon = Pokemon(author)
        elif sans == 2:
            pokemon = Sihirbaz(author)
        elif sans == 3:
            pokemon = Dovuscu(author)
        await ctx.send(await pokemon.bilgi())
        resim_url = await pokemon.resmi_goster()
        if resim_url:
            embed = discord.Embed()
            embed.set_image(url=resim_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokemon'un görüntüsü yüklenemedi.")
    else:
        await ctx.send("Zaten bir Pokemon oluşturdunuz.")

@bot.command()
async def saldir(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemonlar and ctx.author.name in Pokemon.pokemonlar:
            dusman = Pokemon.pokemonlar[target.name]
            saldirgan = Pokemon.pokemonlar[ctx.author.name]
            sonuc = await attacker.saldir(dusman)
            await ctx.send(sonuc)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon'a sahip olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

@bot.command()
async def bilgi(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemonlar:
        pokemon = Pokemon.pokemonlar[author]
        await ctx.send(await pokemon.bilgi())
    else:
        await ctx.send("Pokémon'un yok!")

@bot.command()
async def besle(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemonlar:
        pokemon = Pokemon.pokemonlar[author]
        yanit = await pokemon.besle()
        await ctx.send(yanit)
    else:
        await ctx.send("Pokémon'un yok!")


bot.run(token)

