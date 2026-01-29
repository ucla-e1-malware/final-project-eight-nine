from ..commands import Command # Required
    
def print_brick(): # Helper function
    print("BRICK! 🧱")

class SendEmail(Command): # Call the class anything you'd like
    """
    Send an email! TODO
    """
    # The text above, known as the docstring, is also shown when using the help command in the terminal

    # When this command is called, do_command() is executed. 
    # Feel free to make additional functions outside the class (like print_brick) and call them!
    def do_command(self, lines: str):
        print_brick()

command = SendEmail # Assign the class you created to the variable called command for the system to find the command!