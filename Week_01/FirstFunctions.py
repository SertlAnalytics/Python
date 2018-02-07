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
        
        
i = 5

def f(arg=i):
    print(arg)
    
i = 7

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")
    
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

''' 
cheeseshop("Limburger", "It's very runny, sir.",
   "It's really very, VERY runny, sir.",
   shopkeeper="Michael Palin",
   client="John Cleese",
   sketch="Cheese Shop Sketch")
'''