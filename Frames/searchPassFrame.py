import tkinter as tk
from Database.PDatabase import siteData
from Backend.passwordGenerator import Pgenerator


class SearchPassFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		from Frames.homeFrame import HomeFrame
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
		self.entryFont = ("Rockwell", 12)
		self.labelFont = ("Rockwell", 12, "bold")
		self.Gobj = Pgenerator()
		self.Pobj = siteData()
		self.searchPassFrame = tk.LabelFrame(self, text="Search Password", bd=5, bg=self.backgroundColor, fg=self.secTextColor)
		self.searchPassFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.titleLabel = tk.Label(self.searchPassFrame, text='Search Password', bg = self.backgroundColor, fg = self.primaryColor, font=("Rockwell", 18, "bold"))
		self.titleLabel.place(relx=0.25, rely=0.12, relheight=0.1, relwidth=0.5)
		self.searchLabel = tk.Label(self.searchPassFrame, text='Enter the website name', bg=self.backgroundColor, fg=self.secTextColor, font=self.labelFont)
		self.searchLabel.place(relx=0.05, rely=0.25, relheight=0.05)
		self.siteText = tk.Entry(self.searchPassFrame, width=25, bg=self.surface1Color, fg=self.secTextColor, font=self.entryFont)
		self.siteText.place(relx=0.05, rely=0.3, relheight=0.05, relwidth=0.75)
		self.searchBtn = tk.Button(self.searchPassFrame, text='Q', bg='#03dac5', fg=self.priTextColor, command=self.searchPass, font=self.labelFont)
		self.searchBtn.place(relx=0.85, rely=0.2875, relheight=0.075, relwidth=0.075)
		self.siteLabel = tk.Label(self.searchPassFrame, text='Webite name', bg=self.surface2Color, fg=self.secTextColor)
		self.siteLabel.place(relx=0.05, rely=0.4, relheight=0.05, relwidth=0.425)
		self.usernameLabel = tk.Label(self.searchPassFrame, text='Website Username', bg=self.surface2Color, fg=self.secTextColor)
		self.usernameLabel.place(relx=0.525, rely=0.4, relheight=0.05, relwidth=0.425)		
		self.passLabel = tk.Label(self.searchPassFrame, text='Password', bg=self.surface2Color, fg=self.secTextColor)
		self.passLabel.place(relx=0.28, rely=0.5, relheight=0.05, relwidth=0.425)
		self.copyBtn = tk.Button(self.searchPassFrame, text = "Copy", command=self.copy, bg=self.surface2Color, fg=self.secTextColor)
		self.copyBtn.place(relx=0.36, rely=0.6, relheight=0.05, relwidth=0.12)		
		self.deleteBtn = tk.Button(self.searchPassFrame, text = "Delete", command=self.deletePass, bg=self.errorColor, fg=self.priTextColor) # , font = self.labelFont
		self.deleteBtn.place(relx=0.54, rely=0.6, relwidth=0.11, relheight=0.05)
		self.homeBtn = tk.Button(self.searchPassFrame, text = "Home", command=lambda:[self.siteText.delete(0, "end"), self.siteLabel.config(text="Site"), self.usernameLabel.config(text="Username"), self.passLabel.config(text="Password"),controller.show_frame(HomeFrame)], bg=self.primaryColor, fg=self.secTextColor, font = self.labelFont)
		self.homeBtn.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.08)

	def searchPass(self):
		returnedData = self.Pobj.searchPass(self.siteText.get())
		if returnedData != "": 
			self.siteLabel.config(text = "Site: "+returnedData[0][0])
			self.usernameLabel.config(text = "Username: "+returnedData[0][1])
			self.passLabel.config(text = "Password: "+returnedData[1])
		else:
			invalidLabel = tk.Label(self.searchPassFrame, text = "Invalid Site Name ", bg=self.errorColor, fg=self.secTextColor, font = self.labelFont)
			invalidLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			invalidLabel.after(2000, invalidLabel.destroy)

	def copy(self):
		# print("password copied")
		p = (self.passLabel['text']).split(" ")
		
		self.Gobj.c2c(p[1])
		self.usernameLabel.config(text = "Username")
		self.siteLabel.config(text = "Site")
		self.passLabel.config(text = "Password")
		self.siteText.delete(0, 'end')

	def deletePass(self):
		dataToDelete = ((self.siteLabel['text']).split(" "))[1]
		self.Pobj.deleteDataTable(dataToDelete)
		deleteLabel = tk.Label(self.searchPassFrame, text = "Site details deleted ", bg=self.successColor, fg=self.priTextColor, font = self.labelFont)
		deleteLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
		deleteLabel.after(2000, deleteLabel.destroy)
		self.siteText.delete(0, "end")
		self.siteLabel['text'] = "Website Name"
		self.usernameLabel['text'] = "Username"
		self.passLabel['text'] = "Password"