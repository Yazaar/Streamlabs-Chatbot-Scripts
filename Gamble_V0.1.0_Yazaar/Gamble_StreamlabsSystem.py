#---------------------------------------
# Import Libraries
#---------------------------------------
import os, codecs, json, random

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts
"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Gamble"
Website = "https://www.twitch.tv/yazaar"
Description = "Gamble with special functions"
Creator = "Yazaar"
Version = "0.1.0"
#---------------------------------------
# Variables
#---------------------------------------

FreshInstallFile = os.path.join(os.path.dirname(__file__), "FreshInstall.txt")
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
InformationFile = os.path.join(os.path.dirname(__file__), "Information.txt")

#---------------------------------------
# Read files + winrate list
#---------------------------------------

with open(FreshInstallFile, "r") as f:
	m_FreshInstall = f.read()
	
with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
	Settings = json.load(f, encoding='utf-8-sig')

OutcomePicker = []

for i in range(Settings["WinChanse"]):
	OutcomePicker.append("win")

for i in range(Settings["2xWinChanse"]):
	OutcomePicker.append("2xwin")

for i in range(Settings["LossRisk"]):
	OutcomePicker.append("loss")

random.shuffle(OutcomePicker)

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
		NameToFile = None
		os.startfile(str(InformationFile))

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	if data.GetParam(0).lower() == Settings["Command"].lower() and data.GetParamCount() > 1:

		if Parent.IsOnCooldown(ScriptName,Settings["Command"]):
			if Settings["ShowChannelCooldownMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["ChannelCooldownMessage"]))
			return

		if Parent.IsOnUserCooldown(ScriptName,Settings["Command"],data.User):
			if Settings["ShowPersonalCooldownMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["PersonalCooldownMessage"]))
			return

		if NoPermission(data):
			if Settings["ShowNoPermissionMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["NoPermissionMessage"]))
			return
		
		if data.GetParam(1).lower() == "all":
			Param2 = int(Parent.GetPoints(data.User))
		elif len(data.GetParam(1).lower()) != 0 and data.GetParam(1).lower()[-1] == "%":
			try:
				Param1 = int((float(data.GetParam(1).lower()[:-1]) / 100) * Parent.GetPoints(data.User))
			except Exception:
				if Settings["ShowGambleError"]:
					Parent.SendStreamMessage("Gamble error, invalid percentage: " + data.GetParam(1))
				return
		elif len(data.GetParam(1).lower()) != 0:
			try:
				Param1 = int(data.GetParam(1).lower())
			except Exception:
				if Settings["ShowGambleError"]:
					Parent.SendStreamMessage("Gamble error, invalid number: " + data.GetParam(1))
				return
		else:
			Param1 = None
		
		if data.GetParam(2).lower() == "all":
			Param2 = int(Parent.GetPoints(data.User))
		elif len(data.GetParam(2).lower()) != 0 and data.GetParam(2).lower()[-1] == "%":
			try:
				Param2 = int((float(data.GetParam(2).lower()[:-1]) / 100) * Parent.GetPoints(data.User))
			except Exception:
				if Settings["ShowGambleError"]:
					Parent.SendStreamMessage("Gamble error, invalid percentage: " + data.GetParam(2))
				return
		elif len(data.GetParam(2).lower()) != 0:
			try:
				Param2 = int(data.GetParam(2).lower())
			except Exception:
				if Settings["ShowGambleError"]:
					Parent.SendStreamMessage("Gamble error, invalid number: " + data.GetParam(2))
				return
		else:
			Param2 = None
		
		if isinstance(Param1, int) and isinstance(Param2, int):
			if Param1 > Param2:
				MyGamble = Parent.GetRandom(Param2, Param1+1)
			else:
				MyGamble = Parent.GetRandom(Param1, Param2+1)
		elif isinstance(Param1, int):
			MyGamble = Param1
		
		if MyGamble > Parent.GetPoints(data.User):
			if Settings["ShowNotEnoughMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["NotEnoughMessage"].replace("$(Amount)", str(MyGamble))))
			return

		if MyGamble < Settings["MinGamble"]:
			if Settings["ShowMinGambleMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["MinGambleMessage"]))
			return

		result = random.choice(OutcomePicker)
		if result == "win" and isinstance(MyGamble, int):
			Parent.AddPoints(data.User,data.UserName,MyGamble)
			if Settings["ShowWinMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["WinMessage"].replace("$(Amount)", str(MyGamble))))
		elif result == "2xwin" and isinstance(MyGamble, int):
			Parent.AddPoints(data.User,data.UserName,MyGamble*2)
			if Settings["Show2xWinMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["2xWinMessage"].replace("$(Amount)", str(MyGamble*2))))
		elif result == "loss" and isinstance(MyGamble, int):
			Parent.RemovePoints(data.User,data.UserName,MyGamble)
			if Settings["ShowLossMessage"]:
				Parent.SendStreamMessage(ConvertMessage(data, Settings["LossMessage"].replace("$(Amount)", str(MyGamble))))
	return
#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return


#---------------------------------------
# Other Script Functions
#---------------------------------------

def NoPermission(data):
	Parent.AddUserCooldown(ScriptName,Settings["Command"],data.User,Settings["PersonalCooldown"])
	Parent.AddCooldown(ScriptName,Settings["Command"],Settings["ChannelCooldown"])
	if Settings["Permission"] == "User_Specific":
		if data.User in Settings["PermissionInfo"].lower().split(" "):
			return False
		else:
			return True
		
	if not Parent.HasPermission(data.User, Settings["Permission"], Settings["PermissionInfo"]):
		return True
	else:
		return False

def ConvertMessage(data, raw_message):
	Message = raw_message
	try:
		Message = Message.replace("$(Username)", str(data.User))
		Message = Message.replace("$(Display)", str(Parent.GetDisplayName(data.User)))
		Message = Message.replace("$(CooldownLeft)", str(Parent.GetUserCooldownDuration(ScriptName, Settings["Command"], data.User)))
		Message = Message.replace("$(ChannelCooldownLeft)", str(Parent.GetCooldownDuration(ScriptName,Settings["Command"])))
		Message = Message.replace("$(CurrencyAmount)", str(Parent.GetPoints(data.User)))
	except Exception:
		pass
	Message = Message.replace("$(TotalPersonalCooldown)", str(Settings["PersonalCooldown"]))
	Message = Message.replace("$(TotalChannelCooldown)", str(Settings["ChannelCooldown"]))
	Message = Message.replace("$(MinGamble)", str(Settings["MinGamble"]))
	Message = Message.replace("$(Currency)", str(Parent.GetCurrencyName()))
	Message = Message.replace("$(Command)", str(Settings["Command"]))
	Message = Message.replace("$(Permission)", str(Settings["Permission"]))
	Message = Message.replace("$(PermissionInfo)", str(Settings["PermissionInfo"]))
	Message = Message.replace("$(Roll)", str(Parent.GetRandom(1,101)))
	return Message

def ReloadGambleScript():
	global Settings
	with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
		Settings = json.load(f, encoding='utf-8-sig')
