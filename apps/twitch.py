""" Check a user's Twitch status. """

import requests



def pretty_user_status(nick):
	"""
	get_online_status(string) -> string
	Returns a friendly sentence describing a user's Twitch status
	or the errors it encountered. (bad username, connection issues)
	"""
	
	try:
		status = user_status(nick)
		result = "{user} is {status}.".format(user=nick.capitalize(), status=status)
	
	except UsernameError:
		result = "Sorry, couldn't find a user called {user}.".format(user=nick)

	except requests.exceptions.ConnectionError:
		result = "Sorry, couldn't connect to Twitch."

	return result



def user_status(nick):
	"""
	status(string) -> string
	If the user exists, returns a one word string describing
	their status. (either 'online' or 'offline').
	If there's no such user, raises UsernameError.
	"""

	url="https://api.twitch.tv/kraken/streams/"+nick
	twitch_raw=requests.get(url)
	twitch_json=twitch_raw.json()

	online=twitch_json.get("stream")
	error=twitch_json.get("error")

	if error:
		raise UsernameError
	elif(online):
		return "online"
	else:
		return "offline"



class UsernameError(Exception):
	pass





# JSON formatted
example_responses = {
	'online':

		"""
		user={
		"_links":{
			"self":"https://api.twitch.tv/kraken/streams/jonbams",
			"channel":"https://api.twitch.tv/kraken/channels/jonbams"
			},
		"stream":{
				"_id":17005788080,
				"game":"Team Fortress 2",
				"viewers":595,
				"created_at":"2015-10-15T14:04:18Z",
				"video_height":720,
				"average_fps":59.6598554697,
				"is_playlist":false,
				"_links":{
					"self":"https://api.twitch.tv/kraken/streams/jonbams"
					},
				"preview":{
					"small":"http://static-cdn.jtvnw.net/previews-ttv/live_user_jonbams-80x45.jpg",
					"medium":"http://static-cdn.jtvnw.net/previews-ttv/live_user_jonbams-320x180.jpg",
					"large":"http://static-cdn.jtvnw.net/previews-ttv/live_user_jonbams-640x360.jpg",
					"template":"http://static-cdn.jtvnw.net/previews-ttv/live_user_jonbams-{width}x{height}.jpg"},
				"channel":{
					"_links":{
						"self":"http://api.twitch.tv/kraken/channels/jonbams",
						"follows":"http://api.twitch.tv/kraken/channels/jonbams/follows",
						"commercial":"http://api.twitch.tv/kraken/channels/jonbams/commercial",
						"stream_key":"http://api.twitch.tv/kraken/channels/jonbams/stream_key",
						"chat":"http://api.twitch.tv/kraken/chat/jonbams",
						"features":"http://api.twitch.tv/kraken/channels/jonbams/features",
						"subscriptions":"http://api.twitch.tv/kraken/channels/jonbams/subscriptions",
						"editors":"http://api.twitch.tv/kraken/channels/jonbams/editors",
						"videos":"http://api.twitch.tv/kraken/channels/jonbams/videos",
						"teams":"http://api.twitch.tv/kraken/channels/jonbams/teams"
						},
					"background":null,"banner":null,
					"broadcaster_language":"en",
					"display_name":"JonBams",
					"game":"Team Fortress 2",
					"logo":"http://static-cdn.jtvnw.net/jtv_user_pictures/jonbams-profile_image-b399f10f502bc3b2-300x300.png",
					"mature":true,
					"status":"[Bams] MvM then some unboxing!",
					"partner":true,
					"url":"http://www.twitch.tv/jonbams",
					"video_banner":"http://static-cdn.jtvnw.net/jtv_user_pictures/jonbams-channel_offline_image-1299a344aa2643f1-640x360.png",
					"_id":28252159,
						"name":"jonbams",
					"created_at":"2012-02-16T07:34:11Z",
					"updated_at":"2015-10-15T18:15:50Z","delay":0,"followers":180736,
					"profile_banner":null,
					"profile_banner_background_color":null,
					"views":7089935,"language":"en"
					}
			}
		}
		""",


	'offline':
		"""
		user={
			"_links":{
				"self":"https://api.twitch.tv/kraken/streams/hotform",
				"channel":"https://api.twitch.tv/kraken/channels/hotform"
				},
			"stream":null}
		"""

}