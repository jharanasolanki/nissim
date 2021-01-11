# Import modules for CGI handling
import cgi, cgitb
import os
# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
link = form.getvalue('link')
qr="python3 formweb.py "+str(link)
os.system(qr)
print("Content-type:text/html")
print
print("")
print("")
print('new page is opened')
