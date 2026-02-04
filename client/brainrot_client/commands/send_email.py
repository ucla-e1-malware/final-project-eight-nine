from ..commands import Command # Required

# import the Python standard library modules for sending email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(sender, recipient, subject, html):
	smtp_server, port = ("e1-mail.acmcyber.com", 32525)
	# Our email server is set up to allow any username/password combo
	# Note that you should never include passwords in your source code in a real app!
	username, password = ("god-of-java-69420", "barbecuespaghetti")

	# Start building a a new "multipart" MIME file
	# (MIME, or "Multipurpose Internet Mail Extensions", is the format that modern email uses)
	message = MIMEMultipart("alternative")
	message["From"] = sender
	message["To"] = recipient
	message["Subject"] = subject

	# Make an HTML email attachment from that string, and attach it to our message
	message.attach(MIMEText(html, "html"))

	# Open up an SMTP (Simple Mail Transfer Protocol) to our server, and send your email!
	with smtplib.SMTP(smtp_server, port) as server:
		server.login(username, password)
		server.sendmail(sender, recipient, message.as_string())


class SendEmail(Command): # Call the class anything you'd like
	"""
	Send an email from a sender address to a recipient address, given a file with the contents of the email.
	This command will prompt you to enter the sender's email address, the recipient's email address, the subject, and a filepath to the email to send.
	"""
	# The text above, known as the docstring, is also shown when using the help command in the terminal

	# When this command is called, do_command() is executed. 
	# Feel free to make additional functions outside the class (like print_brick) and call them!
	def do_command(self, lines: str):
		# tokens = lines.split()

		# if len(tokens) != 4:
		# 	print("Usage: send_email <sender_address> <recipient_address> <subject> <path/to/file>")
		# 	print("Example: send_email eight-nine@e1-mail.acmcyber.com e1-instructors@e1-mail.acmcyber.com \"Enable 2FA\" path/to/email.html")
		# 	return
		
		data = [
			input("> Enter in the sender's address: "),
			input("> Enter in the recipient's address: "),
			input("> Enter in the email's subject: "),
		]
		with open(input("> Enter in the filepath to the contents of the email to send: ")) as f:
			data.append(f.read())
		
		sendEmail(*data)


command = SendEmail # Assign the class you created to the variable called command for the system to find the command!