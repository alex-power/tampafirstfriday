from flask import Flask, request, make_response
import datetime
import least_hated
import validator
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
	
app = Flask(__name__)

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

OPTIONS_SPREADHSEET = '1iw1iqAt2ajjCCalnCTqtzoEHAUFcUunyV-veup4OZus'
OPTIONS_SPREADHSEET_RANGE = 'Options!B2:B222'

inputStrings = []

def get_options():	
	try:
		store = file.Storage('token.json')
		creds = store.get()
	except:
		print("No token.json")

	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, trange=RANGE_NAME).execute()
	values = result.get('values', [])
	print(values)
	return values

@app.route('/')
def hello():
	return options()

@app.route('/options')
def options():
	output = "Vote like this: /vote/name?votes=1,2,3,4,5\n"
	index = 1
	for line in open('options.txt'):
		output += "{}. {}\r\n".format(index, line)
		index += 1

	return plain_output(output )

@app.route('/validate')
def validate_endpoint():
	inputString = get_votes()

	validate(inputString)
	return plain_output(output)

def validate(input_str):

	options = open('options.txt', 'r')
	num_votes = len(options.readlines())
	options.close()
	return validator.validate(num_votes, input_str)

@app.route('/write')
def write():
	global inputStrings
	inputFileName = 'input_{}.txt'.format(datetime.datetime.now().strftime("%d.%m.%y_%H.%M.%S"))
	inputFile = open(inputFileName, 'w+')
	for inputString in inputStrings:
		inputFile.write(inputString + '\n')
	inputFile.close()
	output = least_hated.run("options.txt", inputFileName)
	inputStrings = []	
	return plain_output(output)


@app.route('/vote/<name>')
def vote(name):
	global inputStrings
	inputString = get_votes()

	validation = validate(inputString)
	if "FAILURE" in validation:
		return plain_output(validation)

	inputStrings = [x for x in inputStrings if name not in x]
	inputStrings.append(name + ',' + inputString)
	return plain_output("You voted!\nName: " + name + "\nVotes: " + inputString);

def get_votes():
	inputString = ""
	try:
		inputString = request.args.get('votes')
	except:
		abort(400)
	return inputString

def plain_output(out_string):
	resp = make_response(out_string)
	resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
	return resp

@app.errorhandler(400)
def handle():
	return "Please include your votes like the following url: /vote/name?votes=1,2,3,4,5"