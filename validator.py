import sys

outputText = ""

def validate(num_votes, votes):
	global outputText
	num = int(num_votes)

	vote_list = votes

	opts = vote_list.split(',')
	vote_set = set(opts)
	for vote in vote_set:
		try:
			vote_int = int(vote)
		except:
			log("FAILURE: {} Not an int".format(vote))
	if len(opts) != len(vote_set):
		votebucket = {}
		for vote in opts:
			if votebucket.get(vote) == None:
				votebucket[vote] = 1
			else:
				votebucket[vote] += 1

		for key in votebucket:
			if votebucket[key] > 1:
				log("FAILURE: Has {} copies of vote {}".format(votebucket[key], key))


	i = 0
	if len(vote_set) < num:
		log ("FAILURE: Not enough votes. Expected {}, got {}".format(num, len(vote_set)))

	while(i < num):
	  if (str(i + 1)) not in vote_set:
	  	log ("FAILURE: Option {} not voted on.".format(i + 1))
	  i+=1

	out = outputText
	outputText = ""
	return out

def log(msg):
	global outputText
	print(msg)
	outputText += msg + '\n'

if __name__ == '__main__':
	validate(sys.argv[1], sys.argv[2])