import random
import subprocess


class Pgenerator(object):
	def __init__(self):
		self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%*()"
		self.Pass = ''

	# Used in forgotPassFrame and setupFrame to generate OTP once
	def generatePass(self):
		for _ in range(10):
			self.Pass += random.choice(self.characters)
		return self.Pass

	def c2c(self, txt):
		cmd='echo '+(txt).strip()+'|clip'
		return subprocess.check_call(cmd, shell=True)