import os
import random
import discord
from discord.ext import commands


class ExamCommands(commands.Cog):

	def __init__(self, client):
		self.client = client

	@staticmethod
	def write_data(data, file):
		for key, value in data.items():
			file.write(f'{key}: {str(value[0])} {str(value[1])}\n')

	@staticmethod
	def edit_data(data, emoji):  # edit the emoji saved in data.txt so its the same as the user in their group
		pass

	@commands.Cog.listener()
	async def on_message(self, msg):
		author_id = msg.author.id
		channel = msg.channel

		with open('emojis.txt', encoding='utf-8') as f:
			emojis = [i.strip().split(' ')[0].strip('\\')[0] for i in f.readlines()]

		if msg.attachments and len(msg.content) > 0:
			emoji = random.choice(emojis)
			data = {author_id: [msg.content, emoji]}
			emojis.remove(emoji)

			await msg.add_reaction(emoji)

			with open('data.txt', 'a+', encoding='utf-8') as f:
				if not os.path.getsize('data.txt'):
					self.write_data(data, f)

				else:
					f.seek(0)
					f_formated = [i.strip().split(':') for i in f.readlines()]
					content = {item[0]: item[1].lstrip().split(' ') for item in f_formated}

					self.write_data(data, f)

					for key, value in content.items():
						if data[author_id][0] == str(value[0]):
							await channel.send(f'{msg.author.mention} oraz <@{key}> sa w tej samej grupie.')
							await msg.clear_reaction(emoji)
							await msg.add_reaction(value[1])				
									

def setup(client):
	client.add_cog(ExamCommands(client))
