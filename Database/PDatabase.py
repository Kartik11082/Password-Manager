import sqlite3
from Backend.encryption import EncryptDeCrypt


# This class is of MasterTable where app password(hashed) and email is stored in masterTable 
class siteData:
	def __init__(self):
		try:
			self.connect = sqlite3.connect("pwmdatabase.db")
			self.cursor = self.connect.cursor()
		except Exception as e:
			print(e)

	# This will create masterTable (which is done in passwordManagerApp.py file)
	def createDataTable(self):
		dCreate = """
			CREATE TABLE IF NOT EXISTS data (siteName varchar(200), siteUsername varchar(100), sitePassword text)
		"""
		self.cursor.execute(dCreate)
		self.connect.commit()

	# This will hash the password and insert it along with email entered
	def insertDataTable(self, sn, su, sp):
		en = EncryptDeCrypt()
		esp = en.encrypt_message(sp)

		dInsert = """
			INSERT INTO data (siteName, siteUsername, sitePassword)
			VALUES (?, ?, ?)
		"""
		self.cursor.execute(dInsert, (sn, su, esp))
		self.connect.commit()

	def searchPass(self, searchString):
		en = EncryptDeCrypt()

		dSearchSiteName = "SELECT * FROM data WHERE siteName LIKE '%{}%'".format(searchString)

		self.cursor.execute(dSearchSiteName)
		c = self.cursor.fetchall()
		self.connect.commit()
		if not c:
			return ("")
		
		dsp = en.decrypt_message(c[0][2]).decode('utf-8')
		return (c[0], dsp)

	def deleteDataTable(self, sn):
		dDelete = ("DELETE FROM data WHERE siteName LIKE '%{}%'").format(sn)
		try:
			self.cursor.execute(dDelete)
			self.connect.commit()
		except Exception as e:
			print(e)

	def viewData(self):
		dView = """
			SELECT siteName, siteUsername FROM data 
		"""
		self.cursor.execute(dView)
		self.connect.commit()
		allData = self.cursor.fetchall()
		return allData