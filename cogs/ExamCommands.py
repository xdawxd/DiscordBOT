import os
import random
import discord
from discord.ext import commands


class ExamCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, msg):
		ctx = await self.client.get_context(msg)

		def write_data(data):
			for key, value in data.items():
				f.write(f'{key}: {str(value[0])} {str(value[1])}\n')

		with open('emojis.txt', encoding='utf-8') as f:
			emojis = [i.strip().split(' ')[0].strip('\\')[0] for i in f.readlines()]

		if msg.attachments:
			emoji = random.choice(emojis)
			await msg.add_reaction(emoji)

			data = {msg.author: [msg.content, emoji]}
			emojis.remove(emoji)

			with open('data.txt', 'a+', encoding='utf-8') as f:
				if os.path.getsize('data.txt'):
					f.seek(0)
					f_formated = [i.strip().split(':') for i in f.readlines()]
					content = {item[0]: item[1].lstrip().split(' ') for item in f_formated}

					write_data(data)

					for key, value in content.items():
						if int(data[msg.author][0]) == int(value[0]):
							await ctx.send(f'{msg.author.mention} oraz {key} sa w tej samej grupie.')

							# TODO -> figure out how to mention the other user
							# fix the bug: the program works only if the users post one after another
							# and have matchin groups.
							# If someone posts -> 123 -> 335 -> 123 the bot wont work.

				else:
					write_data(data)
									

def setup(client):
	client.add_cog(ExamCommands(client))
