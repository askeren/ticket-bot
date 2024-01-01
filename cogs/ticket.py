import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, message_command, user_command, Option
import ezcord

class Ticket(ezcord.Cog, emoji="🎫"):

# Ticket System

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def ticket(self, ctx):
        embed3 = discord.Embed(
            title="Ticket Erstellen",
            description=f"Erstelle ein Ticket, indem du auf **Ticket erstellen** drückst.",
            color=discord.Color.red(),
        )

        await ctx.send(embed=embed3, view=ANView())
        await ctx.respond("Ticket-Embed wurde erstellt.", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ANView())
        self.bot.add_view(ANClose())


class ANView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket erstellen", style=discord.ButtonStyle.primary, emoji="🎟️", custom_id="ticket")
    async def button_callback1(self, button, interaction: discord.Interaction):

        ### Authorizations for the new ticket channel

        staff_role = interaction.guild.get_role(YOUR STAFF ROLE ID)
        username = interaction.user.name

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        ### Ticket message in the new ticket channel

        embed = discord.Embed(
            title="ArcaneNetworks | Neues Ticket",
            description=f"{username} hat ein neues Ticket erstellt.\n {staff_role.mention}",
            color=discord.Color.red(),
        )

        embed.set_footer(text="Bitte warte bis sich ein Teammitglied meldet.")

        ### Create ticket channel

        ticket_channel = await interaction.guild.create_text_channel(f"ticket-{username}", category=interaction.channel.category, overwrites=overwrites)
        await ticket_channel.send(embed=embed, view=ANClose())

        ### Confirmation message

        embed2 = discord.Embed(
            title="ArcaneNetworks | Ticket",
            description=f"Dein Ticket wurde erstellt: {ticket_channel.mention}",
            color=discord.Color.red(),
        )

        await interaction.response.send_message(embed=embed2, ephemeral=True)

class ANClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close")
    async def button_callback1(self, button, interaction: discord.Interaction):

        staff_role = interaction.guild.get_role(YOUR STAFF ROLE ID)
        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("Du hast keine Berechtigung, um dieses Ticket zu schließen.", ephemeral=True)
            return

        ### Close ticket

        await interaction.channel.delete()

        ### Confirmation message

        embed = discord.Embed(
            title="ArcaneNetworks | Ticket",
            description=f"Dein Ticket wurde geschlossen.",
            color=discord.Color.red(),
        )

        await interaction.user.send(embed=embed)

def setup(bot: discord.Bot):
    bot.add_cog(Ticket(bot))
