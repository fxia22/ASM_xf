#!/usr/bin/env python

# NOTE: starting from abook version 0.4.15 it is often more convenient
# to use command line option "--add-email" instead of this script

# mail2abook.py version 0.1
# by Jaakko Heinonen <jheinonen@users.sourceforge.net>
# based on Moritz Moeller-Herrmann's mail2muttalias.py

# Description:
# this script reads all mail adresses from a piped mailfile and
# offers to write them to the ABOOKFILE specified in the script
# Append the following lines or similiar to your muttrc:
# macro pager A |'path to script'/mail2abook.py\n

# Then press A in pager mode to add an address to your abook addressbook

# Here's the original copyright information:

# RELEASE 0.5
##
# Needs python 1.5 and cursesmodule 1.4 by andrich@fga.de (Oliver Andrich)   
# available somewhere on http://www.python.org or directly from
# http://andrich.net/python/selfmade.html
#
# Copyright by Moritz Moeller-Herrmann <mmh@gmnx.net>
#
# Homepage (check for changes before reporting a bug)
# http://webrum.uni-mannheim.de/jura/moritz/mail2muttalias.html 
#
# Use this any way you want. Please inform me of any error/improvement
# and leave the copyright notice untouched.
# No warranties, as this is my first program :-)
# Works for me on Linux with Python 1.5+
# 
# Thanks to Josh Hildebrand for some improvements
##

# Known bugs: 
# If name containing @ is quoted("") before a mail adress, 
# the program will not catch the whole name, 
# but who would alias such an idiot?
# If you get a problem with "unknown variable / keyword error" 
# with KEYUP and KEYDOWN, either get a newer pythoncurses module 
# or change them to lowercase.
#
# Probably some more, mail me if you find one!

import re 
import string, sys, os 
import curses, traceback
import locale
 
locale.setlocale(locale.LC_ALL,os.environ["LANG"])
  
ABOOKFILE=os.environ["HOME"] + "/.abook/addressbook"

try :
	testcurses = curses.KEY_UP
except NameError:
	print "Your pythoncurses module is old. Please upgrade to 1.4 or higher."
	print "Alternative: Modify the script. Change all 6 occurences of curses.KEY_UP"
	print "and similiar to lowercase."

try : testAF = ABOOKFILE #test if ALIASFILE was configured in script
except NameError:
	try: ALIASFILE=os.environ["ABOOKFILE"] #test is environment MUTTALIASFILE was set
	except KeyError:
		print "Please specify ABOOKFILE at beginning of script \nor set environment variable ABOOKFILE"
		print "Aborting ..."
		sys.exit()



###Thanks for the following go to Michael P. Reilly
if not sys.stdin.isatty():  # is it not attached to a terminal?
  file = sys.stdin.read()
  sys.stdin = _dev_tty = open('/dev/tty', 'w+')
  # close the file descriptor for stdin thru the posix module
  os.close(0)
  # now we duplicate the opened _dev_tty file at file descriptor 0 (fd0)
  # really, dup creates the duplicate at the lowest numbered, closed file
  # descriptor, but since we just closed fd0, we know we will dup to fd0
  os.dup(_dev_tty.fileno())  # on UNIX, the fileno() method returns the
                             # file object's file descriptor
else:  # is a terminal
	print "Please use as a pipe!"
	print "Aborting..."
	sys.exit()
# now standard input points to the terminal again, at the C level, not just
# at the Python level.


print "Looking for mail adresses, this may take a while..."


####  define functions


class screenC:
	"Class to create a simple to use menu using curses"
	def __init__(self):
		import curses, traceback
		self.MAXSECT = 0
		self.LSECT = 1
		# Initialize curses
		self.stdscr=curses.initscr()
		# Turn off echoing of keys, and enter cbreak mode,
		# where no buffering is performed on keyboard input
		curses.noecho() 
		curses.cbreak()

		# In keypad mode, escape sequences for special keys
		# (like the cursor keys) will be interpreted and
		# a special value like curses.KEY_LEFT will be returned
		self.stdscr.keypad(1)		
	
	def titel(self,TITEL="Title  - test",HELP="Use up and down arrows + Return"):	
		"Draws Title and Instructions"
		self.stdscr.addstr(0,0,TITEL,curses.A_UNDERLINE)				# Title + Help
		self.stdscr.addstr(self.Y -2 ,0,HELP,curses.A_REVERSE)

	def refresh(self):
		self.stdscr.refresh()

	def size(self):
		"Returns screen size and cursor position"
		#Y, X = 0, 0
		self.Y, self.X = self.stdscr.getmaxyx()
		#self.y, self.x = 0, 0
		self.y, self.x = self.stdscr.getyx()
		#print Y, X
		return self.Y, self.X, self.y, self.x
		

	def showlist(self,LISTE,LSECT=1):
		"Analyzes list, calculates screen, draws current part of list on screen	"
		s = self.Y -3								#space on screen
		self.MAXSECT=1
		while len(LISTE) > self.MAXSECT * s :		# how many times do we need the screen?
			self.MAXSECT = self.MAXSECT +1
			
		if self.LSECT > self.MAXSECT:				#check for end of list
			self.LSECT = LSECT -1
		
		if self.LSECT <=	0: 						# 
			self.LSECT =1		
		
		if len(LISTE) <= s:
			self.LISTPART=LISTE
		
		else :
			self.LISTPART=LISTE[s * ( self.LSECT -1 ) : s * self.LSECT ]	# part of the List is shown
		
		self.stdscr.addstr(self.Y -2, self.X -len(`self.LSECT`+`self.MAXSECT`) -5, "(" + `self.LSECT` + "/" + `self.MAXSECT` + ")")
		#if len(LISTE) > self.Y - 3:
		#	return 1
		for i in range (1, self.Y -2):			# clear screen between title and help text
			self.stdscr.move(i , 0)
			self.stdscr.clrtoeol()
		for i in range (0,len(self.LISTPART)):		# print out current part of list
			Item = self.LISTPART[i]
			self.stdscr.addstr(i +1, 0, Item[:self.X])
	
	def getresult(self,HOEHE):
		"Get Result from cursor position"
		RESULT= self.LISTPART[(HOEHE -1)]
		return RESULT
	
	def showresult(self, HOEHE, DICT={}):
		"Look up result to show in dictionary if provided, return list member otherwise"
		if DICT=={}:
			return self.getresult(HOEHE)
		else :
			return string.join(DICT[self.getresult(HOEHE)], " || ")
		

	
	def menucall(self, LISTE, DICT={}, TITEL="",HELP="Use up and down arrows, Return to select"):
		"Takes a list and offers a menu where you can choose one item, optionally, look up result in dictionary if provided"
		REFY=1
		self.__init__()
		self.size()
		self.titel(TITEL,HELP)
		self.showlist(LISTE)
		self.refresh()
		self.stdscr.move(1,0)
		while 1:									# read Key events 
			c = self.stdscr.getch()
			self.size()
			
			#if c == curses.KEY_LEFT and self.x  > 0:
			#	self.stdscr.move(self.y, self.x -1); REFY = 1 # REFY == refresh: yes
			
			#if c == curses.KEY_RIGHT		and self.x < self.X -1:
			#	#if x < 4 and LENGTH - ZAHLY > y - 1: 
			#	self.stdscr.move(self.y, self.x + 1); REFY = 1
			
			if c == curses.KEY_UP or c == 107: #up arrow or k
				if self.y > 1:
					self.stdscr.move(self.y -1, self.x); REFY = 1
				else :
					self.LSECT=self.LSECT-1
					self.showlist(LISTE,self.LSECT)
					self.stdscr.move(len(self.LISTPART), 0)
					REFY = 1
				
			if c == curses.KEY_DOWN or c == 106: #down arrow or j
				
				if self.y < len(self.LISTPART) :	
					self.stdscr.move(self.y +1, self.x); REFY = 1

				else :
					self.LSECT=self.LSECT+1
					self.showlist(LISTE,self.LSECT)
					self.stdscr.move(1,0)
					REFY = 1
			
			if c == curses.KEY_PPAGE:
				self.LSECT=self.LSECT-1
				self.showlist(LISTE,self.LSECT)
				self.stdscr.move(1, 0)
				REFY = 1

			if c == curses.KEY_NPAGE:
				self.LSECT=self.LSECT+1
				self.showlist(LISTE,self.LSECT)
				self.stdscr.move(1,0)
				REFY = 1

			if c == curses.KEY_END:
				self.LSECT=self.MAXSECT
				self.showlist(LISTE,self.LSECT)
				self.stdscr.move(1,0)
				REFY = 1
			
			if c == curses.KEY_HOME:
				self.LSECT=1
				self.showlist(LISTE,self.LSECT)
				self.stdscr.move(1,0)
				REFY = 1


			if c == 10 : 				# \n (new line)
				ERG = self.getresult(self.y )
				self.end()
				return ERG
			
			if c == 113 or c == 81: 		# "q or Q"
				self.printoutnwait("Aborted by user!")
				self.end()
				sys.exit()
				return 0
				
			if REFY == 1:
				REFY = 0
				self.size()
				self.stdscr.move(self.Y -1, 0)
				self.stdscr.clrtoeol()
				self.stdscr.addstr(self.Y -1, 0, self.showresult(self.y,DICT)[:self.X -1 ], curses.A_BOLD)
				self.stdscr.move(self.y, self.x)
				self.refresh()

	def end(self):
		"Return terminal"
		# In the event of an error, restore the terminal
		# to a sane state.
		self.Y, self.X, self.y, self.x = 0, 0, 0, 0
		self.LISTPART=[]
		self.stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		#traceback.print_exc()

	def input(self,	promptstr):
		"raw_input equivalent in curses, asks for  Input and returns it"
		self.size()
		curses.echo()
		self.stdscr.move(0,0)
		self.stdscr.clear()
		self.stdscr.addstr(promptstr)
		self.refresh()
		INPUT=self.stdscr.getstr()
		curses.noecho()
		return INPUT
	
					
	def printoutnwait(self, promptstr):
		"Print out Text, wait for key"
		curses.noecho()
		self.stdscr.move(0,0)
		self.stdscr.clear()
# The new Mutt client pauses after running the script already.  No reason
# to pause twice.  -Josh
#		self.stdscr.addstr(promptstr+"\n\n(press key)")
#		self.refresh()
#		c = self.stdscr.getch()# read Key events 
		


def listrex (str, rgx): # Return a list of all regexes matched in string
	"Search string for all occurences of regex and return a list of them."
	result = []
	start = 0 # set counter to zero
	ende =len (str) #set end position
	suchadress = re.compile(rgx,re.LOCALE)#compile regular expression, with LOCALE
	while 1:
		einzelerg = suchadress.search(str, start,ende) #create Match Object einzelerg
		if einzelerg == None:#until none is found
			break
		result.append(einzelerg.group()) #add to result
		start = einzelerg.end()
	return result

def strrex (str): # Return first occurence of regular exp  as string
	"Search string for first occurence of regular expression and return it"
	muster = re.compile(r"<?[\w\b.ßüöä-]+\@[\w.-]+>?", re.LOCALE)	#compile re
	matobj = muster.search(str)		#get Match Objekt from string 
	if muster.search(str) == None:		#if none found
		return ""
	return matobj.group()			#return string 

def stripempty (str):#Looks for all empty charcters and replaces them with a space
	"Looks for all empty charcters and replaces them with a space,kills trailing"
	p = re.compile( "\s+")		#shorten
	shrt = p.sub(" ", str)
	q = re.compile("^\s+|\s+$")	#strip
	strp = q.sub("", shrt)
	return strp

def getmailadressfromstring(str):
	"Takes str and gets the first word containing @ == mail adress"
	StringSplit=string.split(str)
	for i in range(len(StringSplit)):
		if "@" in StringSplit[i]:
			return StringSplit[i]
	return None

### main program

OCCLIST = listrex(file, '"?[\s\w\ö\ä\ü\-\ß\_.]*"?\s*<?[\w.-]+\@[\w.-]+>?')#get list, RE gets all Email adresses + prepending words

if OCCLIST:
	print len(OCCLIST),"possible adresses found!." 
else: 
	print"ERROR, no mails found"
	sys.exit()


for i in range(len(OCCLIST)):			#strip all whitespaces + trailing from each list member
	OCCLIST[i] = string.strip(OCCLIST [i])


OCCDIC={} 						# Dictionary created to avoid duplicates
for i in range(len(OCCLIST)): 			# iterate over 
	d = OCCLIST[i]
	Mail = getmailadressfromstring(OCCLIST[i])
			#strrex(OCCLIST[i])			#Mailadresse
	Schnitt = - len(Mail) 				#cut off mail adress
	Mail = string.replace(Mail, "<", "")#remove <>
	Mail = string.replace(Mail, ">", "")
	Name = string.replace (stripempty (d[:Schnitt]), '"', '')		#leaves name
	if not OCCDIC.get(Mail):			# if new Emailadress
		Liste = []						# create list for names
		Liste.append(Name)				# append name 
		OCCDIC[Mail] = Liste			# assign list to adress
	else : 	
		Liste = OCCDIC[Mail]			# otherwise get list
		Liste.append(Name)				# append name to list of names
		OCCDIC[Mail] =  Liste			# and assign


KEYS = OCCDIC.keys()				#iterate over dictionary, sort names 
									#KEYS are all the adresses

for z in range( len(KEYS) ): 
	NAMLIST = OCCDIC[KEYS[z]]		# Get list of possible names
	d = {} 							# sort out duplicates and 
									# remove bad names + empty strings from adresses
	for x in NAMLIST: 
		if x in ["", "<"]: continue
		d[x]=x
	NAMLIST = d.values()
	NAMLIST.sort()					# sort namelist alphabetically
	print z, KEYS[z], "had possible names:", NAMLIST # Debugging output
	OCCDIC[KEYS[z]] = NAMLIST 		# 

print "\n"

###sorting

def Comparelength(x, y):
	"Compare number of names in OCCDIC, if equal sort alphabetically."
	if len(OCCDIC[y]) == len(OCCDIC[x]):
		return cmp(x, y)
	if len(OCCDIC[y]) < len(OCCDIC[x]):
		return -1
	else:
		return 1	

KEYS.sort(Comparelength)					# Keys sort

###menu

ScreenObject=screenC()			# initialize curses menu
try:
	ZIELADRESS = ScreenObject.menucall(KEYS, OCCDIC, "Choose adress to alias")
	if OCCDIC[ZIELADRESS]:
		LISTNAM=["***ENTER own NAME"]		#add option to edit name
		LISTNAM= LISTNAM + OCCDIC[ZIELADRESS]
		ZIELNAME   = ScreenObject.menucall(LISTNAM, {}, ZIELADRESS + " has which of the possible names?")
		# empty Dictionary {} means show list member itself, not looked up result
	else : ZIELNAME=""
except:
	T=ScreenObject.size()
	ScreenObject.end()
#	traceback.print_exc() # Uncomment for curses debugging info
#	print T
	sys.exit()

### enter new names/aliases

if  ZIELNAME == "***ENTER own NAME" or ZIELNAME == "":
	ZIELNAME = ScreenObject.input(`ZIELADRESS` + " = " + `OCCDIC[ZIELADRESS]` + "\n" + `ZIELADRESS` + " gets which name? ")

if ZIELNAME == "":
	ZIELNAME = "No name"

WRITEALIAS = "\n[]\nname=" + ZIELNAME + "\nemail=" + ZIELADRESS + "\n\n"

f = open(ABOOKFILE, "a")
f.write(WRITEALIAS)
f.close()

ScreenObject.printoutnwait("Item was added to "+  ABOOKFILE + "\nProgam terminated")
ScreenObject.end()

