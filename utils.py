import sqlite3
import asyncio
import discord
from datetime import datetime

def newAdmin(user : discord.Member):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS Admins(member_id)''')
	cursor.execute(f'''INSERT INTO Admins VALUES({user.id})''')

	main.commit()
	cursor.close()
	main.close()

def delAdmin(user : discord.Member):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS Admins(member_id)''')
	cursor.execute(f"SELECT * FROM Admins WHERE member_id = {user.id}")
	result = cursor.fetchone()

	if result:
		cursor.execute(f"DELETE FROM Admins WHERE member_id = {user.id}")

	main.commit()
	cursor.close()
	main.close()

def checkAdmin(user : discord.Member):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS Admins(member_id)''')
	cursor.execute(f"SELECT * FROM Admins WHERE member_id = {user.id}")
	result = cursor.fetchone()

	if result:
		return True
	if not result:
		return False

def checkOwner(user : discord.Member):
	if user.id == 281555678303092738:
		return True
	else:
		return False

def getTime():
	now = datetime.now()
	s1 = now.strftime("%m/%d/%Y, %H:%M")
	return(s1 + " EST")