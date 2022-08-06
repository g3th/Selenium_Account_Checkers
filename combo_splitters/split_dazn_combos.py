import os
from pathlib import Path

directory = str(Path(__file__).parent)

print('Current Directory: \n{} \n'.format(os.listdir(directory)))

combo_list_name = input('Enter name of combo list: ')

clean_list=[]
country = []

with open(combo_list_name, 'r') as disney:
	
	for line in disney.readlines():
		try:
			clean_list.append(line.split(' | ')[0])
			country.append(line.split(' | ')[3])
		except IndexError:
			continue
			
parsed_list_name = input('Enter parsed list name: ')
	
with open(parsed_list_name,'a') as clean:
	for index in range(len(clean_list)):
		try:
			clean.write('{} | {}\n'.format(clean_list[index], country[index]))
		except IndexError:
			clean.write('{}\n'.format(clean_list[index]))
			continue

