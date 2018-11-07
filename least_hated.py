import collections
import os
import sys

class Voter:
	def __init__(self, id, votes, name):
		self.id = id
		self.votes = votes
		self.name = name

class Option:	
	def __init__ (self, id, name):
		self.id = id
		self.name = name

def CreateVoters(path):
	voteFile = open(path, 'r')
	voters = []
	currentUserId = 0

	line = voteFile.readline()
	while line:
		splitVotes = line.split(',')
		name = splitVotes[0]
		splitVotes = splitVotes[1:]

		splitVotes[len(splitVotes) - 1] = splitVotes[len(splitVotes) - 1].strip('\n')

		votes = [int(vote) for vote in splitVotes]
		currentUserId += 1
		voters.append(Voter(currentUserId, votes, name))
		
		line = voteFile.readline()

	voteFile.close()
	for voter in voters:
		log("{}: {}".format(voter.name, voter.votes))
	log("")
	return voters


def CreateOptions(path):
	optionFile = open(path, 'r')
	options = []
	currentOptionId = 0
	
	line = optionFile.readline()
	while line:
		line = line.strip('\n')
		log(line)
		currentOptionId += 1
		options.append(Option(currentOptionId, line))
		

		line = optionFile.readline()

	optionFile.close()
	log("")
	return options

def determineLeastHatedFirstFridayOption(options, voters):	
	opt = determineLeastHatedFirstFridayOptionNumber(options, voters)
	if opt != None:
		return options[opt - 1]
	else:
		return None

def determineLeastHatedFirstFridayOptionNumber(options, voters):
	numOptions = len(options)

	#iterate from the bottom to the top of the votes
	for i in range(numOptions -1, 0, -1):
		if(i < len(voters[0].votes)):
			processRowOfVotes(options, voters, i)		

	if len(voters[0].votes) != 0:
		return returnMostCommonElementInLastRow(voters)
	else:
		return None



def processRowOfVotes(options, voters, i):
	row = [voter.votes[i] for voter in voters]
	log ('Process vote row {0}'.format(row))
	voteCounter = collections.Counter(row)
	mostCommon = voteCounter.most_common()
	maxVoted = mostCommon[0][1]		
	mostHateds = [x for x, y in mostCommon if y == maxVoted]
	log('Most hated option(s) are {0}'.format([option.name for option in options if option.id in mostHateds]))
	voters = removeMostHatedFromVotes(voters, mostHateds)
	if len(voters[0].votes) != 0:
		printStateOfVoterVotes(voters)

def removeMostHatedFromVotes(voters, mostHateds):
	for mostHated in mostHateds:
		for voter in voters:
			voter.votes.remove(mostHated)
	if len(voters[0].votes) == 0:
		enterSuddenDeath(voters, mostHateds)
	return voters

def enterSuddenDeath(voters, mostHateds):
	log("There has been a tie! Entering sudden death! The contestants are:")
	index = 1
	for contestant in mostHateds:
		log("{}: {}".format(index, options[contestant - 1].name))
		index += 1
	log("Please re-vote on these {} contestants!\n".format(len(mostHateds)))

def returnMostCommonElementInLastRow(voters):
	return collections.Counter([voter.votes[0] for voter in voters]).most_common()[0][0]

def printStateOfVoterVotes(voters):
	for voter in voters:
	 log ('{0}: {1} '.format(voter.name, voter.votes))

def run(optionsFile, inputFile):
	global outputText
	options = CreateOptions(optionsFile)
	voters = CreateVoters(inputFile)
	winner = determineLeastHatedFirstFridayOption(options, voters)
	if winner is not None:
		log('And the winner is...{0}'.format(winner.name))
	out = outputText
	outputText = ""
	return out

def log(msg):
	global outputText
	print(msg)
	outputText += msg + '\n'

outputText = ""
if __name__ == '__main__':	
	if (len(sys.argv) != 3):
		print("ERROR: Must provide Options and Input. python least_hated.py <path-to-options> <path-to-input>")
	optionsFile = sys.argv[1]
	inputFile = sys.argv[2]
	run(optionsFile, inputFile)

