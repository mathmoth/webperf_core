# -*- coding: utf-8 -*-
#from urllib.parse import urlparse # https://docs.python.org/3/library/urllib.parse.html
import subprocess
import json
from models import Rating

def run_test(_, langCode, url):
	"""

	"""
	
	print(langCode, url)

	result = subprocess.run(['pa11y', '--reporter', 'json', url[0][1]], stdout=subprocess.PIPE)
	
	mod_results = result.stdout.decode("utf-8")
	result_list = json.loads(mod_results)
	num_errors = len(result_list)
	return_dict = {}
	
	points = 0
	review_overall = ''
	review = ''
	
	if  num_errors == 0:
		points = 5
		review_overall = '* Webbplatsen har inga uppenbara fel kring tillgänglighet!\n'
	elif num_errors == 1:
		points = 4
		review_overall = '* Webbplatsen kan bli mer tillgänglig, men är helt ok.\n'
	elif num_errors > 8:
		points = 1
		review_overall = '* Väldigt dålig tillgänglighet!\n'
	elif num_errors >= 4:
		points = 2
		review_overall = '* Dålig tillgänglighet.\n'
	elif num_errors >= 2:
		points = 3
		review_overall = '* Genomsnittlig tillgänglighet men kan bli bättre.\n'

	review += '* Antal tillgänglighetsproblem: {} st\n'.format(num_errors)
	return_dict['antal_problem'] = num_errors

	if num_errors > 0:
		review += '\nProblem:\n'
	
	i = 1
	old_error = ''

	for error in result_list:
		err_mess = error.get('message').replace('This', 'A')
		if err_mess != old_error:
			old_error = err_mess
			review += '* {0}\n'.format(err_mess)
			key = error.get('code') #'{0}-{1}'.format(error.get('code'), i)
			return_dict.update( { key : err_mess } )

			i += 1
		
		if i > 10:
			review += '* Info: För många unika problem för att lista alla\n'
			break

	rating = Rating(_)
	rating.set_overall(points, review_overall)
	rating.set_a11y(points, review)
	
	print(points, review, return_dict)
	return (rating, return_dict)

"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
	print(run_test('sv', 'https://webperf.se'))