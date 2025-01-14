import os

pre_dir = os.getcwd()

set_index = ['train2017','val2017']

for set_node in set_index:
	label_file = open(set_node+'.txt','w')
	for root,file,files in os.walk(pre_dir+os.sep+'images/'+set_node):
		for file in files:
			if file[-4:] == '.jpg':
				file = os.path.join(pre_dir+os.sep+'images/'+set_node,file)
				label_file.write(file+'\n')
	label_file.close()

