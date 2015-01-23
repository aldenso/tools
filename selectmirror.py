#!/usr/bin/env python2
import csv

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

def main():
	count=1
	globalplaces = placesglobal()
	showmenu = {}
	print("### Select Global Location ###")
	for i in globalplaces:
		showmenu[count]=i
		print("({0}) ==> {1}".format(count, i) )
		count=count+1
	answer=0
	while answer == 0:
		try:
			answer = input("Press number of choice and Enter:")
		except Exception as e:
			print("Not in the posibilities {}".format(e))
	if answer:
		selectedglobal = showmenu.get(answer)
		count=1
		localplaces = placeslocal(selectedglobal)
		showmenu = {}
		print("### Select specific Location  ###")
		for i in localplaces:
			showmenu[count]=i
			print("({0}) ==> {1}".format(count, i) )
			count=count+1
		answer=0
		while answer == 0:
			try:
				answer = input("Press number of choice and Enter:")
			except Exception as e:
				print("Not in the posibilities{}".format(e))
		if answer:
			selectedlocal = showmenu.get(answer)
			count=1
			sites = site(selectedglobal,selectedlocal)
			showmenu = {}
			print("### Select specific Site ###")
			for i in sites:
				showmenu[count]=i
				print("({0}) ==> {1}".format(count, i) )
				count=count+1
			answer=0
			while answer == 0:
				try:
					answer = input("Press number of choice and Enter:")
				except Exception as e:
					print("Not in the posibilities{}".format(e))
			if answer:
				selectedsite = showmenu.get(answer)
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

if __name__ == '__main__':
	main()