import Voter
import Option

def CreateVoters(path):
	voteFile = open(path, 'r')
	voters = []
	currentUserId = 0

	line = voteFile.readline()
	while line:
		splitVotes = line.split(',')

		splitVotes[len(splitVotes) - 1] = splitVotes[len(splitVotes) - 1].strip('\n')

		votes = [int(vote) for vote in splitVotes]
		currentUserId += 1
		voters.append(Voter.Voter(currentUserId, votes))
		
		line = voteFile.readline()

	voteFile.close()
	print ([voter.votes for voter in voters])
	return voters


def CreateOptions(path):
	optionFile = open(path, 'r')
	options = []
	currentOptionId = 0
	
	line = optionFile.readline()
	while line:
		url = line[line.index('('):-1]
		line = line[0:line.index('(')]
		print(line)
		currentOptionId += 1
		options.append(Option.Option(currentOptionId, line, url))
		

		line = optionFile.readline()

	optionFile.close()

	return	options
