#!/Users/tomar/Anaconda3/python.exe
"""
Created on Sat May 27 16:34:21 2017 by tomar
#!/usr/bin/python3
#!C:\ProgramData\Anaconda3\python.exe
#!/Users/tomar/Anaconda3/python.exe
"""
import sys
import cgi
import random
sys.path.append("..")
import gUtils
import Users
import Songs

print("Content-type: text/html \n")

print('''
<html><head><title>SongBook</title>
<LINK REL='StyleSheet' HREF='/python/songs.css?{}'  TYPE='text/css' TITLE='ToMarStyle' MEDIA='screen'>
<LINK REL='StyleSheet' HREF='/python/tomar.css?{}'  TYPE='text/css' TITLE='ToMarStyle' MEDIA='screen'>
<link href='//fonts.googleapis.com/css?family=Didact Gothic' rel='stylesheet'>
<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="932688745244-i4vfeap5jgu8id5dagrc49786vvs0qrf.apps.googleusercontent.com">
</head>
<body>
'''.format(random.randrange(9999), random.randrange(9999)))
form = cgi.FieldStorage() # instantiate only once!
gid = form.getvalue('gId', '')	#remove default
name = form.getvalue('gName', '')	#remove default
gMail = form.getvalue('gMail', '')	#remove default
gImg = form.getvalue('gImage', '')	#remove default
oper = form.getvalue('oper','')
#gid = '106932376942135580175'
print('''
<form name="gForm" method="POST" action="#">
<input type="hidden" name="gId" value="{}">
<input type="hidden" name="gName" value="{}">
<input type="hidden" name="gMail" value="{}">
<input type="hidden" name="gImage" value="{}">
<input type="hidden" name="oper">
</form>
'''.format(gid, name, gMail, gImg))
if gid == '':
	gUtils.googleSignIn()
else:
	users = Users.Users()
	authS = users.authenticate(gid, name, gMail, gImg, users.SONGBOOK)		# gets you into songbook public tags
	authA = users.authenticate(gid, name, gMail, gImg, users.ADMIN)			# gets you notes
	authT = users.authenticate(gid, name, gMail, gImg, users.TEA)			# gets you all tags and media
	authF = users.authenticate(gid, name, gMail, gImg, users.FF)			# gets you all tags and media
	if authA[0] == '1':
		perm = 3
	#elif authT[0] == '1' and authF[0] == '1':
	#	perm = 3
	elif authT[0] == '1' or authF[0] == '1':
		perm = 2
	elif authS[0] == '1':
		perm = 1
	else:
		perm = 0
	#perm = 2						#uncomment to test permissions
	print(authS[1])					#banner html
	if perm > 0:
		songbook = Songs.Songs()
		print(songbook.jsFunctions(perm))
	else:
		print('''
Welcome to ToMarGames Friends and Family!<br><br>It looks like you've landed on a page you don't have permission to access.
				''')
print('</body></html>')