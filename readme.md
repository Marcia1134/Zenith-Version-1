# Zenith Collective Project

This is the the bot manager behind Zenith...

## Nameing Standards
All files use '_' (underscores) as a seperator. All discord.ext.commands.cogs are denoted with CamelCasing (This is done to avoid name space errors).
All cogs partaining to a service link 'events' or etc that are built for the purpose of using an event trigger from discord.py will use that events name as the file name and as the cog name (using the above standards)

## Cogs and Config files

There is a main config file and a seprate cogs list. These files contain all configuration data for Zenith Collective Manager. Please do note that all config settings are name sensitive. All loading and use of the config files should work past and error and you will be able to reload config files even after the bot is online and working. When adding or editing config files please do remember that JSON is highly sensitive to changes and forgetting a coma somewhere can cause a file to become unreable to python. Make sure you are using text high linting and error checking in your Code/Text Editor (visual studio \code has this out of the box). 

## Error reporting

When reporting and error with Zenith Collective Manager, please provide any relvant infomation by using print statements and using the console as a log of what is happening, use the Datetime module to create timestamps and if the error shows on discord include screen shots (if relvant), these errors can go to the GitHub or to my personal Email: mossmarcia1134+ZenithDevelopmentReporting@gmail.com

## Custom Assignments

You may notice that the use of dictionaries assigned to free names in for the bot class can be found in use all over the place in the code. This is to reduce repeative queries to the discord api and to allow for neater code. No [custom] functions are a part of the bot as of yet.. however that is something I will look at in the future, given that there is a need. For logging in the log channel or any channel that is used in more then one document you may want to create that. For that, edit the choice selection in the config_manager.py file to allow your channel to be assigned via a command, and and an entry to the config.json file under 'channels' and your channel's snowflake will be loaded into the bot (on_ready) under a dictionary, callable from any file. 

### Email Standards

The email addressed in this document all use mossmarcia1134 as a base plate with '+[str]' at the end. This is done for automatic email sorting. if you do not use the exact str my email client will not sort your email into the correct space and it will collect into my extras inbox, which may take time for me to get to. Using the correct email address with the correct str will help everyone with a more streamlined, efficent process.

Here is a look up:

**NOT CASE SENSTIVE**

Development Support : mossmarcia1134+ZenithDevelopmentSupport@Gmail.com
Error Reporting (developer) : mossmarcia1134+ZenithDevelopmentReporting@gmail.com
Error Reporting (public) : mossmarcia1134+HelpDesk@gmail.com
***More Adresses will be added as needed***
