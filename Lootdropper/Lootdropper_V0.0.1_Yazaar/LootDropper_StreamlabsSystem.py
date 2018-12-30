#---------------------------------------
# Import Libraries
#---------------------------------------
import os, datetime, random, codecs, json

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts
"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "LootDropper"
Website = "https://www.twitch.tv/yazaar"
Description = "Reward active users with chatbot currency!"
Creator = "Yazaar"
Version = "0.0.1"
#---------------------------------------
# Variables + Files
#---------------------------------------

Winners = None

SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
InformationFile = os.path.join(os.path.dirname(__file__), "Information.txt")
FreshInstallFile = os.path.join(os.path.dirname(__file__), "FreshInstall.txt")

#---------------------------------------
# READ FILES
#---------------------------------------

with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
  Settings = json.load(f, encoding='utf-8-sig')

with open(FreshInstallFile, "r") as f:
	FreshInstallState = f.read()

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	global FreshInstallState
	if FreshInstallState == "True":

		with open(InformationFile, 'r') as f:
			temp = f.read()

		temp = temp.replace('[NAME_OF_USER]', str(Parent.GetChannelName()))

		with open(InformationFile, 'w') as f:
			f.write(temp)

		temp = None
		os.startfile(InformationFile)

		with open(FreshInstallFile, 'w') as f:
			f.write("False")

		FreshInstallState = "False"
		return
	
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global Dropping, Time1, Entries
	if data.GetParam(0).lower() == Settings["Command"].lower() and data.GetParamCount() == 1 and data.IsChatMessage():

		if NoPermission(data):
			return
		
		if Parent.IsOnCooldown(ScriptName,Settings["Command"]):
			return

		
		if Parent.IsOnUserCooldown(ScriptName, Settings["Command"], data.User):
			Parent.SendStreamMessage(ConvertMessage(data, Settings["CooldownMessage"]))
			return
		
		Parent.AddCooldown(ScriptName,Settings["Command"],Settings["ChannelCooldown"])
			

		if Dropping == True:
			if str(Parent.GetDisplayName(data.User)) in Entries:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["AlreadyInDropMessage"]))
				return
			Entries.append(str(Parent.GetDisplayName(data.User)))
			Parent.SendStreamMessage(ConvertMessage(data, Settings["JoinedDropMessage"]))
			Parent.AddPoints(data.User, Settings["JoinReward"])
			Parent.AddUserCooldown(ScriptName, Settings["Command"], data.User, Settings["Cooldown"])
			return
		else:
			Parent.SendStreamMessage(ConvertMessage(data, Settings["NoDropMessage"]))
			Parent.AddUserCooldown(ScriptName, Settings["Command"], data.User, Settings["Cooldown"])
			return

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
	global Dropping, Time1, Entries, Winners
	if datetime.datetime.today() > Time1 and Dropping == False:
		Time1 = datetime.datetime.today() + datetime.timedelta(seconds=Settings["DropTime"])
		Dropping = True
		Parent.SendStreamMessage(ConvertMessage(None, Settings["DropStartingMessage"]))
		return
	if datetime.datetime.today() > Time1 and Dropping == True:
		Time1 = datetime.datetime.today() + datetime.timedelta(minutes=Parent.GetRandom(Settings["SleepMin"], Settings["SleepMax"]+1))
		Dropping = False
		Winners = random.sample(Entries, k=int(len(Entries)*Settings["LotteryWinner"]))
		
		if len(Winners) == 0:
			Parent.SendStreamMessage(ConvertMessage(None, Settings["DropClosingMessage1"]))
		else:
			Parent.SendStreamMessage(ConvertMessage(None, Settings["DropClosingMessage2"]))
			
			for i in Winners:
				Parent.AddPoints(i.lower(), Settings["LotteryPrice"])
			
		Entries = []
		return
	
		
		
def ScriptToggled(state):
	global Dropping, Time1, Entries
	if state == True:
		Time1 = datetime.datetime.today() + datetime.timedelta(minutes=Parent.GetRandom(Settings["SleepMin"], Settings["SleepMax"]+1))
		Dropping = False
		Entries = []
		return

	if state == False:
		return

#---------------------------------------
# OTHER FUNCTIONS FOR THE SCRIPT
#---------------------------------------

def OpenLootDropperInfo():
	os.startfile(InformationFile)
	return

def ReloadLootDropperScript():
	with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
		Settings = json.load(f, encoding='utf-8-sig')
	return

def NoPermission(data):
  if Settings["Permission"] == "User_Specific":
    if data.User in Settings["PermissionInfo"].lower().split(" "):
      return False
    else:
      Parent.SendStreamMessage(ConvertMessage(data, Settings["NoPermissionMessage"]))
      Parent.AddUserCooldown(ScriptName,Settings["Command"],data.User,Settings["Cooldown"])
      return True

  if not Parent.HasPermission(data.User, Settings["Permission"], Settings["PermissionInfo"]):
    Parent.SendStreamMessage(ConvertMessage(data, Settings["NoPermissionMessage"]))
    Parent.AddUserCooldown(ScriptName,Settings["Command"],data.User,Settings["Cooldown"])
    return True
  else:
    return False

def ConvertMessage(data, raw_message):
	Message = raw_message
	try:
		Message = Message.replace("$(Username)", str(data.User))
	except Exception:
		pass
	try:
		Message = Message.replace("$(Display)", str(Parent.GetDisplayName(data.User)))
	except Exception:
		pass
	try:
		Message = Message.replace("$(CooldownLeft)", str(Parent.GetUserCooldownDuration(ScriptName, Settings["Command"], data.User)))
	except Exception:
		pass
	Message = Message.replace("$(Cooldown)", str(Settings["Cooldown"]))
	Message = Message.replace("$(Currency)", str(Parent.GetCurrencyName()))
	Message = Message.replace("$(LotteryWinners)", str(Winners).replace("[", "").replace("]", "").replace("'", ""))
	Message = Message.replace("$(LotteryReward)", str(Settings["LotteryPrice"]))
	Message = Message.replace("$(JoinReward)", str(Settings["JoinReward"]))
	Message = Message.replace("$(DropTime)", str(Settings["DropTime"]))
	Message = Message.replace("$(Command)", str(Settings["Command"]))
	Message = Message.replace("$(Permission)", str(Settings["Permission"]))
	Message = Message.replace("$(PermissionInfo)", str(Settings["PermissionInfo"]))
	return Message