import discord
from discord.ext import commands


class ExamCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.command(name='react')
	@commands.has_permissions(manage_messages=True)  # We can change that later so every student can use that function
	async def add_reactions(self, ctx):
		keywords = {'A': '🇦', 'B': '🇧', 'C': '🇨', 'D': '🇩', 'E': '🇪', 'F': '🇫'}
		channel = self.client.get_channel(809235905884979263)
		messages = await channel.history(limit=200).flatten()

		for message in messages:
			for keyword in keywords:
				if keyword in message.content and message.attachments:
					await message.add_reaction(keywords[keyword])

		print('Done!')

def setup(client):
	client.add_cog(ExamCommands(client))
