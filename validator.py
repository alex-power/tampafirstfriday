import sys

num = int(sys.argv[1])

vote_list = sys.argv[2]

opts = vote_list.split(',')
vote_set = set(opts)

if len(opts) != len(vote_set):
	print ("FAILURE: Detected duplicate vote.")
	votebucket = {}
	for vote in opts:
		if votebucket.get(vote) == None:
			votebucket[vote] = 1
		else:
			votebucket[vote] += 1

	for key in votebucket:
		if votebucket[key] > 1:
			print("Has {} copies of vote {}".format(votebucket[key], key))


i = 0
if len(vote_set) < num:
	print ("FAILURE: Not enough votes")

while(i < num):
  if (str(i + 1)) not in vote_set:
  	print ("Option {} not voted on.".format(i + 1))
  i+=1
