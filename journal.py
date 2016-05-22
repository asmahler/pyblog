#!/usr/bin/env python

from collections import OrderedDict
import datetime
import os 
import sys


from peewee import * 

db = SqliteDatabase('diary.db')


class Entry(Model):
	content = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now) 

	class Meta: 
		database = db 


def initialize():
	#create table and tb is they don't exist
	db.connect()
	db.create_tables([Entry], safe=True)

def clear():
	os.system('cls' if os.name =='nt' else 'clear') 

def menu_loop():
	#show the menu
	choice = None

	while choice != 'q':
		clear()
		print("Enter 'q' to quit")
		for key, value in menu.items():
			print("{}) {}".format(key,value.__doc__))
		choice = raw_input('Action: ').lower().strip()

		if choice in menu:
			clear()
			menu[choice]()

def add_entry():
	#add an entry 
	'''Add an entry '''
	print("Enter your entry.Press ctrl+d when finished.")
	data = sys.stdin.read().strip()

	if data:
		if raw_input("Save entry? [Yn] ").lower() != 'n':
			Entry.create(content=data)
			print('Saved Succesfully!')


def view_entries(search_query=None):
	#view an entry
	'''View all entries'''
	entries = Entry.select().order_by(Entry.timestamp.desc())
	if search_query:
		entries = entries.where(Entry.content.contains(search_query))
	for entry in entries:
		timestamp = entry.timestamp.strftime('%A %B %d, %Y %I :%M%p')
		clear()
		print(timestamp)
		print('\n\n' + '-'*len(timestamp))
		print(entry.content)
		print('N) next entry')
		print('d) delete entry')
		print('q) return to main menu')

		next_action = raw_input("Action: [Ndq] ")
		if next_action == 'q':
			break
		elif next_action =='d':
			delete_entry(entry)

def search_entries():
	'''Search Entries for a String.'''
	view_entries(raw_input("Search query: "))


def delete_entry(entry):
	#delete an entry 
	'''Delete an entry'''
	if raw_input("Are you sure yN").lower() == 'y':
		entry.delete_instance()
		print('Entry deleted')


menu = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('s', search_entries)
	])


if __name__ == '__main__':
	initialize()
	menu_loop()
	

