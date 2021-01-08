import csv
import matplotlib.pyplot as plt



def question_1():
	names =[]
	twitter = []
	facebook =[]
	insta = []
	with open("Data-Quiz3-Q1 - data.csv",'r') as file:
		readcsv = csv.reader(file)
		for row in readcsv:


			names.append(row[0])
			ind = row[1].find('/',9)
			twitter.append(row[1][ind+1:])
			ind = row[2].find('/',9)
			facebook.append(row[2][ind+1:])
			ind = row[3].find('/',9)
			insta.append(row[3][ind+1:])

	net_1 = net_2 = net_3 = 0
	for i in range(len(names)):
		if (twitter[i]!=facebook[i] and facebook[i]!=insta[i] and insta[i]!=twitter[i]):
			net_1+=1
		elif (twitter[i]==facebook[i] and facebook[i] == insta[i]):
			net_3+=1
		else : 
			net_2+=1

	p_1 = net_1*100./len(names)
	p_2 = net_2*100./len(names)
	p_3 = net_3*100./len(names)
	p = []
	p.append(p_1)
	p.append(p_2)
	p.append(p_3)
	hi =[]
	hi.append("Network 1")
	hi.append("Network 2")
	hi.append("Network 3")
	#graph(hi,p)

	# part 2

	name_count =[]

	for i in range(len(names)):
		print(i)
		count = sequence(twitter[i],facebook[i])
		count = count/min(len(facebook[i]),len(twitter[i]))
		name_count.append([names[i],count])


	name_count = sort_list(name_count)
	

	x=[]
	for i in range(len(name_count)):
		x.append(name_count[i][1])

	print(x)
	plt.plot(x)
	plt.ylabel("Normalized LCS")
	plt.xlabel("User in decending order of LCS")
	plt.show()





def sort_list(lt):  
	lt.sort(key = lambda x: x[1],reverse = True)  
	return lt






def sequence(twitter,facebook): 
	len_t = len(twitter) 
	len_f = len(facebook) 
	hello = [[None]*(len_f + 1) for i in range(len_t + 1)] 
  
	for j in range(len_t + 1): 
		for k in range(len_f + 1): 
			if j == 0 or k == 0 : 
				hello[j][k] = 0
			elif twitter[j-1] == facebook[k-1]: 
				hello[j][k] = hello[j-1][k-1]+1
			else: 
				hello[j][k] = max(hello[j-1][k], hello[j][k-1]) 
	return hello[len_t][len_f] 




def graph(hi,p):
	
	plt.bar(hi,p)
	
	plt.ylabel('Percentage')
	plt.xlabel('Networks')
	plt.title('Question 1a')
	plt.show()

question_1()
			