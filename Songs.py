#!/Users/tomar/Anaconda3/python.exe
"""
Created on Sat May 27 16:34:21 2017 by tomar
#!/usr/bin/python3
#!C:\ProgramData\Anaconda3\python.exe#!/Users/tomar/Anaconda3/python.exe
"""
import json
import sys
import codecs
import urllib

try:
	import gUtils
	import utils
except:
	sys.path.append("..")
	import gUtils
	import utils
def renderHtml(x):
	# for greek
	if sys.stdout.encoding == 'UTF_8':
		return(x.encode('UTF_8', 'xmlcharrefreplace').decode('utf8'))
	else:
		return(x.encode('ascii', 'xmlcharrefreplace').decode('utf8'))
def encodeHtml(x):
	return urllib.parse.unquote(x, encoding='utf-8', errors='replace') 
def noDupes(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

class Songs(object):
	def __init__(self):
		'''
cardDict records are lists of:
[0] title
[1] deck
[2] list of tags -- from the notes table
[3] wikipedia link
[4] lyrics link
[5] time
[6] songbook -- file name in media folder
[7] notes --from the notes table
tag types:
	A artist
	B beats per minute
	C collection
	G genre
	H hit chart position peak
	K key
	M miscellaneous musical things
	O capo position
	S source
	Y year
	Z harmonica key
		'''
		with codecs.open("marieSongBook.json",'r',encoding='utf8') as cards:
			cardDict = json.load(cards)
		self.tagGroup = {"A":"Artist",
						"B":"BPM",
						"C":"Collection",
						"G":"Group",
						"H":"Chart",
						"K":"Key",
						"M":"Music",
						"O":"Capo",
						"S":"People",
						"Y":"Year",
						"Z":"Harmonica"}
		self.tagOrder = ["A", "Y", "G", "H", "C", "K", "B", "M", "O", "Z", "S"]
		self.tagDict = {}		# type: {tag: [id, id, id]}
		self.deckDict = {}		# dict: {"songs":[],"tags":[],"color":""}
		self.songDict = {}		# each entry is a dict version of the list loaded from json
		self.publicTags = ["A", "C", "H", "Y"]
		self.marked = []   #not using yet -- need to look at colored flags too
		for c in cardDict:
			self.songDict[c] = {}
			self.songDict[c]["Title"] = cardDict[c][0]
			self.songDict[c]["Deck"] = cardDict[c][1]
			self.songDict[c]["Tags"] = cardDict[c][2]
			self.songDict[c]["Wiki"] = cardDict[c][3]
			self.songDict[c]["Lyrics"] = cardDict[c][4]
			self.songDict[c]["Time"] = cardDict[c][5]
			self.songDict[c]["SB"] = cardDict[c][6]
			self.songDict[c]["Notes"] = cardDict[c][7]
			if self.songDict[c]["Deck"] not in self.deckDict:
				self.deckDict[self.songDict[c]["Deck"]] = {}		
				self.deckDict[self.songDict[c]["Deck"]]["songs"] = []
				self.deckDict[self.songDict[c]["Deck"]]["tags"] = []
			self.deckDict[self.songDict[c]["Deck"]]["songs"].append(c)
			for t in self.songDict[c]["Tags"]:
				type = t[0:1]
				tag = t[1:]
				if "marked" == t:
					self.marked.append(c)
#				elif type not in self.tagOrder:
#					print("unknown type {}".format(type))
				if type in self.tagDict:
					if tag in self.tagDict[type]:
						self.tagDict[type][tag].append(c)
					else:
						self.tagDict[type][tag] = [c]
					self.deckDict[self.songDict[c]["Deck"]]["tags"].append(t)
				else:
					#print("type is {}, tag is {}, c is {}".format(type, tag, c))
					self.tagDict[type] = {}
					self.tagDict[type][tag] = [c]
		# ultimately, i'd like to sort this in descending length of list
		for type in self.tagDict:
			for tag in self.tagDict[type]:
				self.tagDict[type][tag] = sorted(self.tagDict[type][tag])
		deckColors = ["lightgreen","azure","beige","lightblue","lightcyan","lightpink"]
		dCnt = 0
		for d in sorted(self.deckDict):
			self.deckDict[d]["color"] = deckColors[dCnt]
			dCnt += 1
	
	def jsFunctions(self, perm):
		returnHtml = ''
		returnHtml += '''
<table border=1><tr><td width=50%>		
<input type="text" id="searchBox" list="searchList" onClick="javascript:doSearch();" style="font-size:24px; width:400px; color: darkgreen; background-color: lightgreen;" placeHolder="search">
<input type="button" style="font-size:24px; color:lightgreen; background-color:darkgreen" value="Search" onClick="javascript:doSearch();">
<input type="button" style="font-size:24px; color:azure; background-color:cornflowerblue;" value="Clear" onClick="javascript:doClear();">
'''
		returnHtml += '</td><td><table border=1><tr>'
		for d in sorted(self.deckDict):
			dLink = '''<a href="javascript:getDeck('{}');">{}</a>'''.format(d, d)
			returnHtml += '''
<td style="background-color: {}; padding: 5px;">{} ({})<input type="checkbox" onchange=javascript:getDataList() id="c{}" checked></td>
				'''.format(self.deckDict[d]["color"], dLink, len(self.deckDict[d]["songs"]),d)
		returnHtml += '</tr></table></td></tr></table><div id="datalistDiv">'
		returnHtml += self.dataList(perm, '111111111'[0:len(self.deckDict)])
		returnHtml += '''</div>'''
		if perm == 3:						#modal to show notes
			returnHtml += '''
<div id="myModal" class="modal">
  <!-- Modal content -->
  <div class="modal-content">
    <span class="close">×</span>
    <p id="nDisplay">filler</p>
  </div>
</div>
'''
		returnHtml += '''
<script>
var lastSortedCol = -1;
function goTo(x)
{
	gForm.action = x;
	gForm.submit();
}
function doClear()
{
	document.getElementById("searchBox").value = '';
	document.getElementById("searchBox").focus();
}
// open media file in new window
function showMedia(x)
{
	window.open('/python/media/' + x);
}
function sortTable(col)
{
	//alert("coming in to sort " + col + ", last sorted was " + lastSortedCol);
	var table, rows, switching, i, x, y, shouldSwitch;
	table = document.getElementById("detailTable");
	switching = true;
	/*Make a loop that will continue until no switching has been done:*/
	while (switching)
	{
		switching = false;
		rows = table.getElementsByTagName("TR");
		/*Loop through all table rows (except the first, which contains table headers):*/
		for (i = 1; i < (rows.length - 1); i++)
		{
			shouldSwitch = false;
			/*Get the two elements you want to compare, one from current row and one from the next:*/
			x = rows[i].getElementsByTagName("TD")[col];
			y = rows[i + 1].getElementsByTagName("TD")[col];
			//check if the two rows should switch place:
			if (lastSortedCol == col)
			{
				if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase())
				{
					//if so, mark as a switch and break the loop:
					shouldSwitch= true;
					break;
				}
			}
			else if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase())
			{
				//if so, mark as a switch and break the loop:
				shouldSwitch= true;
				break;
			}
		}
		if (shouldSwitch)
		{
			/*If a switch has been marked, make the switch and mark that a switch has been done:*/
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
		}
	}
	lastSortedCol = col;
}
function openLink(x)
{
	window.open(x);
}
function doSearch(tag)
{
	if (typeof(tag) == "undefined")
	{
		tag = document.getElementById("searchBox").value;
	}
	//alert("tag is " + tag);
	if (tag > '')
	{
		var xhttp = new XMLHttpRequest();
  		xhttp.onreadystatechange = function() 
		{
    		if (this.readyState == 4 && this.status == 200) 
			{
     			document.getElementById("searchResults").innerHTML = this.responseText;
				doClear();	 
    		}
 		};
	 	xhttp.open("POST", "srchResults.py?q=" + tag, true);
 		xhttp.send();
	}
}	
function getDeck(d)
{
	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() 
	{
    	if (this.readyState == 4 && this.status == 200) 
		{
     		document.getElementById("searchResults").innerHTML = this.responseText;
			doClear();	 
    	}
 	};
'''
		returnHtml += 'tag = checkDecks() + "{}d" + d; '.format(perm)
		returnHtml += ''' 
 	xhttp.open("POST", "srchResults.py?q=" + tag, true);
 	xhttp.send();
}	
function getDataList()
{
	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() 
	{
    	if (this.readyState == 4 && this.status == 200) 
		{
     		document.getElementById("datalistDiv").innerHTML = this.responseText;
			doClear();	 
    	}
 	};
	g = checkDecks();
'''
		returnHtml += '''
 	xhttp.open("POST", "dataList.py?q={}" + g, true);
		'''.format(perm)
		returnHtml += '''
 	xhttp.send();
}	
document.getElementById("searchBox").focus();
function checkDecks() 
{ 
	var val = ""; 
'''
		for d in sorted(self.deckDict):
			returnHtml += '/* in deckDict loop for {} */\n'.format(d)
			returnHtml += 'if (document.getElementById("c{}").checked == true) '.format(d)
			returnHtml += '''
	{
		val += '1';
	}
	else
	{
		val += '0';
	}
			'''
		returnHtml += '''
	return val;
}	'''
		if perm == 3:
			returnHtml += '''
// Get the modal, the close element, and the nDisplay element
var modal = document.getElementById('myModal');
var span = document.getElementsByClassName("close")[0];
var nDisplay = document.getElementById('nDisplay');
// When the user clicks on <span> (x), close the modal
span.onclick = function()
{
	modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event)
{
	if (event.target == modal)
	{
		modal.style.display = "none";
	}
}
// When the user clicks the button, open the modal
function showNote(x)
{
	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() 
	{
    	if (this.readyState == 4 && this.status == 200) 
		{
			nDisplay.innerHTML = this.responseText;
			modal.style.display = "block";
    	}
 	};
 	xhttp.open("GET", "getNote.py?q="+x, true);
 	xhttp.send();
}
'''			
		returnHtml += '''
</script>
<div id="searchResults">
</div>
'''
#		print(returnHtml)
		return renderHtml(returnHtml)
	def tagsToUse(self, perm):
		if perm == 1:
			return self.publicTags[:]
		else:
			return self.tagOrder[:]
	# deckString defaults to all decks turned on
	def dataList(self, perm, deckString):
		returnHtml = '<datalist id="searchList">'
		for s in sorted(self.deckFilter(deckString)):
			returnHtml += '''<option value="{}{}X{}">Song: X{}</option>'''.format(deckString, perm, s, self.songDict[s]["Title"]) 
		for t in sorted(self.tagFilter(deckString, perm)):
			returnHtml += '''<option value="{}{}{}">{}: {}({})</option>'''.format(deckString, perm, encodeHtml(t), self.tagGroup[t[0]],t, len(self.tagDict[t[0]][t[1:]]))
		returnHtml += "</datalist>"
		return returnHtml
	def deckFilter(self, deckString):
		possibles = []
		for d in sorted(self.deckDict):
			if deckString[0] == '1':
				possibles += self.deckDict[d]["songs"]
			deckString = deckString[1:]
		return noDupes(possibles)
	def tagFilter(self, deckString, perm):
		possibles = []
		for d in sorted(self.deckDict):
			if deckString[0] == '1':
				for p in self.deckDict[d]["tags"]:
					if p[0] in self.tagsToUse(perm):
						possibles.append(p)
			deckString = deckString[1:]
		return noDupes(possibles)
#s = Songs()
#j = s.dataList(3)