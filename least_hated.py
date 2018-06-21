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
		print("{}: {}".format(voter.name, voter.votes))

	return voters


def CreateOptions(path):
	optionFile = open(path, 'r')
	options = []
	currentOptionId = 0
	
	line = optionFile.readline()
	while line:
		print(line)
		currentOptionId += 1
		options.append(Option(currentOptionId, line))
		

		line = optionFile.readline()

	optionFile.close()

	return options

def determineLeastHatedFirstFridayOption(options, voters):	
	return options[determineLeastHatedFirstFridayOptionNumber(options, voters) - 1]

def determineLeastHatedFirstFridayOptionNumber(options, voters):
	numOptions = len(options)

	#iterate from the bottom to the top of the votes
	for i in range(numOptions -1, 0, -1):
		if(i < len(voters[0].votes)):
			processRowOfVotes(options, voters, i)		

	return returnMostCommonElementInLastRow(voters)


def processRowOfVotes(options, voters, i):
	row = [voter.votes[i] for voter in voters]
	print ('Process vote row {0}'.format(row))
	voteCounter = collections.Counter(row)
	mostCommon = voteCounter.most_common()
	maxVoted = mostCommon[0][1]		
	mostHateds = [x for x, y in mostCommon if y == maxVoted]
	print('Most hated option(s) are {0}'.format([option.name for option in options if option.id in mostHateds]))
	voters = removeMostHatedFromVotes(voters, mostHateds)
	printStateOfVoterVotes(voters)

def removeMostHatedFromVotes(voters, mostHateds):
	for mostHated in mostHateds:
		for voter in voters:
			voter.votes.remove(mostHated)
	return voters

def returnMostCommonElementInLastRow(voters):
	return collections.Counter([voter.votes[0] for voter in voters]).most_common()[0][0]

def printStateOfVoterVotes(voters):
	for voter in voters:
	 print ('User {0}: {1} '.format(voter.id, voter.votes))

if (len(sys.argv) != 3):
	print("ERROR: Must provide Options and Input. python least_hated.py <path-to-options> <path-to-input>")
options = CreateOptions(sys.argv[1])
voters = CreateVoters(sys.argv[2])

winner = determineLeastHatedFirstFridayOption(options, voters)

print ('And the winner is...{0}'.format( winner.name))