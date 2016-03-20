""" Main part of Ask """

from werkzeug.wrappers import Request, Response
import logging
import requests
from reply import get_reply

# Set up output file for logs
logging.basicConfig(filename='/Apps/MAMP/logs/request.log', level=logging.INFO)
# Make requests output only warnings or errors
logging.getLogger('requests').setLevel(logging.WARNING)



def application(environ, start_response):
	"""
	Main WSGI callable - the function the server calls upon
	receiveing a request.
	Receives an SMS message, calls get_reply (which interprets
	the message and returns an adequate reply) and dispatches
	a reply SMS to the SMSGateway app server. (via a HTTP GET request)
	"""
	request = Request(environ)
	method = request.method
	
	# Our server receives an SMS using a GET Request.
	# I'd use POST if it was my choice, but the
	# creator of SMS Gateway chose GET :(.
	if method == 'GET':
		params = request.args
		
		phone = str(params.get('phone'))
		user_message = str(params.get('text'))
		log("Received", phone, user_message, begin=True)
		
		# call the reply function
		reply_message = get_reply(user_message, phone)
		log("Sent", phone, reply_message, end=True)
		
		if __name__ != '__main__':
			send_sms(phone, reply_message)
		
	#response = Response('', mimetype='text/html')
	response = Response(reply_message, mimetype='text/html')
	return response(environ, start_response)




def send_sms(phone, message):
	""" send_sms(string, string) -> void

	Dispatches a HTTP GET request containing the SMS
	to SMSGateway's server.
	"""
	
	# sms_gateway_url = 'http://192.168.0.102:9090/sendsms'
	sms_gateway_url = 'http://192.168.43.78:6969/sendsms'
	message_params = {'phone': phone, 'text': message}
	
	# Again - not my idea, just what SMSG requires :(
	requests.get(sms_gateway_url, params=message_params)



# might make it more versatile in the future
def log(event, phone, message, begin=False, end=False, line_len=20):
	""" 
	Logs the number and message. Optional args begin and end
	add some separators and spacing.
	"""
	word_len = len(event) + 2 #for two spaces
	left = (line_len - word_len) // 2
	right = line_len - (left + word_len)
	
	
	if begin: logging.info(' ' + '*'*line_len)
	
	logging.info(" {L} {ev} {R} ".format( L=left*'-', ev=event, R=right*'-' ))
	logging.info(" " + phone)
	logging.info(" " + message)
	
	if end: logging.info('\n\n')




if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	server = make_server('localhost', 80, application)
	server.serve_forever()