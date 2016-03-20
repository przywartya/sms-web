I did not write any code on the SMS-SERVER side!!!
My code is only the "apps" folder!!!

This application allows user to use the internet through SMS.
How?
```
We use SMSGateaway application on Android to POST the SMS data
on our web server, then we collect the data, run the appropriate
module and send information back to the user.
```

In other words:
```
With this app you can: search google or wikipedia, check the rout
on google maps or check if your streamer is available on twitch.

You send and SMS to the Android device ( with SMSGateaway configured).
And in couple of seconds you receive requested information.
```


```
# SMSSync Config (for werkzeug):
- HTTP Method: POST
- Data Format: URLEncoded


# Apache Config:
# in MAMP, go to MAMP/conf/apache/httpd.conf
# and add this to the end.

WSGIScriptAlias /ask "C:/Users/lubieowoce/Documents/ask/wrapper.wsgi"

<Directory "C:/Users/lubieowoce/Documents/ask">
Order allow,deny
Allow from all
</Directory>
```
