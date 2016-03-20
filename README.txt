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