from discord.ext import commands
import logging
import requests as req
from helper_files.embed import embed 
import helper_files.settings as settings
import json

logger = logging.getLogger('wall_e')


class Misc():

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def poll(self, ctx, *questions):
		logger.info("[Misc poll()] poll command detected from user "+str(ctx.message.author))
		if len(questions) > 12:
			logger.error("[Misc poll()] was called with too many options.")
			await ctx.send("Poll Error:\n```Please only submit a maximum of 11 options for a multi-option question.```")
			return
		elif len(questions) == 1:
			logger.info("[Misc poll()] yes/no poll being constructed.")
			post = await ctx.send("Poll:\n" + "```" + questions[0] + "```")
			await post.add_reaction(u"\U0001F44D")
			await post.add_reaction(u"\U0001F44E")
			logger.info("[Misc poll()] yes/no poll constructed and sent to server.")
			return
		if len(questions) == 2:
			logger.error("[Misc poll()] poll with only 2 arguments detected.")
			await ctx.send("Poll Error:\n```Please submit at least 2 options for a multi-option question.```")
			return
		elif len(questions) == 0:
			logger.error("[Misc poll()] poll with no arguments detected.")
			await ctx.send('```Usage: .poll <Question> [Option A] [Option B] ...```')
			return
		else:
			logger.info("[Misc poll()] multi-option poll being constructed.")
			questions = list(questions)
			optionString = "\n"
			numbersEmoji = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
			numbersUnicode = [u"0\u20e3", u"1\u20e3", u"2\u20e3", u"3\u20e3", u"4\u20e3", u"5\u20e3", u"6\u20e3", u"7\u20e3", u"8\u20e3", u"9\u20e3", u"\U0001F51F"]
			question = questions.pop(0)
			options = 0
			for m, n in zip(numbersEmoji, questions):
				optionString += m + ": " + n +"\n"
				options += 1
			pollPost = await ctx.send("Poll:\n```" + question + "```" + optionString)
			logger.info("[Misc poll()] multi-option poll message contructed and sent.")
			for i in range(0, options):
				await pollPost.add_reaction(numbersUnicode[i])
			logger.info("[Misc poll()] reactions added to multi-option poll message.")

	@commands.command()
	async def urban(self, ctx, *arg):
		logger.info("[Misc urban()] urban command detected from user "+str(ctx.message.author))
		logger.info("[Misc urban()] query string being contructed")
		queryString = ''
		for x in arg:
			queryString += x

		logger.info("[Misc urban()] url contructed for get request")
		url = 'http://api.urbandictionary.com/v0/define?term=%s' % queryString
		urbanUrl = 'https://www.urbandictionary.com/define.php?term=%s' % queryString

		logger.info("[Misc urban()] Get request made")
		res = req.get(url)
		
		if(res.status_code != 404):
			logger.info("[Misc urban()] Get request successful")			
			data = res.json()
		else:
			logger.error("[Misc urban()] Get request failed, 404 resulted")
			data = ''

		data = data['list']
		if not data:
			logger.error("[Misc urban()] sending message indicating 404 result")
			eObj = embed(title="Urban Results", author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, colour=0xfd6a02, description=":thonk:404:thonk:You searched something dumb didn't you?")
			await ctx.send(embed=eObj)
			return
		else:
			logger.info("[Misc urban()] constructing embed object with definition of " + queryString)
			content = [
				['Definition', data[1]['definition']], 
				['Link', '[here](%s)' % urbanUrl]
				]
			eObj = embed(title='Results from Urban Dictionary', author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, colour=0xfd6a02, content=content)
			await ctx.send(embed=eObj)

def setup(bot):
	bot.add_cog(Misc(bot))
