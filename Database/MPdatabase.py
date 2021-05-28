import sqlite3
import hashlib


# This class is of MasterTable where app password(hashed) and email is stored in masterTable 
class PMPDatabase:
	def __init__(self):
		try:
			self.connect = sqlite3.connect("pwmdatabase.db")
			self.cursor = self.connect.cursor()
		except Exception as e:
			print(e)

	# This will create masterTable (which is done in passwordManagerApp.py file)
	def createTable(self):
		qCreate = """
			CREATE TABLE IF NOT EXISTS masterTable (masterPass varchar(200), email varchar(100))
		"""
		self.cursor.execute(qCreate)
		self.connect.commit()

	# This will hash the password and insert it along with email entered
	def insertIntoTable(self, mp, em):

		bytesMP = bytes(mp, 'utf-8')
		hashedMP = hashlib.sha256(bytesMP).hexdigest()

		qInsert = """
			INSERT INTO masterTable (masterPass, email)
			VALUES (?, ?)
		"""
		self.cursor.execute(qInsert, (hashedMP, em))
		self.connect.commit()

	# This will update the existing password(hashed) instead of making a new row in database
	# This is called in resetPassFrame.py
	def updateIntoTable(self, mp):
		mail = self.getMail()		
		bytesMP = bytes(mp, 'utf-8')
		hashedMP = hashlib.sha256(bytesMP).hexdigest()

		qUpdate = """
			UPDATE masterTable SET masterPass = ? WHERE email = ?
		"""
		self.cursor.execute(qUpdate, (hashedMP, mail))
		self.connect.commit()


	# This is used to check whether there is an existing user in passwordManagerApp.py
	# If user exists:
		# -> if True: setupFrame is raised
		# -> if False: loginFrame is raised
	def isEmpty(self):
		qCount = """
			SELECT COUNT(*) FROM masterTable
		"""
		self.cursor.execute(qCount)
		entries = self.cursor.fetchall()
		if (entries[0][0] == 0):
			return True
		return False

	# This is used in loginFrame.py to check the password with database
	def loginCheck(self, mp):
		bytesMP = bytes(mp, 'utf-8')
		hashedMP = hashlib.sha256(bytesMP).hexdigest()

		qSelect = """
			SELECT * FROM masterTable
		"""
		self.cursor.execute(qSelect)
		data = self.cursor.fetchall()

		if hashedMP == data[0][0]:
			return True
		return False

	# This is used in forgotPassFrame.py to check email entered with database
	def mailCheck(self, mail):
		qSelect = """
			SELECT * FROM masterTable
		"""
		self.cursor.execute(qSelect)
		data = self.cursor.fetchall()
		if mail == data[0][1]:
			return True
		return False


	# Used in updateIntoTable() to get mail from databse 
	def getMail(self):
		qSelect = """
			SELECT * FROM masterTable
		"""
		self.cursor.execute(qSelect)
		data = self.cursor.fetchall()
		# print(data[0][1])
		mail = data[0][1]
		return mail