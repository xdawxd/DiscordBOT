import os
import random
import discord
from discord.ext import commands


class ExamCommands(commands.Cog):
	def __init__(self, client):
		self.client = client

	@staticmethod
	def write_data(data):
		with open('data.txt', 'a+') as file:
			for key, value in data.items():
				file.write(f'{key}: {value}\n')

	@staticmethod
	def read_data():
		with open('data.txt') as file:
			file.seek(0)
			f_formated = [i.strip().split(':') for i in file.readlines()]
			groups = {item[0]: item[1].strip() for item in f_formated}
			return groups

	def edit_messages(self, channel):  # TODO
		pass

	@commands.Cog.listener()
	async def on_message(self, msg):
		channel = self.client.get_channel(812498438699614209)
		author_id, guild, emoji, data, groups = str(msg.author.id), msg.guild, '😎', {} , {}

		role_names = [gn.name for gn in guild.roles]

		if msg.attachments:
			if len(msg.content):
				data = {author_id: msg.content}
				role_name = f'Grupa: {str(msg.content).rstrip().lstrip()}'

			if len(msg.content) == 0:
				random_group = random.randint(1, 1000000)
				data = {author_id: random_group}
				role_name = f'Grupa: {random_group}'

			await msg.add_reaction(emoji)

			if role_name not in role_names:
				await guild.create_role(name=role_name)
				role = discord.utils.get(guild.roles, name=role_name)
				await msg.author.add_roles(role)
			else:
				role = discord.utils.get(guild.roles, name=role_name)
				await msg.author.add_roles(role)

			# TODO -> make an if statement for repetative id's
			self.write_data(data)

			try:
				groups = self.read_data()
			except FileNotFoundError:
				pass

			# TODO -> fix the callout 
			message, counter = '', 0
			for user, group in groups.items():
				print(f'user: {user}, group: {group}')
				if group == msg.content:
					message += f'<@{user}>, '
					counter += 1
			if counter > 1:
				await channel.send(f'{message} sa w \'{role_name}\'')

	def role(self, reaction, user):
		msg_author_id = str(reaction.message.author.id)
		groups = self.read_data()

		for user_id, group in groups.items():
			if user_id == msg_author_id:
				role_name = f'Grupa: {group}'
				role = discord.utils.get(reaction.message.guild.roles, name=role_name)
				return role

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.emoji and user != self.client.user:
			role = self.role(reaction, user)
			await user.add_roles(role)

	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction, user):
			role = self.role(reaction, user)
			await user.remove_roles(role)

	@commands.command()
	@commands.has_permissions(manage_roles=True, ban_members=True)
	async def delete_roles(self, ctx):
		guild = ctx.message.guild
		roles = [role.name for role in ctx.message.guild.roles]
		for role_name in roles:
			if role_name.startswith('Grupa: '):
				role = discord.utils.get(guild.roles, name=role_name)
				await role.delete()
		await ctx.message.channel.send('Usunieto wszystkie grupy.')


def setup(client):
	client.add_cog(ExamCommands(client))
