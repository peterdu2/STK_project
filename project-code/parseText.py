# path = '/home/lab/independentStudy/stk-code/cmake_build/example.txt'
#
# f = open(path, 'r')
# lines = f.readlines()
# f.close()

distCenter = []
headings=[]
steers = []


def getData(path):
	print(path)
	distCenter = []
	headings = []
	steers = []
	f = open(path, 'r')
	lines = f.readlines()
	f.close()
	for i, line in enumerate(lines):
		my_list = line.split(",")
		#print(line)
		#speeds.append(float(my_list[0]))
		#print(my_list)
		distCenter.append(float(my_list[0]))
		headings.append(float(my_list[1]))
		steers.append(float(my_list[2]))
	#clf_expert = MLPRegressor(hidden_layer_sizes=(60,40,20))
	return distCenter, headings, steers
