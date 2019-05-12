from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import multiprocessing
import requests
import json
from itertools import product
from string import ascii_lowercase

import pyexcel
#setting
api_url = 'https://domain-registry.appspot.com/check?domain='
domain_ltd = '.dev'
#generate 3 char domainascii_lowercase
alphabets = ['a', 'b', 'c'] 
domain_length= 1

#generator
gen_domain=map(''.join, product(ascii_lowercase, repeat=domain_length))
domain_list =list(gen_domain)
#domain_name = "abc"
result_list=[]

#functions
def is_available(a):
	if a is True:
		return "Available"
	else:
		return "Not available"
def find_domain(domain):
	request_url = api_url+domain+domain_ltd
	response = requests.get(request_url)
	json_data = json.loads(response.content)
	json_data['domain'] = domain+domain_ltd
	print(json_data['domain']  +" is " + is_available(json_data['available'] ))
	result_list.append(json_data)
	

with PoolExecutor(max_workers =multiprocessing.cpu_count()) as executor:
	for _ in executor.map(find_domain,domain_list):
		pass


print("Saving on CSV file...")
# https://github.com/pyexcel/pyexcel
pyexcel.save_as(records=result_list, dest_file_name="domain_list.csv")
print("Done saving")