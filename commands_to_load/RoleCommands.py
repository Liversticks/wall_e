from discord.ext import commands
import discord
import logging
from helper_files.Paginate import paginate
import helper_files.settings as settings
from helper_files.embed import embed

logger = logging.getLogger('wall_e')

class RoleCommands():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newrole(self, ctx, roleToAdd):
        logger.info("[RoleCommands newrole()] "+str(ctx.message.author)+" called newrole with following argument: roleToAdd="+roleToAdd)
        roleToAdd = roleToAdd.lower()
        guild = ctx.guild
        for role in guild.roles:
            if role.name == roleToAdd:
                eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Role '" + roleToAdd + "' exists. Calling .iam " + roleToAdd +" will add you to it.")
                await ctx.send(embed=eObj)
                logger.error("[RoleCommands newrole()] "+roleToAdd+" already exists")
                return
        role = await guild.create_role(name=roleToAdd)
        await role.edit(mentionable=True)
        logger.info("[RoleCommands newrole()] "+str(roleToAdd)+" created and is set to mentionable")

        eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="You have successfully created role **`" + roleToAdd + "`**.\nCalling `.iam "+roleToAdd+"` will add it to you.")
        await ctx.send(embed=eObj)

    @commands.command()
    async def deleterole(self, ctx, roleToDelete):
        logger.info("[RoleCommands deleterole()] "+str(ctx.message.author)+" called deleterole with role "+str(roleToDelete)+".")
        roleToDelete = roleToDelete.lower()
        role = discord.utils.get(ctx.guild.roles, name=roleToDelete)
        if role == None:
            logger.info("[RoleCommands deleterole()] role that user wants to delete doesnt seem to exist.")
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Role **`" + roleToDelete + "`** does not exist.")
            await ctx.send(embed=eObj)
            return
        membersOfRole = role.members
        if not membersOfRole:
            deleteRole = await role.delete()
            logger.info("[RoleCommands deleterole()] no members were detected, role has been deleted.")
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Role **`" + roleToDelete + "`** deleted.")
            await ctx.send(embed=eObj)        
        else:
            logger.info("[RoleCommands deleterole()] members were detected, role can't be deleted.")
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Role **`" + roleToDelete + "`** has members. Cannot delete.")
            await ctx.send(embed=eObj)

    @commands.command()
    async def iam(self, ctx, roleToAdd):
        logger.info("[RoleCommands iam()] "+str(ctx.message.author)+" called iam with role "+str(roleToAdd))
        roleToAdd = roleToAdd.lower()
        role = discord.utils.get(ctx.guild.roles, name=roleToAdd)
        if role == None:
            logger.error("[RoleCommands iam()] role doesnt exist.")
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Role **`" + roleToAdd + "**` doesn't exist.\nCalling .newrole " + roleToAdd)
            await ctx.send(embed=eObj)
            return
        user = ctx.message.author
        membersOfRole = role.members
        if user in membersOfRole:
            logger.error("[RoleCommands iam()] " + str(user) + " was already in the role " + str(roleToAdd) + ".")
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Beep Boop\n You've already got the role dude STAAAPH!!")            
            await ctx.send(embed=eObj)
        else:
            await user.add_roles(role)
            logger.info("[RoleCommands iam()] user " + str(user) + " added to role " + str(roleToAdd) + ".")
            
            if(roleToAdd == 'froshee'):
                eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="**WELCOME TO SFU!!!!**\nYou have successfully been added to role **`" + roleToAdd + "`**.")
            else:
                eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="You have successfully been added to role **`" + roleToAdd + "`**.")
            await ctx.send(embed=eObj)
        
    @commands.command()
    async def iamn(self, ctx, roleToRemove):
        logger.info("[RoleCommands iamn()] "+str(ctx.message.author)+" called iamn with role "+str(roleToRemove))
        roleToRemove = roleToRemove.lower()
        role = discord.utils.get(ctx.guild.roles, name=roleToRemove)
        if role == None:
            logger.error("[RoleCommands iam()] role doesnt exist.")
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Role **`" + roleToRemove + "`** doesn't exist.")
            await ctx.send(embed=eObj)
            return
        membersOfRole = role.members
        user = ctx.message.author
        if user in membersOfRole:
            await user.remove_roles(role)
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="You have successfully been removed from role **`" + roleToRemove + "`**.")
            await ctx.send(embed=eObj)
            logger.info("[RoleCommands iamn()] " + str(user) + " has been removed from role " + str(roleToRemove) )
        else:
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="Boop Beep??\n You don't have the role, so how am I gonna remove it????")
            await ctx.send(embed=eObj)
            logger.error("[RoleCommands iamn()] " + str(user) + " wasnt in the role " + str(roleToRemove) )
        
        

    @commands.command()
    async def whois(self, ctx, roleToCheck):
        logger.info("[RoleCommands whois()] "+str(ctx.message.author)+" called whois with role "+str(roleToCheck))
        memberString = ""
        logString = ""
        role = discord.utils.get(ctx.guild.roles, name=roleToCheck)
        if role == None:
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="**`" + roleToCheck + "`** does not exist.")
            await ctx.send(embed=eObj)
            logger.error("[RoleCommands whois()] role "+str(roleToCheck) + " doesnt exist")
            return
        membersOfRole = role.members
        if not membersOfRole:
            logger.error("[RoleCommands whois()] there are no members in the role "+str(roleToCheck))
            eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description="No members in role **`" + roleToCheck + "`**.")
            await ctx.send(embed=eObj)
            return
        for members in membersOfRole:
            name = members.display_name
            memberString += name + "\n"
            logString += name + '\t'
        logger.info("[RoleCommands whois()] following members were found in the role: "+str(logString))
        await ctx.send("Members belonging to role `" + roleToCheck + "`:\n" + "```\n" + memberString + "```")

    @commands.command()
    async def roles(self, ctx):
        logger.info("[Misc roles()] roles command detected from user "+str(ctx.message.author))
        guild = ctx.guild
        rolesList = []
        selfAssignRoles = []
        for role in guild.roles:
            if role.name != "@everyone" and role.name[0] == role.name[0].lower():
                selfAssignRoles.append(str(role.name))
        logger.info("[Misc roles()] selfAssignRoles array populated with the roles extracted from \"guild.roles\"")

        selfAssignRoles = sorted(selfAssignRoles, key=str.lower)
        logger.info("[Misc roles()] roles in arrays sorted alphabetically")

        await paginate(bot=self.bot,title="Self-Assignable Roles" ,ctx=ctx,listToPaginate=selfAssignRoles, numOfPageEntries=10)

    @commands.command()
    async def Roles(self, ctx):
        logger.info("[Misc Roles()] roles command detected from user "+str(ctx.message.author))
        guild = ctx.guild
        assignedRoles = []
        for role in guild.roles:
            if role.name != "@everyone" and role.name[0] != role.name[0].lower():
                assignedRoles.append(str(role.name))

        logger.info("[Misc Roles()] assignedRoles array populated with the roles extracted from \"guild.roles\"")

        assignedRoles = sorted(assignedRoles, key=str.lower)
        logger.info("[Misc Roles()] roles in arrays sorted alphabetically")

        await paginate(bot=self.bot,title="Mod/Exec/XP Assigned Roles" ,ctx=ctx,listToPaginate=assignedRoles, numOfPageEntries=10)
def setup(bot):
    bot.add_cog(RoleCommands(bot))