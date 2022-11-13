from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import whisper
import requests
import warnings
import subprocess
import contextlib


warnings.filterwarnings("ignore", category=DeprecationWarning) 

url = 'https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php'
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(url)
print('\n\n====== Captcha Solver started! ======\n\n')
time.sleep(5)

input('\n\nPress ENTER to solve the captcha.')

print('Finding the captcha element...')
frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to.frame(frames[0])
time.sleep(1)
driver.find_element_by_class_name('recaptcha-checkbox-border').click()
driver.switch_to.default_content()
frames = driver.find_element_by_xpath('/html/body/div/div[4]').find_elements_by_tag_name('iframe')
driver.switch_to.frame(frames[0])
time.sleep(1)
print('Switching to the audio challenge...')
driver.find_element_by_id('recaptcha-audio-button').click()
driver.switch_to.default_content()
frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to.frame(frames[-1])
time.sleep(1)

print('Getting audio url...')

src = driver.find_elements_by_tag_name('a')[0].get_attribute('href')
print('Downloading audio...')

with contextlib.redirect_stdout(None):
    command = 'curl --output "audio.mp3" "[URL]"'

    subprocess.call(command.replace('[URL]', src), shell=True)

print('Loading openai whisper model...')
with contextlib.redirect_stdout(None):
    model = whisper.load_model('tiny')

print('Transcribing audio...')
with contextlib.redirect_stdout(None):
    result = model.transcribe("audio.mp3")
    text = result['text']
print('Successfully transcribed audio: ' + text)

print('Sending text to input field...')
driver.find_element_by_id('audio-response').send_keys(text)
driver.find_element_by_id('audio-response').send_keys(Keys.ENTER)

print('\nDone! :)')
