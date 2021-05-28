from sqlite3.dbapi2 import SQLITE_ALTER_TABLE
import tkinter as tk
from Frames.forgotPassFrame import ForgotPassFrame
from Database.MPdatabase import PMPDatabase


class LoginFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		#colors
		self.primaryColor = '#4479ff'
		self.backgroundColor = '#000000'
		self.surface1Color = '#121212'
		self.surface2Color = '#212121'
		self.successColor = '#03dac6'
		self.errorColor = '#cf6679'
		self.priTextColor = '#000000'
		self.secTextColor = '#ffffff'

		#fonts
		self.labelFont = ("Rockwell", 12, "bold")
		self.entryFont = ("Rockwell", 16)

		self.controller = controller

		self.loginFrame = tk.LabelFrame(self, text="Login", bd=5, bg=self.backgroundColor, fg=self.secTextColor)
		self.loginFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.titleLabel = tk.Label(self.loginFrame, text='Password Manager', bg = self.backgroundColor, fg = self.primaryColor, font=("Rockwell", 20, "bold"))
		self.titleLabel.place(relx=0.25, rely=0.2, relheight=0.1, relwidth=0.5)
		self.epassLabel = tk.Label(self.loginFrame, text='Enter password', bg = self.backgroundColor, fg = self.secTextColor, font=self.labelFont)
		self.epassLabel.place(relx=0.35, rely=0.37, relheight=0.07, relwidth=0.3)
		self.mpassentry = tk.Entry(self.loginFrame, show = "*", width = 20, font = self.entryFont, bg=self.surface1Color, fg=self.primaryColor)
		self.mpassentry.place(relx=0.25, rely=0.45, relwidth=0.5, relheight=0.07)
		self.mpassentry.bind("<Return>", self.shortcuts)
		self.mpassentry.delete(0, 'end')
		self.mpassenter = tk.Button(self.loginFrame, text = "Enter", bg=self.primaryColor, fg=self.secTextColor, command = lambda: self.checkPass(), font = self.labelFont)
		self.mpassenter.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.07)
		self.forgotPass = tk.Button(self.loginFrame, text = "Forgot Password", bg=self.surface2Color, fg=self.secTextColor, command = lambda: controller.show_frame(ForgotPassFrame))
		self.forgotPass.place(relx=0.4, rely=0.7, relwidth=0.2, relheight=0.05)


	# Shortcut for Enter key 
	def shortcuts(self, event):
		key = event.char
		if key == '\r':
			self.checkPass()

	# Check entered password with database (Pending: raises next frame) 
	def checkPass(self):
		mp = self.mpassentry.get()
		pdb = PMPDatabase()
		if (pdb.loginCheck(mp)):
			confirmLabel = tk.Label(self.loginFrame, text = "Login Successful", font = self.labelFont, bg = self.successColor, fg=self.priTextColor)
			confirmLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			confirmLabel.after(2000, confirmLabel.destroy)
			self.mpassentry.delete(0, 'end')
			from Frames.homeFrame import HomeFrame
			self.controller.show_frame(HomeFrame)
			return
		errorLabel = tk.Label(self.loginFrame, text = "Wrong Password... try again", font = self.labelFont, bg = self.errorColor, fg = self.priTextColor)
		errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
		errorLabel.after(2000, errorLabel.destroy)