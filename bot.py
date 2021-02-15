import os
import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)

@client.command()
async def load(ctx, extension):  # ctx - context, extension - represents the cog that is being loaded or unloaded
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension}.')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension}.')


@client.command()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} reloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
    	client.load_extension(f'cogs.{filename[:-3]}')

client.run('PASS THE TOKEN HERE')
