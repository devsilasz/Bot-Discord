# flake8: noqa
# type: ignore
import discord
from discord.ext import commands
from discord.utils import get
import validation

class BotDiscordForAuth:
    def __init__(self) -> None:
        self.permissions = discord.Intents.default()
        self.permissions.members = True
        self.permissions.guilds = True
        self.permissions.message_content = True
        self.bot = commands.Bot(command_prefix="/", intents=self.permissions)

        @self.bot.event
        async def on_ready():
            # Aqui será a mensagem primaria que irá perguntar o
            print("funcionando")

        @self.bot.event
        async def on_member_join(ctx):
            channel = ctx.guild.system_channel
            if channel:
               message = await channel.send('Seja bem vindo ao servidor para verficação clique no ✉️ abaixo')
               await message.add_reaction('✉️')

        @self.bot.event
        async def on_reaction_add(reaction, user):
            if user.bot:
                return None

            if reaction.emoji == '✉️':
                # Aqui entra a função de verificação de dados presente na tabela
                await reaction.message.channel.send('Digite /validarUsuario (Seu email):')
                return None

        @self.bot.command()
        async def validarUsuario(ctx, value):
            token = open('token_notion.txt', 'r')
            token_notion = token.read()
            db_id = '15fea55528f780619da5f8c34abd3031'
            valid = validation.FuncionsValidation(token_notion, db_id).UserValidation(value)
            user = ctx.author
            if valid:
                cargo = ctx.guild.get_role(1319076975867986023)
                await user.add_roles(cargo)
                await ctx.send(f'{user} foi adicionado ao cargo de Tier 1 por pago!')
            else:
                cargo = ctx.guild.get_role(1319077014417838100)    
                await user.add_roles(cargo)
                await ctx.send(f'{user} foi adicionado ao cargo de Tier 2 por não ter pago!')
                
            
        
    def runBot(self):
        try:
            token = open('token_discord.txt', 'r')
            self.bot.run(token.read())
        except FileExistsError:
            ...
        return None
        
        
if __name__ == "__main__":

    BotDiscordForAuth().runBot()
