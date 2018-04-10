import requests
import logging
import ConfigParser #Python 3 should import configparser
import time
import random


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
config = ConfigParser.ConfigParser()
config.read('config.ini')
merchant_id = config.get('SANDBOX', 'MERCHANT_ID')
api_token = config.get('SANDBOX', 'API_TOKEN')
environment_url = config.get('SANDBOX', "URL")


request_url = environment_url + "/v3/merchants/" + merchant_id + "/orders"

max_attempts = 5
attempts = 0

# Retry attempts should max out after a reasonable number of attemps.
while attempts < max_attempts:
	print (request_url)
	
	# Make a request to Clover REST API
	response = requests.get(request_url, headers = {"Authorization": "Bearer " + api_token})
	
	# Checks if the response is rate limited
	if(response.status_code == 429):
		retry_duration = int(response.headers.get('retry-after'))
		logging.error(response.text + "\n" + str(response.headers))
		time.sleep(retry_duration + random.random()) #Add jitter to sleep duration.
	# Checks if there is another error
	elif(response.status_code>=400):
		logging.error(response.text + "\n" + str(response.headers))
	# If successful, break out of while loop and continue with the rest of the code
	elif response.status_code == 200:
		logging.info(str(response.status_code) + " " + request_url)
		break
	
	attempts = attempts + 1
	if(attempts >= max_attempts):
		logging.error('Failed: Maxed out attempts')