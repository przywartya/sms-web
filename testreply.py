""" Reply generating component """

def get_reply(user_message, phone):
	"""
	Tries to interpret the input from user_message. If the input
	is a valid command, it calls the right app from apps/ with the
	interpreted parameters, and returns its output. (string) If the
	input isn't valid, returns a nice error message. (string)
	"""

	words = user_message.split(' ')
	name = words[-1]
	reply_message = 'hej ' + name

	return reply_message

# About the error message: It should make clear what the error actually is.
# The error cases I could think of:
#
# ---- USER ERRORS ----
# 1) Invalid app
# 2) Valid app, invalid parameters:
#   a) Valid app, can't understand parameters
#   b) Valid app, not enough parameters
#   c) Valid app, too many parameters
# ---- OTHER ERRORS ----
# 3) Valid app, valid parameters, but the app found no results.
#      Example: no results from google search
# 4) The app is currently unavailable (because google maps is down or sth)
