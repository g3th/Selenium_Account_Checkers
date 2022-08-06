import os
from pathlib import Path

directory = str(Path(__file__).parent)

print('Current Directory: \n{} \n'.format(os.listdir(directory)))

combo_list_name = input('Enter name of combo list: ')

clean_list=[]

with open(combo_list_name, 'r') as disney:
	
	for line in disney.readlines():
			clean_list.append(line.split(' | ')[0])
			
parsed_list_name = input('Enter parsed list name: ')
	
with open(parsed_list_name,'a') as clean:
	for line in clean_list:
		clean.write(line+'\n')

