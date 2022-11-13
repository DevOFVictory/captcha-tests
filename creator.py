from captcha.image import ImageCaptcha
import random
import string
from PIL import Image

def randomword():
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(random.randint(5, 7)))
 
image = ImageCaptcha(width = 280, height = 90)
 
captcha_text = randomword() 
 
data = image.generate(captcha_text) 
 
image.write(captcha_text, 'captcha.png')
Image.open("captcha.png").show()

user_input = input('Please enter the captcha: ')

if user_input.strip().upper() == captcha_text:
    print('Correct! You are (probably) not a robot.')
else:
    print('Incorrect! You are (probably) a robot.')

