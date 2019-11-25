#!/Users/tomar/Anaconda3/python.exe
"""
Created on Tuesday September 27 2019 by tomar
#!/usr/bin/python3
#!C:\ProgramData\Anaconda3\python.exe#!/Users/tomar/Anaconda3/python.exe
"""
import cgi
import Songs

form = cgi.FieldStorage() # instantiate only once!
q = form.getvalue('q', '3100000')	#remove default
songbook = Songs.Songs()
print("Content-type: text/html \n")
print(Songs.renderHtml(songbook.dataList(q[0],q[1:])))