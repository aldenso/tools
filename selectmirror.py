#!/usr/bin/env python2
import csv

showmenu1 = {}
showmenu2 = {}
showmenu3 = {}
answer1 = 0
answer2 = 0
answer3 = 0

def placesglobal():
	places=[]
	with open('mirrorlist.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) == 7 and row[6]:
				if row[0] not in places:
					places.append(row[0])
	return places

def placeslocal(placesglobal):
	countries=[]
	with open('mirrorlist.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) == 7 and row[0] == placesglobal and row[6] != "":
				if row[1] not in countries:
					countries.append(row[1])
	return countries

def site(placesglobal, placeslocal):
	org=[]
	with open('mirrorlist.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) == 7 and row[0] == placesglobal and row[1] == placeslocal and row[6] != "":
				if row[2] not in org:
					org.append(row[2])
	return org

def urls(placesglobal, placeslocal, site):
	httpurl=''
	rsyncurl=''
	with open('mirrorlist.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) == 7 and row[0] == placesglobal and row[1] == placeslocal and row[2] == site:
				httpurl = row[4]
				if row[6]:
					rsyncurl = row[6]
	return httpurl, rsyncurl

def showmenuglobal():
	count=1
	globalplaces = placesglobal()
	global showmenu1
	global answer1
	answer1 = 0
	print("### Select Global Location ###")
	for i in globalplaces:
		showmenu1[count]=i
		print("({0}) ==> {1}".format(count, i) )
		count=count+1
	while answer1 == 0:
		try:
			answer1 = input("Press number of choice and Enter:")
			if answer1 not in showmenu1.keys():
				print("#"*30+"\nNot a valid choice\n"+"#"*30)
				showmenuglobal()
			else:
				showmenulocal(showmenu1, answer1)
		except Exception as e:
			print("Not in the posibilities: {}".format(e))

def showmenulocal(showmenu, answer1):
	selectedglobal = showmenu1.get(answer1)
	count=1
	localplaces = placeslocal(selectedglobal)
	global showmenu2
	global answer2
	answer2 = 0
	print("### Select specific Location  ###")
	for i in localplaces:
		showmenu2[count]=i
		print("({0}) ==> {1}".format(count, i) )
		count=count+1
	while answer2 == 0:
		try:
			answer2 = input("(0) ==> Return to previous Menu\n"
				+"Press number of choice and Enter:")
			if answer2 == 0:
				showmenuglobal()
			elif answer2 not in showmenu2.keys():
				print("#"*30+"\nNot a valid choice\n"+"#"*30)
				showmenulocal(showmenu2, answer1)
			else:
				showmenuurl(selectedglobal, showmenu2, answer2)
		except Exception as e:
			print("Not in the posibilities: {}".format(e))

def showmenuurl(selectedglobal, showmenu2, answer2):
	selectedlocal = showmenu2.get(answer2)
	count=1
	sites = site(selectedglobal,selectedlocal)
	global showmenu3
	global answer3
	answer3 = 0
	print("### Select specific Site ###")
	for i in sites:
		showmenu3[count]=i
		print("({0}) ==> {1}".format(count, i) )
		count=count+1
	while answer3 == 0:
		try:
			answer3 = input("(0) ==> Return to previous Menu\n"
				+"Press number of choice and Enter:")
			if answer3 == 0:
				showmenulocal(showmenu2, answer1)
			elif answer3 not in showmenu3.keys():
				print("#"*30+"\nNot a valid choice\n"+"#"*30)
				showmenuurl(selectedglobal, showmenu2, answer2)
			else:
				selectedsite = showmenu3.get(answer3)
				count=1
				useurls = urls(selectedglobal, selectedlocal, selectedsite)
				httpurl, rsyncurl = useurls
				print("Site has the next urls:\n{0}\n{1}".format(httpurl,rsyncurl))
				print("#"*60)
				print("Set the variable urlremoterepo in script createrepolocal:")
				print("#"*60)
				print("@"*60)
				print("urlremoterepo={0}".format(rsyncurl.split(':')[1]))
				print("@"*60)

		except Exception as e:
			print("Not in the posibilities: {}".format(e))


def main():
	showmenuglobal()

if __name__ == '__main__':
	main()