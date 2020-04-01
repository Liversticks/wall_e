from discord.ext import commands
import discord
import importlib
import os
import inspect
import random
import sys
from resources.cogs.manage_cog import ManageCog
from resources.utilities.config.config import WallEConfig
from resources.utilities.database import setup_database, setup_stats_of_command_database_table
from resources.utilities.embed import embed as imported_embed
from resources.utilities.logger_setup import initialize_logger
from resources.utilities.log_channel import write_to_bot_log_channel

bot = commands.Bot(command_prefix='.')

##################################################
# signals to all functions that use            ##
# "wait_until_ready" that the bot is now ready ##
# to start performing background tasks         ##
##################################################
@bot.event
async def on_ready():
    logger.info('[main.py on_ready()] Logged in as')
    logger.info('[main.py on_ready()] {}'.format(bot.user.name))
    logger.info('[main.py on_ready()] {}'.format(str(bot.user.id)))
    logger.info('[main.py on_ready()] ------')
    WallEConfig.set_config_value("bot_profile", "BOT_NAME", bot.user.name)
    WallEConfig.set_config_value("bot_profile", "BOT_AVATAR", bot.user.avatar_url)
    logger.info(
        "[main.py on_ready()] BOT_NAME initialized to {}".format(
            WallEConfig.get_config_value("bot_profile", "BOT_NAME")
            )
        )
    logger.info(
        "[main.py on_ready()] BOT_AVATAR initialized to {}".format(
            WallEConfig.get_config_value("bot_profile", "BOT_AVATAR")
            )
        )
    logger.info("[main.py on_ready()] {} is now ready for commands".format(bot.user.name))

########################################################
# Function that gets called any input or output from ##
# the script					     ##
########################################################
@bot.event
async def on_message(message):
    if message.guild is None and message.author != bot.user:
        await message.author.send("DM has been detected \nUnfortunately none of my developers are smart enough to "
                                  "make me an AI capable of holding a conversation and no one else has volunteered"
                                  " :( \nAll I can say is Harry Potter for life and Long Live Windows Vista!")
    else:
        await bot.process_commands(message)


@bot.listen()
async def on_member_join(member):
    if member is not None:
        output = "Hi, welcome to the SFU CSSS Discord Server\n"
        output += "\tWe are a group of students who live to talk about classes and nerdy stuff.\n"
        output += "\tIf you need help, please ping any of our Execs, Execs at large, or First Year Reps.\n"
        output += "\n"
        output += "\tOur general channels include some of the following:\n"
        output += "\t#off-topic, where we discuss damn near anything.\n"
        output += "\t#first-years, for students who are starting, or about to start their first year.\n"
        output += "\t#discussion, for serious non-academic discussion. (Politics et al.)\n"
        output += "\t#sfu-discussions, for all SFU related discussion.\n"
        output += "\t#projects_and_dev, for non-academic tech/dev/project discussion.\n"
        output += "\t#bot_commands_and_misc, for command testing to reduce spam on other channels.\n"
        output += "\n"
        output += "\n"
        output += "\tWe also have a smattering of course specific Academic channels.\n"
        output += "\tYou can give yourself a class role by running <.iam cmpt320> or create a new class by <.newclass"
        output += " cmpt316>\n"
        output += "\tPlease keep Academic Honesty in mind when discussing course material here.\n"
        e_obj = await imported_embed(
            member,
            description=output,
            author=WallEConfig.get_config_value('bot_profile', 'BOT_NAME'),
            avatar=WallEConfig.get_config_value('bot_profile', 'BOT_AVATAR')
        )
        if e_obj is not False:
            await member.send(embed=e_obj)
            logger.info("[main.py on_member_join] embed sent to member {}".format(member))

# April Fools 2020 - A Mysterious Virus has Appeared!
# Two new roles: Asymptomatic (no colour) and Infected (Black)
# How to use: Give someone talkative the Asymptomatic role

# Incubation cycle
# Timer cycle: Every minute
# For each cycle:
# Asymptomatic -> Infected at 0.01 chance = Mean Incubation Period is 100 cycles
async def incubation_cycle():
    await bot.wait_until_ready()
    while not bot.is_closed:
        asymp_role = discord.utils.get(bot.guilds[0].roles, name='Asymptomatic')
        if asymp_role is None:
            asymp_role = await bot.guilds[0].create_role(name='Asymptomatic')
        infec_role = discord.utils.get(bot.guilds[0].roles, name='Infected')
        if infec_role is None:
            infec_role = await bot.guilds[0].create_role(name='Infected', colour=discord.Colour(1))
        asymp_members = asymp_role.members
        for asymp_member in asymp_members:
            if random.random() < 0.01:
                await asymp_member.remove_roles(asymp_role)
                await asymp_member.add_roles(infec_role)
        await asyncio.sleep(60)


# Transmission trigger
# (Susceptible) = authors of the previous 4 channel messages and neither Asymptomatic nor Infected
# For each post by an Asymptomatic:
# Each (Susceptible) -> Asymptomatic at 0.5 chance = Mean Single Event Reproduction is 2
# For each post by an Infected:
# Each (Susceptible) -> Asymptomatic at 0.75 chance = Mean Single Event Reproduction is 3
@bot.listen()
async def on_message(message):
    asymp_role = discord.utils.get(bot.guilds[0].roles, name='Asymptomatic')
    if asymp_role is None:
        asymp_role = await bot.guilds[0].create_role(name='Asymptomatic')
    infec_role = discord.utils.get(bot.guilds[0].roles, name='Infected')
    if infec_role is None:
        infec_role = await bot.guilds[0].create_role(name='Infected', colour=discord.Colour(1))
    sick_member = message.author
    if asymp_role in sick_member.roles or infec_role in sick_member.roles:
        p = 0.5 if asymp_role in sick_member.roles else 0.75
        susce_channel = message.channel
        async for susce_message in susce_channel.history(limit=4, before=message):
            susce_member = susce_message.author
            if asymp_role not in susce_member.roles and infec_role not in susce_member.roles:
                if random.random() < p:
                    await susce_member.add_roles(asymp_role)


####################
# STARTING POINT ##
####################
if __name__ == "__main__":
    logger, FILENAME = initialize_logger()
    WallEConfig = WallEConfig(os.environ['ENVIRONMENT'])

    logger.info("[main.py] Wall-E is starting up")
    if WallEConfig.enabled("database", option="DB_ENABLED"):
        setup_database(WallEConfig)
        setup_stats_of_command_database_table(WallEConfig)
    # tries to open log file in prep for write_to_bot_log_channel function
    try:
        logger.info("[main.py] trying to open {}.log to be able to send "
                    "its output to #bot_log channel".format(FILENAME))
        f = open('{}.log'.format(FILENAME), 'r')
        f.seek(0)
        bot.loop.create_task(write_to_bot_log_channel(bot, WallEConfig, f))
        logger.info("[main.py] log file successfully opened and connection to bot_log channel has been made")
    except Exception as e:
        logger.error("[main.py] Could not open log file to read from and sent entries to bot_log channel due to "
                     "following error{}".format(e))

    # load the code dealing with test server interaction
    try:
        bot.add_cog(ManageCog(bot, WallEConfig))
    except Exception as e:
        exception = '{}: {}'.format(type(e).__name__, e)
        logger.error('[main.py] Failed to load test server code testenv\n{}'.format(exception))

    # removing default help command to allow for custom help command
    logger.info("[main.py] default help command being removed")
    bot.remove_command("help")
    # tries to loads any commands specified in the_commands into the bot

    for cog in WallEConfig.get_cogs():
        try:
            logger.info("[main.py] attempting to load command {}".format(cog["name"]))
            cog_file = importlib.import_module(str(cog['path'])+str(cog["name"]))
            cog_class_name = inspect.getmembers(sys.modules[cog_file.__name__], inspect.isclass)[0][0]
            cog_to_load = getattr(cog_file, cog_class_name)
            bot.add_cog(cog_to_load(bot, WallEConfig))
            logger.info("[main.py] {} successfully loaded".format(cog["name"]))
        except Exception as e:
            exception = '{}: {}'.format(type(e).__name__, e)
            logger.error('[main.py] Failed to load command {}\n{}'.format(cog, exception))
    # April Fools 2020: Add virus incubation cycle
    bot.loop.create_task(incubation_cycle())
    # final step, running the bot with the passed in environment TOKEN variable
    bot.run(WallEConfig.get_config_value("basic_config", "TOKEN"))
