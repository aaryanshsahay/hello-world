######################################## LIBRARIES ##################################################

import discord
import time
from datetime import datetime
#Machine-Learning Libraries
import numpy as np
import matplotlib.pyplot as plt
# Linear Regression
from sklearn.linear_model import LinearRegression
# Neural Networks
from keras.models import model_from_json
from keras import models
import cv2
#Movie Recommendation
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#Misc
import urllib.request
import pickle
import re



bot=discord.Client()
bot_key='ODM0NzQ2MzkzODY3NTgzNDg5.YIFYKQ.DqBbwzqMxcLLJZfXZ6GJgehQI4Y'

######################################################################################################
######################################## BOT EVENTS ##################################################
######################################################################################################

@bot.event
async def on_ready():
	print('Logged in as {}'.format(bot))

@bot.event
async def on_message(message):

	# Ignore messages sent by bot
	if message.author==bot.user:
		return

	# Greeting 
	if message.content.startswith('!hello') or message.content.startswith('!hi') or message.content.startswith('!hey'):
		embed=discord.Embed(description=greeting_message.format(message.author))
		await message.channel.send(embed=embed)


######################################################################################################
######################################## FUNCTIONS ###################################################
######################################################################################################


######################################################################################################
######################################## FILE PATH ###################################################
######################################################################################################



######################################################################################################
######################################## MESSAGES ####################################################
######################################################################################################

greeting_message='Hello there {} :wave: Glad to meet you! Use !help to get started quickly.'


bot.run(bot_key)
