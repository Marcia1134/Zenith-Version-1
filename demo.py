import discord 
from discord.ext import commands
from discord import app_commands

class Demo(commands.Cog):
    def __init__(self, bot : commands.Bot):
        print("so this got loaded?")
        self.bot = bot
    
    @app_commands.command(name="demo_dec", description="demo command")
    @discord.app_commands.choices(choice_demo = [discord.app_commands.Choice(name="option 1", value=1),
                                                discord.app_commands.Choice(name="option 2", value=2),
                                                discord.app_commands.Choice(name="option 3", value=3),
                                                discord.app_commands.Choice(name="option 4", value=4),
                                                discord.app_commands.Choice(name="option 5", value=5),
                                                discord.app_commands.Choice(name="option 6", value=6),
                                                ])
    async def demo_dec(self, interaction : discord.Interaction, choice_demo : int, demo_str : str, demo_int : int, demo_bool : bool):
        await interaction.response.send_message(f"""`{choice_demo}` - choice demo
`{demo_str}` - string demo
`{demo_int}` - int demo
`{demo_bool} - bool demo`""")
        embed = discord.Embed(color=discord.Color.green(), title="demo embed", description="This is description")
        embed.set_thumbnail(url=interaction.user.default_avatar.url)
        embed.set_image(url="https://i.ibb.co/db8SSbZ/night-rice-field-terraces-asian-mountains-landscape-with-paddy-plantation-cascades-chinese-agricultu.jpg")
        embed.add_field(name="This is a field name", value="this is a field value")
        embed.set_footer(text="this is a footer")

        class demoview(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(discord.ui.Button(style=discord.ButtonStyle.url, url='https://zorox.to/', label="Click me to go to a website!"))
            
            @discord.ui.button(label="modal demo", style=discord.ButtonStyle.primary, emoji="📖")
            async def demo_modal(self, interaction : discord.Interaction, button : discord.Button):

                class modal_demo(discord.ui.Modal):
                    def __init__(self):
                        super().__init__(title = "This is a demo", timeout = None)
                        self.short_input = discord.ui.TextInput(label="this is a short text input", placeholder="You can either have hints like this", required=True)
                        self.long_input = discord.ui.TextInput(label="This is a long input", style=discord.TextStyle.long, default="Or you can have text already present!", required=True)
                        self.paragraph_input = discord.ui.TextInput(label="This is a paragraph input", style=discord.TextStyle.paragraph, placeholder="Or you can even have options that are not required...", min_length=16, max_length=962, required=False)
                        self.add_item(self.short_input)
                        self.add_item(self.long_input)
                        self.add_item(self.paragraph_input)

                    async def on_submit(self, interaction : discord.Interaction):
                        await interaction.response.send_message(f"""
```{self.short_input.value}```
```{self.long_input.value}```
*```{self.paragraph_input.value}```*
""")
                await interaction.response.send_modal(modal_demo())

            @discord.ui.select(options=[discord.SelectOption(label="This is option 1", value="Option 1", description="This is an option that is one"),
                                        discord.SelectOption(label="This is a second option ", value="Option 2", default=True, description="This one is the default!"),
                                        discord.SelectOption(label="This has an emoji", value="Option 3", description="This one is the emoji one", emoji="3️⃣")], 
                                        min_values=1, 
                                        max_values=1)
            async def this_dropdown_function(self, interaction : discord.Interaction, select : discord.ui.Select):
                await interaction.response.send_message(f"you picked: {select.values[0]}")

            
        await interaction.channel.send(embed=embed, view=demoview())

async def setup(bot : commands.Bot):
    print("this was run")
    await bot.add_cog(Demo(bot))