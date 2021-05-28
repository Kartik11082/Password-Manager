from Frames.resetPassFrame import ResetPassFrame
import tkinter as tk
from Database.MPdatabase import PMPDatabase
from Backend.OTPGenerator import Otp
from Backend.sendMail import SendMail


class ForgotPassFrame(tk.Frame):
	def __init__(self, parent, controller):
		# from loginFrame import LoginFrame
		from Frames.loginFrame import LoginFrame
		tk.Frame.__init__(self, parent)
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
		# To change frame in other functions
		self.controller = controller
		otpObj = Otp()
		self.generatedOTP = otpObj.generateOTP()
		self.forgotPassFrame = tk.LabelFrame(self, text="Forgot Password", bd=5, bg=self.backgroundColor, fg=self.secTextColor)
		self.forgotPassFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.confirmLabel = tk.Label(self.forgotPassFrame, text="Email Sent", bg = self.successColor, fg = self.priTextColor, font=self.labelFont)
		# User will enter email to send OTP to
		self.titleLabel = tk.Label(self.forgotPassFrame, text='Forgot Password ?', bg = self.backgroundColor, fg = self.primaryColor, font=("Rockwell", 18, "bold"))
		self.titleLabel.place(relx=0.25, rely=0.15, relheight=0.1, relwidth=0.5)
		self.emailLabel = tk.Label(self.forgotPassFrame, text='Enter registered email id', bg = self.backgroundColor, fg = self.secTextColor, font=self.labelFont)
		self.emailLabel.place(relx=0.25, rely=0.32, relheight=0.07, relwidth=0.5)
		self.emailentry = tk.Entry(self.forgotPassFrame, width=20, font=self.entryFont, bg=self.surface1Color, fg=self.secTextColor)
		self.emailentry.place(relx=0.25, rely=0.38, relwidth=0.5, relheight=0.05)
		self.emailentry.insert(0, "Enter your Email")
		self.emailentry.focus()
		self.emailentry.delete(0, 'end')
		# Will send OTP to email to verify email
		self.sendOtpButton = tk.Button(self.forgotPassFrame, text="Send OTP", command=self.sendOtp, font=self.labelFont, bg=self.primaryColor, fg=self.secTextColor)
		self.sendOtpButton.place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.07)
		# User will enter OTP here
		self.otpLabel = tk.Label(self.forgotPassFrame, text='Enter Otp', bg = self.backgroundColor, fg = self.secTextColor, font=self.labelFont)
		self.otpLabel.place(relx=0.25, rely=0.56, relheight=0.07, relwidth=0.5)
		self.otpentry = tk.Entry(self.forgotPassFrame, width=20, font=self.entryFont, bg=self.surface1Color, fg=self.secTextColor)
		self.otpentry.place(relx=0.25, rely=0.62, relwidth=0.5, relheight=0.05)
		self.otpentry.bind("<Return>", self.shortcuts)
		# self.otpentry.insert(0, "Enter OTP here")
		self.otpentry.delete(0, 'end')
		# Will call chekOTP function and check the OTP
		self.otpEnterButton = tk.Button(self.forgotPassFrame, text="Enter",	command=lambda: [ self.checkOTP(), self.emailentry.delete(0, 'end'), self.otpentry.delete(0, 'end')], font=self.labelFont, bg=self.primaryColor, fg=self.secTextColor)
		self.otpEnterButton.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.07)
		# Will take back to Login Frame if user changed their mind
		self.backButton = tk.Button(self.forgotPassFrame, text="Back", command=lambda: [self.emailentry.delete(0, 'end'), self.otpentry.delete(0, 'end'), controller.show_frame(LoginFrame)], bg=self.surface2Color, fg=self.secTextColor)
		self.backButton.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.05)
	# Will check OTP generated
	# OTP is generated only once in __init__()
	def checkOTP(self):
		enteredOTP = self.otpentry.get()
		if (enteredOTP == self.generatedOTP):
			self.controller.show_frame(ResetPassFrame)
		else:
			errorLabel = tk.Label(self.forgotPassFrame, text="OTP incorrect", bg = self.errorColor, fg = self.priTextColor, font=self.labelFont)
			errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			errorLabel.after(2000, errorLabel.destroy)

	# Will check the email with database(since changing email is not allowed) and send OTP to the entered email 
	def sendOtp(self):
		mail = self.emailentry.get()
		pdb = PMPDatabase()
		if (not (pdb.mailCheck(mail))):
			errorLabel = tk.Label(self.forgotPassFrame, text="Wrong Email entered",	bg = self.errorColor, fg = self.priTextColor, font=self.labelFont)
			errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
			errorLabel.after(3000, errorLabel.destroy)
			return

		mail = SendMail()
		subject = 'Forgot Password'
		message = "Your OTP for Password Manager is:\n" + str(self.generatedOTP)
		mail.send((self.emailentry.get()), subject, message)

		self.confirmLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
		self.confirmLabel.after(3000, self.confirmLabel.destroy())

	# Shortcut for Enter key 
	def shortcuts(self, event):
		key = event.char
		if key == '\r':
			self.sendOtp()