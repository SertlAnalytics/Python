# Demo file for Spyder Tutorial
# Hans Fangohr, University of Southampton, UK

def hello():
    """Print "Hello World" and return None"""
    print("Hello World")
    
def hello2():
    "Print 'Hello World' and return None"
    print("Hello World2")
    

def ask_ok(prompt, retries=4, reminder = 'Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)