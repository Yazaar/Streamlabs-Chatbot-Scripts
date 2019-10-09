#---------------------------------------
# Import Libraries
#---------------------------------------
import os, codecs, json, random, datetime

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts
"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Russian Roulette"
Website = "https://www.twitch.tv/yazaar"
Description = "1v1 Russian Roulette"
Creator = "Yazaar"
Version = "0.1.0"
#---------------------------------------
# Variables
#---------------------------------------

FreshInstallFile = os.path.join(os.path.dirname(__file__), "FreshInstall.txt")
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
InformationFile = os.path.join(os.path.dirname(__file__), "Information.txt")
MissFile = os.path.join(os.path.dirname(__file__), "miss.txt")
HitFile = os.path.join(os.path.dirname(__file__), "hit.txt")


# 0 = Waiting for a challenge
# 1 = Waiting for a response
# 2 = Betting
# 3 = Game in progress
GameState = 0

target = ''
challenger = ''
rouletteAmount = 0
CurrentUser = ''
BetAmount = 0

betting = {
	'pot': 0,
	'challenger': [],
	'target': []
}

rounds = [0, 0, 0, 0, 0, 1]

timer = datetime.datetime.now()

#---------------------------------------
# Read files + winrate list
#---------------------------------------

def resetSettings():
	global Settings
	Settings = {
		"Permission": "Everyone",
		"PermissionInfo": "",
		"Command": "!rr",
		"BetDuration": 90,
		"MinRoulette": 1,
		"MaxRoulette": 0,
		"MinBet": 1,
		"MaxBet": 0,
		"DurationBetweenRounds": 1,
		"PendingDuration": 30,
		"PersonalCooldown": 10,
		"ChannelCooldown": 0,
		"NoPermissionMessage": "$(Display), you have no permission to use the command!",
		"ShowPermissionMessage": True,
		"PersonalCooldownMessage": "$(Display), you have $(CooldownLeft) seconds left on your cooldown!",
		"ShowPersonalCooldownMessage": True,
		"ChannelCooldownMessage": "$(Display), there is a channel cooldown on $(ChannelCooldownLeft) seconds!",
		"ShowChannelCooldownMessage": True,
		"BetYourselfMessage": "$(Display), you are unable to bet on your own game.",
		"ShowBetYourselfMessage": True,
		"AlreadyBettedMessage": "$(Display) has betted already.",
		"ShowAlreadyBettedMessage": True,
		"BetOutOfRangeDownMessage": "$(Display), you have to bet at least $(MinBet) $(Currency)",
		"ShowBetOutOfRangeDownMessage": True,
		"BetOutOfRangeUpMessage": "$(Display), you are unable to bet more than $(MaxBet) $(Currency)",
		"ShowBetOutOfRangeUpMessage": True,
		"NotEnoughPointsMessage": "$(Display) does not have enough $(Currency) to bet $(BetAmount)",
		"ShowNotEnoughPointsMessage": True,
		"BetCompleteMessage": "$(Display) betted on $(Challenger)",
		"ShowBetCompleteMessage": True,
		"InvalidBetMessage": "Invalid bet, try: $(Command) username/challenger/target [AMOUNT]",
		"ShowInvalidBetMessage": True,
		"GameInProgressMessage": "A game is in progress already. Please wait.",
		"ShowGameInProgressMessage": True,
		"NotChallengedMessage": "You are not challenged, $(Display).",
		"ShowNotChallengedMessage": True,
		"TooLowRouletteMessage": "$(Display), you have to bet at least $(MinRoulette) $(Currency)",
		"ShowTooLowRouletteMessage": True,
		"TooHighRouletteMessage": "$(Display), you are unable to bet more than $(MaxRoulette) $(Currency)",
		"ShowTooHighRouletteMessage": True,
		"RouletteAcceptedMessage": "$(Display) accepted the challenge against $(Challenger) and betting has begun (active for $(BetDuration) seconds).",
		"ShowRouletteAcceptedMessage": True,
		"ChallengeYourselfMessage": "You are unable to challenge yourself, but nice try!",
		"ShowChallengeYourselfMessage": True,
		"InvalidRouletteNumberMessage": "Argument 3 has to be a number: $(Command) [USER] [BET AMOUNT]",
		"ShowInvalidRouletteNumberMessage": True,
		"RouletteTooLowMessage": "$(Display), you have to bet at least $(MinRoulette) $(Currency)",
		"ShowRouletteTooLowMessage": True,
		"RouletteTooHighMessage": "$(Display), you are unable to bet more than $(MaxRoulette) $(Currency)",
		"ShowRouletteTooHighMessage": True,
		"ChallengerNotEnoughPointsMessage": "$(Challenger) needs at least $(RouletteAmount) $(Currency) to continue...",
		"ShowChallengerNotEnoughPointsMessage": True,
		"TargetNotEnoughPointsMessage": "$(Target) needs at least $(RouletteAmount) $(Currency) to continue...",
		"ShowTargetNotEnoughPointsMessage": True,
		"ChallengeCompleteMessage": "$(Display) challenged $(Target) in Russian Roulette, with a bet of $(RouletteAmount) $(Currency)!",
		"ShowChallengeCompleteMessage": True,
		"RejectMessage": "$(Display) rejected your challenge $(Challenger).",
		"ShowRejectMessage": True,
		"HelpMessage": "Start a 1v1 Russian Roulette through: $(Command) [USER] [BET AMOUNT]",
		"ShowHelpMessage": True,
		"TargetNoResponseMessage": "$(Target) never responded and the game has been canceled.",
		"ShowTargetNoResponseMessage": True,
		"BeginningMessage": "The revolver has been prepared and the game has begun.",
		"ShowBeginningMessage": True
	}

with open(FreshInstallFile, "r") as f:
	m_FreshInstall = f.read()

with open(HitFile, "r") as f:
	HitQuotes = f.read().split('\n')

with open(MissFile, "r") as f:
	MissQuotes = f.read().split('\n')

if os.path.isfile(SettingsFile):
	with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
		Settings = json.load(f, encoding='utf-8-sig')
else:
	resetSettings()

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	if m_FreshInstall == "true":
		with open(FreshInstallFile, "w+") as f:
			f.write("false")
		with open(InformationFile, "r") as f:
			NameToFile = f.read()
		NameToFile = NameToFile.replace("[NAME_OF_USER]", Parent.GetChannelName())
		with open(InformationFile, "w+") as f:
			f.write(NameToFile)
		os.startfile(InformationFile)

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global GameState, challenger, target, rouletteAmount, rounds, timer, betting, BetAmount
	if data.GetParam(0).lower() != Settings['Command'].lower():
		return

	if Parent.IsOnUserCooldown(ScriptName,Settings['Command'], data.User):
		if Settings['ShowPersonalCooldownMessage'] == True:
			Parent.SendStreamMessage(ConvertMessage(data, Settings['PersonalCooldownMessage']))
		return
	
	if Parent.IsOnCooldown(ScriptName, Settings['Command']):
		if Settings['ShowChannelCooldownMessage'] == True:
			Parent.SendStreamMessage(ConvertMessage(data, Settings['ChannelCooldownMessage']))
		return

	if NoPermission(data, Settings['Permission'], Settings['PermissionInfo']):
		if Settings['ShowPermissionMessage'] == True:
			Parent.SendStreamMessage(ConvertMessage(data, Settings['NoPermissionMessage']))
		return
	
	Parent.AddCooldown(ScriptName, Settings['Command'], Settings['ChannelCooldown'])
	Parent.AddUserCooldown(ScriptName, Settings['Command'], data.User, Settings['PersonalCooldown'])

	if data.GetParamCount() > 2 and GameState != 2:
		if GameState != 0:
			if Settings['ShowGameInProgressMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['GameInProgressMessage']))
			return
		challenger = data.User
		target = data.GetParam(1).lower()

		if challenger == target:
			if Settings['ShowChallengeYourselfMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['ChallengeYourselfMessage']))
			return

		try:
			rouletteAmount = int(data.GetParam(2))
		except Exception:
			if Settings['ShowInvalidRouletteNumberMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['InvalidRouletteNumberMessage']))
			return
		
		if rouletteAmount < Settings['MinRoulette']:
			if Settings['ShowRouletteTooLowMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['RouletteTooLowMessage']))
			return
		if rouletteAmount > Settings['MaxRoulette']:
			if Settings['MaxRoulette'] != 0:
				if Settings['ShowRouletteTooHighMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['RouletteTooHighMessage']))
				return
		
		if Parent.GetPoints(challenger) < rouletteAmount:
			if Settings['ShowChallengerNotEnoughPointsMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['ChallengerNotEnoughPointsMessage']))
			return
		if Parent.GetPoints(target) < rouletteAmount:
			if Settings['ShowTargetNotEnoughPointsMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['TargetNotEnoughPointsMessage']))
			return
		
		if Settings['ShowChallengeCompleteMessage'] == True:
			Parent.SendStreamMessage(ConvertMessage(data, Settings['ChallengeCompleteMessage']))

		timer = datetime.datetime.now()
		
		GameState = 1
		return

	if GameState == 2 and data.GetParamCount() > 2:
		if (datetime.datetime.now() - timer).total_seconds() < Settings['BetDuration']:
			if data.User == challenger or data.User == target:
				if Settings['ShowBetYourselfMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['BetYourselfMessage']))
				return
			if alreadyBetted(data.User):
				if Settings['ShowAlreadyBettedMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['AlreadyBettedMessage']))
				return
			BetTarget = data.GetParam(1).lower()
			if BetTarget[0] == '@':
				BetTarget = BetTarget[1:]
			try:
				BetAmount = int(data.GetParam(2))
			except Exception:
				BetAmount = -1
				BetTarget = ''
			
			if BetAmount < Settings['MinBet']:
				if Settings['ShowBetOutOfRangeDownMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['BetOutOfRangeDownMessage']))
				return
			if BetAmount > Settings['MaxBet']:
				if Settings['MaxBet'] != 0:
					if Settings['ShowBetOutOfRangeUpMessage'] == True:
						Parent.SendStreamMessage(ConvertMessage(data, Settings['BetOutOfRangeUpMessage']))
					return
			
			if Parent.GetPoints(challenger) < BetAmount:
				if Settings['ShowNotEnoughPointsMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['NotEnoughPointsMessage']))
				return
			
			if BetTarget == challenger or BetTarget == 'challenger':
				betting['challenger'].append([data.User, BetAmount])
				betting['pot'] += BetAmount
				if Settings['ShowBetCompleteMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['BetCompleteMessage']))
				return

			elif BetTarget == target or BetTarget == 'target':
				betting['target'].append([data.User, BetAmount])
				betting['pot'] += BetAmount
				if Settings['ShowBetCompleteMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['BetCompleteMessage']))
				return
			else:
				if Settings['ShowInvalidBetMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['InvalidBetMessage']))
				return

	if data.GetParamCount() > 1:
		if data.GetParam(1).lower() == 'accept':
			if GameState != 1 or data.User != target:
				if Settings['ShowNotChallengedMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['NotChallengedMessage']))
				return
			if rouletteAmount < Settings['MinRoulette']:
				if Settings['ShowTooLowRouletteMessage'] == True:	
					Parent.SendStreamMessage(ConvertMessage(data, Settings['TooLowRouletteMessage']))
				return
			if rouletteAmount > Settings['MaxRoulette']:
				if Settings['MaxRoulette'] != 0:
					if Settings['ShowTooHighRouletteMessage'] == True:
						Parent.SendStreamMessage(ConvertMessage(data, Settings['TooHighRouletteMessage']))
					return
			Parent.RemovePoints(challenger, Parent.GetDisplayName(challenger), rouletteAmount)
			Parent.RemovePoints(target, Parent.GetDisplayName(target), rouletteAmount)
			GameState = 2
			rounds = [0, 0, 0, 0, 0, 1]
			random.shuffle(rounds)
			timer = datetime.datetime.now()
			betting = {'pot': 0, 'challenger': [], 'target': []}
			if Settings['ShowRouletteAcceptedMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['RouletteAcceptedMessage']))
			return
		elif data.GetParam(1).lower() == 'reject':
			if GameState != 1 and (data.User != target or data.User != challenger):
				if Settings['ShowNotChallengedMessage'] == True:
					Parent.SendStreamMessage(ConvertMessage(data, Settings['NotChallengedMessage']))
				return
			GameState = 0
			if Settings['ShowRejectMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage(data, Settings['RejectMessage']))
			return
	
	if Settings['ShowHelpMessage'] == True:
		Parent.SendStreamMessage(ConvertMessage(data, Settings['HelpMessage']))

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
	global timer, GameState, CurrentUser
	if GameState == 1:
		if (datetime.datetime.now() - timer).total_seconds() > Settings['PendingDuration']:
			GameState = 0
			if Settings['ShowTargetNoResponseMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage('', Settings['TargetNoResponseMessage']))
		return
	elif GameState == 2:
		if (datetime.datetime.now() - timer).total_seconds() > Settings['BetDuration']:
			if Settings['ShowBeginningMessage'] == True:
				Parent.SendStreamMessage(ConvertMessage('', Settings['BeginningMessage']))
			GameState = 3
	elif GameState == 3:
		if (datetime.datetime.now() - timer).total_seconds() > Settings['DurationBetweenRounds']:
			if len(rounds) % 2 == 0:
				CurrentUser = challenger
			else:
				CurrentUser = target

			if rounds.pop(0) == 1:
				Parent.SendStreamMessage(ConvertMessage('', random.choice(HitQuotes)))
				Parent.AddPoints(CurrentUser, Parent.GetDisplayName(CurrentUser) , rouletteAmount * 2)
				handleBettingPayout()
				GameState = 0
			else:
				Parent.SendStreamMessage(ConvertMessage('', random.choice(MissQuotes)))
				timer = datetime.datetime.now()
			return


#---------------------------------------
# Other Script Functions
#---------------------------------------

def alreadyBetted(user):
	for bet in betting['challenger']:
		if bet[0] == user:
			return True
	for bet in betting['target']:
		if bet[0] == user:
			return True
	return False

def handleBettingPayout():
	if CurrentUser == challenger:
		key = 'challenger'
	else:
		key = 'target'
	WinSidePot = 0.0
	for i in betting[key]:
		WinSidePot += i[1]
	for i in betting[key]:
		Parent.AddPoints(i[0], Parent.GetDisplayName(i[0]), int(betting['pot'] * (i[1] / WinSidePot)))

def calculateNextUser():
	if len(rounds) % 2 == 0:
		return challenger
	else:
		return target

def NoPermission(data, permission, permissionInfo):
	if permission == "User_Specific":
		if data.User in permissionInfo.lower().split(" "):
			return False
		else:
			return True
	if not Parent.HasPermission(data.User, permission, permissionInfo):
		return True
	else:
		return False

def ConvertMessage(data, raw_message):
	Message = raw_message
	if data != '':
		Message = Message.replace("$(Username)", str(data.User))
		Message = Message.replace("$(Display)", str(Parent.GetDisplayName(data.User)))
		Message = Message.replace("$(CooldownLeft)", str(Parent.GetUserCooldownDuration(ScriptName, Settings["Command"], data.User)))
		Message = Message.replace("$(CurrencyAmount)", str(Parent.GetPoints(data.User)))
	Message = Message.replace("$(WinAmount)", str(rouletteAmount*2))
	Message = Message.replace("$(RouletteAmount)", str(rouletteAmount))
	Message = Message.replace("$(AcceptDuration)", str(Settings['PendingDuration']))
	Message = Message.replace("$(BetDuration)", str(Settings['BetDuration']))
	Message = Message.replace("$(Roll)", str((6 - len(rounds))))
	Message = Message.replace("$(ChannelCooldownLeft)", str(Parent.GetCooldownDuration(ScriptName,Settings["Command"])))
	Message = Message.replace("$(Target)", str(Parent.GetDisplayName(target)))
	Message = Message.replace("$(Challenger)", str(Parent.GetDisplayName(challenger)))
	Message = Message.replace("$(CurrentUser)", Parent.GetDisplayName(CurrentUser))
	Message = Message.replace("$(NextUser)", Parent.GetDisplayName(calculateNextUser()))
	Message = Message.replace("$(TotalPersonalCooldown)", str(Settings["PersonalCooldown"]))
	Message = Message.replace("$(TotalChannelCooldown)", str(Settings["ChannelCooldown"]))
	Message = Message.replace("$(MinBet)", str(Settings["MinBet"]))
	Message = Message.replace("$(MaxBet)", str(Settings["MaxBet"]))
	Message = Message.replace("$(BetAmount)", str(BetAmount))
	Message = Message.replace("$(MinRoulette)", str(Settings["MinRoulette"]))
	Message = Message.replace("$(MaxRoulette)", str(Settings["MaxRoulette"]))
	Message = Message.replace("$(Currency)", str(Parent.GetCurrencyName()))
	Message = Message.replace("$(Command)", str(Settings["Command"]))
	Message = Message.replace("$(Permission)", str(Settings["Permission"]))
	Message = Message.replace("$(PermissionInfo)", str(Settings["PermissionInfo"]))
	return Message

def ReloadRussianRouletteScript():
	global Settings, HitQuotes, MissQuotes
	with open(HitFile, "r") as f:
		HitQuotes = f.read().split('\n')

	with open(MissFile, "r") as f:
		MissQuotes = f.read().split('\n')

	if os.path.isfile(SettingsFile):
		with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
			Settings = json.load(f, encoding='utf-8-sig')
	else:
		resetSettings()

def OpenMissRussianRouletteMessagesScript():
	os.startfile(MissFile)

def OpenHitRussianRouletteMessagesScript():
	os.startfile(HitFile)