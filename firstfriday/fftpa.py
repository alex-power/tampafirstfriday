import Voter
import Option
import Factory
import collections


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

options = Factory.CreateOptions("C:/Users/apower/Documents/firstfriday/ffOptionsInput.txt")
voters = Factory.CreateVoters("C:/Users/apower/Documents/firstfriday/input.txt")

winner = determineLeastHatedFirstFridayOption(options, voters)

print ('And the winner is...{0}'.format( winner.name))