import random


class Otp:
	def __init__(self):
		self.characters = "abcdefghijklmnopqrstuvwxyz0123456789"
		self.OTP = ''

	# Used in forgotPassFrame and setupFrame to generate OTP once
	def generateOTP(self):
		for _ in range(6):
			self.OTP += random.choice(self.characters)
		return self.OTP