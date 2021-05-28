import tkinter as tk
from tkinter.constants import LEFT
from Database.MPdatabase import PMPDatabase
from Backend.OTPGenerator import Otp
from Backend.sendMail import SendMail


class SetupFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		# colors
		self.primaryColor = '#4479ff'
		self.backgroundColor = '#000000'
		self.surface1Color = '#121212'
		self.surface2Color = '#212121'
		self.successColor = '#03dac6'
		self.errorColor = '#cf6679'
		self.priTextColor = '#000000'
		self.secTextColor = '#ffffff'

		# fonts
		self.entryFont = ("Rockwell", 12)
		self.labelFont = ("Rockwell", 12, "bold")

		self.controller = controller
		otpObj = Otp()
		self.generatedOTP = otpObj.generateOTP()

		self.setupFrame = tk.LabelFrame(self, text="Setup", bg=self.backgroundColor, fg=self.secTextColor)
		self.setupFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.titleLabel = tk.Label(self.setupFrame, text='Setup', bg = self.backgroundColor, fg = self.primaryColor, font=("Rockwell", 18, "bold"))
		self.titleLabel.place(relx=0.25, rely=0.1, relheight=0.1, relwidth=0.5)
		# User will enter email for the first time
		self.emailLabel = tk.Label(self.setupFrame, bd = 2, text = "Email", bg=self.backgroundColor, fg=self.secTextColor, font = self.labelFont)
		self.emailLabel.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.07)
		self.emailentry = tk.Entry(self.setupFrame, width = 20, font = self.entryFont, bg=self.surface1Color, fg=self.secTextColor)
		self.emailentry.place(relx=0.25, rely=0.26, relwidth=0.5, relheight=0.05)
		self.emailentry.delete(0, 'end')
		# Will send OTP to verify Email
		self.sendOtpButton = tk.Button(self.setupFrame, text="Send OTP", command=self.sendOtp, bg=self.primaryColor, fg=self.secTextColor,	font=self.labelFont)
		self.sendOtpButton.place(relx=0.35, rely=0.34, relwidth=0.3, relheight=0.07)
		# Will check the entered OTP with generated OTP
		# User will enter OTP from the email
		self.otpLabel = tk.Label(self.setupFrame, bd = 2, text = "OTP", bg=self.backgroundColor, fg=self.secTextColor, font = self.labelFont)
		self.otpLabel.place(relx=0.25, rely=0.43, relwidth=0.5, relheight=0.07)
		self.otpentry = tk.Entry(self.setupFrame, width=20, font=self.entryFont, bg=self.surface1Color, fg=self.secTextColor)
		self.otpentry.place(relx=0.25, rely=0.49, relwidth=0.5, relheight=0.05)
		self.otpentry.delete(0, 'end')
		self.otpEnterButton = tk.Button(self.setupFrame, text="Check OTP",	command=lambda: [self.checkOTP()], font=self.labelFont, bg=self.primaryColor, fg=self.secTextColor)
		self.otpEnterButton.place(relx=0.35, rely=0.57, relwidth=0.3, relheight=0.06)
		# User will enter the password for the first time
		self.passLabel = tk.Label(self.setupFrame, text = "Password", font = self.labelFont, bg=self.backgroundColor, fg=self.secTextColor)
		self.passLabel.place(relx=0.25, rely=0.66, relwidth=0.5, relheight=0.07)
		self.passentry = tk.Entry(self.setupFrame, show = "*", width = 20, bd = 2, font = self.entryFont, bg=self.surface1Color, fg=self.secTextColor)
		self.passentry.place(relx=0.25, rely=0.72, relwidth=0.5, relheight=0.05)
		self.passentry.delete(0, 'end')
		# Will insert email and password to database
		self.enter = tk.Button(self.setupFrame, text = "Enter", bg=self.primaryColor, fg=self.secTextColor, font = self.labelFont, command = lambda:[self.insertPass(self.checkOTP())])
		self.enter.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.07)

	# Will check the entered OTP with otpStatus from checkOTP()
	def insertPass(self, otpStatus):
			from Frames.loginFrame import LoginFrame
			try:
				db = PMPDatabase()
				em = self.emailentry.get()
				mp = self.passentry.get()
				if(otpStatus == True):
					# print("otp is true")
					db.insertIntoTable(mp, em)
					confirmInsertLabel = tk.Label(self.setupFrame, text = "Successful", bg = self.successColor, fg = self.priTextColor, font = self.labelFont)
					confirmInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
					confirmInsertLabel.after(2000, confirmInsertLabel.destroy)
					self.controller.show_frame(LoginFrame)
				else:
					# print("otp is false")
					errorInsertLabel = tk.Label(self.setupFrame, text = "Try again!", bg = self.errorColor, fg = self.priTextColor, font = self.labelFont)
					errorInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
					errorInsertLabel.after(2000, errorInsertLabel.destroy)
					self.emailentry.delete(0, 'end')
					self.passentry.delete(0, 'end')
					self.otpentry.delete(0, 'end')
			except:
				errorInsertLabel = tk.Label(self.setupFrame, text = "Database Error Try again", bg = self.errorColor, fg = self.priTextColor, font = self.labelFont)
				errorInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
				errorInsertLabel.after(2000, errorInsertLabel.destroy)
			finally:
				self.emailentry.delete(0, 'end')
				self.passentry.delete(0, 'end')
				self.otpentry.delete(0, 'end')

	# Check the OTP with generated OTP and return True or False
	def checkOTP(self):
		enteredOTP = self.otpentry.get()
		if (enteredOTP == self.generatedOTP):
			# print("OTP Correct")
			confirmOtpLabel = tk.Label(self.setupFrame, text = "OTP Correct", bg = self.successColor, fg = self.priTextColor, font = self.labelFont)
			confirmOtpLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			confirmOtpLabel.after(2000, confirmOtpLabel.destroy)
			return True
		else:
			# print("OTP Incorrect")
			wrongOtpLabel = tk.Label(self.setupFrame, text = "OTP Incorrect", bg = self.errorColor, fg = self.priTextColor, font = self.labelFont)
			wrongOtpLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			wrongOtpLabel.after(2000, wrongOtpLabel.destroy)
			return False

	# Send mail with generated OTP
	def sendOtp(self):
		try:
			mail = SendMail()
			subject = 'OTP Verification'
			message = "Your OTP for Password Manager is:\n" + str(self.generatedOTP)
			mail.send((self.emailentry.get()), subject, message)
			mailLabel = tk.Label(self.setupFrame, text="Otp Sent", font=self.labelFont, bg = self.successColor, fg = self.priTextColor)
			mailLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			mailLabel.after(6000, mailLabel.destroy())
			# print("OTP send")
		except:
			mailErrorLabel = tk.Label(self.setupFrame, text="Error in Sending mail", font=self.labelFont, bg = self.errorColor, fg = self.priTextColor)
			mailErrorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			mailErrorLabel.after(6000, mailErrorLabel.destroy())
			# print("OTP NOT send")