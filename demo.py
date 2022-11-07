from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

##################################################### Loading the model ##################################################### 
model=SentenceTransformer('bert-base-nli-mean-tokens')

##################################################### Flask ################################################################  
app = Flask(__name__)

##################################################### Functions ###########################################################
def embed_questions(sentences):
	'''
	Embeds a list of sentences.

	Input : List of sentences -> questions

	Output: Array of (len(sentences),768)
	'''
	embed=model.encode(sentences)
	return embed

def convert_query(query,embed_questions,answers):
	'''
	Takes a query, converts it into vector space of (1,768), checks cosine sim with all embedded questions, returns the maximum index and a response.

	Input: query (string) , embedded questions (list) , responses (list)

	Output: response and score_index (-> index of max value of cosine sim else a string if max value is below the threshold)
	'''
	embed=model.encode(query)
	
	
	scores=cosine_similarity([embed],questions_embed)
	score=scores[0].tolist()
	score_index=score.index(max(score))

	if score[score_index]<=0.75:
		res='Sorry I couldnt get you, try framing it in a different way!'
		score_index='nonint'
		
	else:
		res=answers[score_index]
	

	return res,score_index
	
##################################################### Lists ##################################################### 
questions=[
	'What is the location of the store',
	'what time does it operate',
	'Tell me about the new product',
	'what all products do you have',
	'tell me about muscleblaze biozyme whey',
	'tell me about dymatize protein',
	'tell me about muscletech nitrotech whey',
	'tell me about gold standard whey',
	]

answers=[
		'*Pro-Gains : Everything Protein and More* \n Located on Palm Beach Mall, Sector - 50 (new), Seawoods, Navi Mumbai. Location : {}'.format('https://goo.gl/maps/7McRnsnbYkJ9jPig8'),
		'Our shops operate from 11 am till 10 pm, Monday through Saturday! We also offer Home Delivery services and  have membership benefits.',
		'The hottest new product is the new MuscleTech NitroTech Performance Series - 4\n\nNitro-Tech is a scientifically engineered whey protein powder designed for anyone looking to build more muscle, improve their strength and enhance overall performance. Nitrotech from MuscleTech contains pure whey protein isolate and peptides as the primary source. \n- 30 grams of ultra-pure whey protein.\n- 6.9 grams of Branched Chain Amino Acids (BCAAs).\n- 3-gram dose of creatine.\n-it contains 1g of carbohydrate, 1g of sugar and 1.5g of total fat per serving.',
		'Currently we have the following products *in stock*:\n1)MuscleBlaze Biozyme\n2)Dymatize\n3)Muscletech Nitrotech\n4)Gold Standard\n\n For more information you can ask me about the iterms individually!',
		'*MuscleBlaze Biozyme Whey*\n\nMuscleBlaze ® Biozyme Performance Whey is a Labdoor, USA tested & certified whey protein formulation with the highest possible grading of A+ for its all-accurate claims & purity. Launched in a delicious Rich Chocolate flavour\n- 25 g of Protein.\n-5.51 g of BCAA.\n-11.75 g of EAA.\n-4.38 g of Glutamic acid.\n-130.72 of Kcal(per serving).',
		'*Dymatize ISO-100 Protein*\n\n(Helps in gaining lean muscle. Increases your energy level. Helps in building and repairing your muscles and it provides 5.5g of Branched Chain Amino Acids (BCAAs) per serving which helps in fast recovery post intense exercise sessions.\n-Protein    25 g.\n-BCAA    5.5 g.\n-Calories    120.\n-BCAA per Serving)   5.5 g.\n-Number of Servings    71.',
		'*MuscleTech NitroTech Whey Performance Series - 4*\n\nNitro-Tech is a scientifically engineered whey protein powder designed for anyone looking to build more muscle, improve their strength and enhance overall performance. Nitrotech from MuscleTech contains pure whey protein isolate and peptides as the primary source.\n- 30 grams of ultra-pure whey protein.\n- 6.9 grams of Branched Chain Amino Acids (BCAAs).\n- 3-gram dose of creatine.\n-it contains 1g of carbohydrate, 1g of sugar and 1.5g of total fat per serving.  ',
		'*Gold Standard Whey*\n\nOptimum Nutrition Gold Standard 100% Whey Protein 5 lb Double Rich Chocolate comes with whey protein isolate and ultra-filtered whey protein concentrate, which provide support in the development of lean muscle.\n-Protein per Serving    24 g.\n-BCAA    5.5 g.\n-Glutamic acid    4 g\n-Kcal    117.\n-Vegetarian.',
		'Greetings! Welcome to *Pro-Gains* 💪🏽 \nwhere you can find everything protein.\nWe have whey protein of various different brands.(eg. Dymatize,Muscletech,Gold Standard etc).\n\nIf you have any queries related to our products then you can message us here. Your message will be replied here in the FAQ system(in whatsapp). Since this is an automated message reply, so please be elaborative in your questions.\nUse command "help" if you get stuck! Thanks for reaching Pro-Gains protein world!',
		"Here's all the possible questions you can ask me:\n1)What is the location of the store?\n2)what time does it operate?\n3)Tell me about the new product.\n4)what all products do you have?\n5) You can even ask me about individual products."
		]

answers_media=[
			None,
			None,
			None,
			None,
			'https://img2.hkrtcdn.com/9990/prd_998921-MuscleBlaze-Biozyme-Whey-Isolate-4.4-lb-Ice-Cream-Chocolate_o.jpg',
			'https://m.media-amazon.com/images/I/413GuC4J4FL.jpg',
			'https://m.media-amazon.com/images/I/81UYTN3kHjL._SY450_.jpg',
			'https://m.media-amazon.com/images/I/71uwfbcAkYL._AC_SX425_.jpg',
			None,
			None,
			
			]

##################################################### Embedding Questions ##################################################### 
questions_embed=embed_questions(questions)


##################################################### Logic ###################################################################
@app.route('/bot', methods=['POST'])
def bot():
	incoming_msg=request.values.get('Body','').lower()
	resp=MessagingResponse()
	msg=resp.message()
	responded=False
	# Gretting message
	if 'hi' in incoming_msg or 'hello' in incoming_msg or  'hey' in incoming_msg:
		msg.body(answers[-2])
		responded=True
	# Helper command
	elif 'help' in incoming_msg:	
		msg.body(answers[-1])
		responded=True
	# All cases except greeting and help
	else:
		# If query is too short
		if len(incoming_msg.split()) <= 2:
			msg.body('Sorry I couldnt get you, try elaborating it!')
			responded=True
		# If query is too long
		elif len(incoming_msg.split())>=9:
			msg.body('Question is too long, try removing some extra words!')
			responded=True
		# If query is of appropriate length->
		else:
			# Running logic on user query
			pred_query=convert_query(incoming_msg,embed_questions,answers)
			# If score_index returns a string i.e 'nonint' -> error message : 'try framing it in a different way'
			if type(pred_query[1])==str:
				msg.body(pred_query[0])
				responded=True
			# If score_index returns an int -> 
			else:
				# If media file is not present
				if answers_media[pred_query[1]]==None:
					msg.body(pred_query[0])
					responded=True
				# if media file is present
				else:
					msg.body(pred_query[0])
					msg.media(answers_media[pred_query[1]])
					responded=True 
	
				
	if not responded:
		msg.body('Something went wrong TOOT TOOT oops~')

	return str(resp)

if __name__ == '__main__':
    app.run()
