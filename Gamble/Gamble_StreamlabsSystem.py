#---------------------------------------
# Import Libraries
#---------------------------------------
import os
import pickle

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts/tree/Gamble

"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Gamble"
Website = "https://www.twitch.tv/yazaar"
Description = "Gamble with special functions"
Creator = "Yazaar"
Version = "0.0.1"
#---------------------------------------
# FILES
#---------------------------------------
ChannelCooldownFile = os.path.join(os.path.dirname(__file__), "Settings\ChannelCooldown.txt")
CommandFile = os.path.join(os.path.dirname(__file__), "Settings\Command.txt")
HugeWinHighFile = os.path.join(os.path.dirname(__file__), "Settings\HugeWinHigh.txt")
HugeWinLowFile = os.path.join(os.path.dirname(__file__), "Settings\HugeWinLow.txt")
IfChannelCooldownMessageFile = os.path.join(os.path.dirname(__file__), "Settings\IfChannelCooldownMessage.txt")
IfPersonalCooldownMessageFile = os.path.join(os.path.dirname(__file__), "Settings\IfPersonalCooldownMessage.txt")
LossHighFile = os.path.join(os.path.dirname(__file__), "Settings\LossHigh.txt")
LossLowFile = os.path.join(os.path.dirname(__file__), "Settings\LossLow.txt")
MinimumGambleFile = os.path.join(os.path.dirname(__file__), "Settings\MinimumGamble.txt")
OfflineMessageFile = os.path.join(os.path.dirname(__file__), "Settings\OfflineMessage.txt")
OnlineMessageFile = os.path.join(os.path.dirname(__file__), "Settings\OnlineMessage.txt")
PersonalCooldownFile = os.path.join(os.path.dirname(__file__), "Settings\PersonalCooldown.txt")
WinHighFile = os.path.join(os.path.dirname(__file__), "Settings\WinHigh.txt")
WinLowFile = os.path.join(os.path.dirname(__file__), "Settings\WinLow.txt")
PermissionFile = os.path.join(os.path.dirname(__file__), "Settings\Permission.txt")
ShowPermissionFile = os.path.join(os.path.dirname(__file__), "Settings\ShowPermission.txt")
AdminsFile = os.path.join(os.path.dirname(__file__), "Settings\Admins.pickle")
FreshInstallFile = os.path.join(os.path.dirname(__file__), "Settings\FreshInstall.txt")
InformationFile = os.path.join(os.path.dirname(__file__), "Information.txt")
#---------------------------------------
# Read all files for settings
#---------------------------------------
with open(ChannelCooldownFile, "r") as f:
	m_ChannelCooldownSeconds = f.read()
	m_ChannelCooldownSeconds = int(m_ChannelCooldownSeconds)

with open(CommandFile, "r") as f:
	m_Command = f.read()

with open(HugeWinHighFile, "r") as f:
	m_HugeWinHigh = f.read()
	m_HugeWinHigh = int(m_HugeWinHigh)

with open(HugeWinLowFile, "r") as f:
	m_HugeWinLow = f.read()
	m_HugeWinLow = int(m_HugeWinLow)

with open(IfChannelCooldownMessageFile, "r") as f:
	IfChannelCooldownMessage = f.read()

with open(IfPersonalCooldownMessageFile, "r") as f:
	IfPersonalCooldownMessage = f.read()

with open(LossHighFile, "r") as f:
	m_LossHigh = f.read()
	m_LossHigh = int(m_LossHigh)

with open(LossLowFile, "r") as f:
	m_LossLow = f.read()
	m_LossLow = int(m_LossLow)

with open(MinimumGambleFile, "r") as f:
	m_MinimumGamble = f.read()
	m_MinimumGamble = int(m_MinimumGamble)

with open(OfflineMessageFile, "r") as f:
	m_CommandDown = f.read()

with open(OnlineMessageFile, "r") as f:
	m_CommandUp = f.read()

with open(PersonalCooldownFile, "r") as f:
	m_PersonalCooldownSeconds = f.read()
	m_PersonalCooldownSeconds = int(m_PersonalCooldownSeconds)

with open(WinHighFile, "r") as f:
	m_WinHigh = f.read()
	m_WinHigh = int(m_WinHigh)

with open(WinLowFile, "r") as f:
	m_WinLow = f.read()
	m_WinLow = int(m_WinLow)

with open(PermissionFile, "r") as f:
	m_CommandPermission = f.read()

with open(ShowPermissionFile, "r") as f:
	m_ShowPermission = f.read()

with open(AdminsFile, "rb") as f:
    m_Admins = pickle.load(f)

with open(FreshInstallFile, "r") as f:
	m_FreshInstall = f.read()
	

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	if m_FreshInstall == "true":
		with open(FreshInstallFile, "w+") as f:
			f.write("false")
		with open(InformationFile, "r") as f:
			ChangePath = f.read()
		ChangePath = ChangePath.replace("THIS_DOCUMENTS_FILE_PATH", str(os.path.realpath(__file__)))
		ChangePath = ChangePath.replace("Gamble_StreamlabsSystem.py", "Information.txt")
		with open(InformationFile, "w+") as f:
			f.write(ChangePath)
		ChangePath = None
		os.startfile(str(InformationFile))
	if m_CommandUp == "true":
		Parent.SendTwitchMessage("/me Gamble command online")
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global m_ChannelCooldownSeconds, m_Command, m_HugeWinHigh, m_HugeWinLow, IfChannelCooldownMessage, IfPersonalCooldownMessage, m_LossHigh, m_LossLow, m_MinimumGamble, m_CommandDown, m_CommandUp, m_PersonalCooldownSeconds, m_WinHigh, m_WinLow, m_CommandPermission, m_ShowPermission, m_Admins
	if data.IsChatMessage() and data.GetParam(0).lower() == m_Command.lower():
	
		if not Parent.HasPermission(data.User, m_CommandPermission, ""):
			Parent.SendTwitchMessage("/me No permission to use command...")
			return
		
		if Parent.IsOnUserCooldown(ScriptName, m_Command, data.User) and not data.GetParam(1).lower() == "edit" and not data.GetParam(1).lower() == "show" and not data.GetParam(1).lower() == "editors":
			MyPersonalCooldown = Parent.GetUserCooldownDuration(ScriptName, m_Command, data.User)
			Message = "MyUser got a cooldown on MyPersonalCooldown seconds for the command."
			Message = Message.replace("MyPersonalCooldown", str(MyPersonalCooldown))
			Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
			if IfPersonalCooldownMessage == "true":
				Parent.SendTwitchMessage(Message)
			return
			
		if Parent.IsOnCooldown(ScriptName, m_Command) and not data.GetParam(1).lower() == "edit" and not data.GetParam(1).lower() == "show" and not data.GetParam(1).lower() == "editors":
			MyChannelCooldown = Parent.GetCooldownDuration(ScriptName, m_Command)
			Message = "There are still a channel cooldown on MyChannelCooldown seconds for the command."
			Message = Message.replace("MyChannelCooldown", str(MyChannelCooldown))
			if IfChannelCooldownMessage == "true":
				Parent.SendTwitchMessage(Message)
			return
	
		Param1 = data.GetParam(1).lower()
		Param2 = data.GetParam(2).lower()
		Param3 = data.GetParam(3).lower()
		
		if data.GetParamCount() == 1:
			Message = "MyCommand [number/percentage] | MyCommand random [number/percentage] [number/percentage]"
			Message = Message.replace("MyCommand", str(m_Command))
			Parent.SendTwitchMessage(Message)		
			return

		if Param1 == "all":
			Param1 = str(Parent.GetPoints(data.User))
		if Param2 == "all":
			Param2 = str(Parent.GetPoints(data.User))
		if Param3 == "all":
			Param3 = str(Parent.GetPoints(data.User))
			
		if "%" in Param1:
			try:
				Param1 = Param1.replace("%", "")
				Param1 = Param1.replace(",", ".")
				Param1 = float(Param1)
				Param1 = Param1 / 100
				Param1 = round(Param1 * Parent.GetPoints(data.User))
				Param1 = str(int(Param1))
			except ValueError:
				Message = "Please insert valid data, MyCommand for instructions"
				Message = Message.replace("MyCommand", str(m_Command))
				Parent.SendTwitchMessage(Message)
				return

		if "%" in Param2:
			try:
				Param2 = Param2.replace("%", "")
				Param2 = Param2.replace(",", ".")
				Param2 = float(Param2)
				Param2 = Param2 / 100
				Param2 = round(Param2 * Parent.GetPoints(data.User))
				Param2 = str(int(Param2))
			except ValueError:
				Message = "Please insert valid data, MyCommand for instructions"
				Message = Message.replace("MyCommand", str(m_Command))
				Parent.SendTwitchMessage(Message)
				return

		if "%" in Param3:
			try:
				Param3 = Param3.replace("%", "")
				Param3 = Param3.replace(",", ".")
				Param3 = float(Param3)
				Param3 = Param3 / 100
				Param3 = round(Param3 * Parent.GetPoints(data.User))
				Param3 = str(int(Param3))
			except ValueError:
				Message = "Please insert valid data, MyCommand for instructions"
				Message = Message.replace("MyCommand", str(m_Command))
				Parent.SendTwitchMessage(Message)
				return
		
		if Param1.isdigit() and data.GetParamCount() == 2:
			if int(Param1) < m_MinimumGamble:
				Message = "You have to gamble at least MinimumGamble..."
				Message = Message.replace("MinimumGamble", str(m_MinimumGamble))
				Message = Message.replace("MyCurrency", str(Parent.GetCurrencyName()))
				Parent.SendTwitchMessage(Message)
				return
			MyGamble = int(Param1)
			MyPoints = int(Parent.GetPoints(data.User))
			if MyGamble <= MyPoints:
				WinOrLoss = Parent.GetRandom(1, 101)
				Roll = Parent.GetRandom(1, 101)
				if m_WinLow <= WinOrLoss <= m_WinHigh:
					Parent.AddPoints(data.User, MyGamble)
					Message = "Rolled MyRoll: MyUser won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
					Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
					Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
					Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
					Message = Message.replace("MyGamble", str(MyGamble))
					Message = Message.replace("MyRoll", str(Roll))
					Parent.SendTwitchMessage(Message)
					Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
					Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
					return
					
				if m_LossLow <= WinOrLoss <= m_LossHigh:
					Parent.RemovePoints(data.User, MyGamble)
					Message = "Rolled MyRoll: MyUser lost MyGamble MyCurrency in gamble and now has MyPoints MyCurrency..."
					Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
					Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
					Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
					Message = Message.replace("MyGamble", str(MyGamble))
					Message = Message.replace("MyRoll", str(Roll))
					Parent.SendTwitchMessage(Message)
					Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
					Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
					return
					
				if m_HugeWinLow <= WinOrLoss <= m_HugeWinHigh:
					Parent.AddPoints(data.User, MyGamble*2)
					Message = "Rolled MyRoll: MyUser got a huge win and won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
					Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
					Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
					Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
					Message = Message.replace("MyGamble", str(MyGamble*2))
					Message = Message.replace("MyRoll", str(Roll))
					Parent.SendTwitchMessage(Message)
					Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
					Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
					return
					
			else:
				Message = "Not enough to gamble MyGamble MyCurrency MyUser, you have MyPoints MyCurrency"
				Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
				Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
				Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
				Message = Message.replace("MyGamble", str(MyGamble))
				Parent.SendTwitchMessage(Message)
				return
				
		elif Param1.lower() == "random" and data.GetParamCount() == 4 and Param2.isdigit() and Param3.isdigit():
			MyNum1 = int(Param2)
			MyNum2 = int(Param3)
			MyPoints = int(Parent.GetPoints(data.User))
			
			if MyNum1 < MyNum2:
				if MyNum2 > MyPoints:
					Message = "Not enough to gamble MyGamble MyCurrency MyUser, you have MyPoints MyCurrency"
					Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
					Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
					Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
					Message = Message.replace("MyGamble", str(MyNum2))
					Parent.SendTwitchMessage(Message)
					return
					
				else:
					MyGamble = Parent.GetRandom(MyNum1, MyNum2 + 1)
					Roll = Parent.GetRandom(1, 101)
					WinOrLoss = Parent.GetRandom(1, 101)
					
					if m_WinLow <= WinOrLoss <= m_WinHigh:
						Parent.AddPoints(data.User, MyGamble)
						Message = "Rolled MyRoll: MyUser won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
						
					if m_LossLow <= WinOrLoss <= m_LossHigh:
						Parent.RemovePoints(data.User, MyGamble)
						Message = "Rolled MyRoll: MyUser lost MyGamble MyCurrency in gamble and now has MyPoints MyCurrency..."
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
						
					if m_HugeWinLow <= WinOrLoss <= m_HugeWinHigh:
						Parent.AddPoints(data.User, MyGamble*2)
						Message = "Rolled MyRoll: MyUser got a huge win and won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble*2))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
					

			elif MyNum1 > MyNum2:
				if MyNum1 > MyPoints:
					Message = "Not enough to gamble MyGamble MyCurrency MyUser, you have MyPoints MyCurrency"
					Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
					Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
					Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
					Message = Message.replace("MyGamble", str(MyNum1))
					Parent.SendTwitchMessage(Message)
					return
					
				else:
					MyGamble = Parent.GetRandom(MyNum2, MyNum1 + 1)
					Roll = Parent.GetRandom(1, 101)
					WinOrLoss = Parent.GetRandom(1, 101)
					
					if m_WinLow <= WinOrLoss <= m_WinHigh:
						Parent.AddPoints(data.User, MyGamble)
						Message = "Rolled MyRoll: MyUser won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
						
					if m_LossLow <= WinOrLoss <= m_LossHigh:
						Parent.RemovePoints(data.User, MyGamble)
						Message = "Rolled MyRoll: MyUser lost MyGamble MyCurrency in gamble and now has MyPoints MyCurrency..."
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
						
					if m_HugeWinLow <= WinOrLoss <= m_HugeWinHigh:
						Parent.AddPoints(data.User, MyGamble*2)
						Message = "Rolled MyRoll: MyUser got a huge win and won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble*2))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return

			elif MyNum1 == MyNum2:
				if MyNum1 > MyPoints:
					Message = "Not enough to gamble MyGamble MyCurrency MyUser, you have MyPoints MyCurrency"
					Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
					Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
					Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
					Message = Message.replace("MyGamble", str(MyNum1))
					Parent.SendTwitchMessage(Message)
					return
					
				else:
					MyGamble = Parent.GetRandom(MyNum1, MyNum2 + 1)
					Roll = Parent.GetRandom(1, 101)
					WinOrLoss = Parent.GetRandom(1, 101)
					
					if m_WinLow <= WinOrLoss <= m_WinHigh:
						Parent.AddPoints(data.User, MyGamble)
						Message = "Rolled MyRoll: MyUser won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
						
					if m_LossLow <= WinOrLoss <= m_LossHigh:
						Parent.RemovePoints(data.User, MyGamble)
						Message = "Rolled MyRoll: MyUser lost MyGamble MyCurrency in gamble and now has MyPoints MyCurrency..."
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return
						
					if m_HugeWinLow <= WinOrLoss <= m_HugeWinHigh:
						Parent.AddPoints(data.User, MyGamble*2)
						Message = "Rolled MyRoll: MyUser got a huge win and won MyGamble MyCurrency in gamble and now has MyPoints MyCurrency!"
						Message = Message.replace("MyCurrency", Parent.GetCurrencyName())
						Message = Message.replace("MyPoints", str(Parent.GetPoints(data.User)))
						Message = Message.replace("MyUser", Parent.GetDisplayName(data.User))
						Message = Message.replace("MyGamble", str(MyGamble*2))
						Message = Message.replace("MyRoll", str(Roll))
						Parent.SendTwitchMessage(Message)
						Parent.AddCooldown(ScriptName, m_Command, m_ChannelCooldownSeconds)
						Parent.AddUserCooldown(ScriptName, m_Command, data.User, m_PersonalCooldownSeconds)
						return

						
		if data.GetParam(1).lower() == "edit":
			if data.User in m_Admins or data.User == Parent.GetChannelName().lower():
				if data.GetParam(2).lower() == "channelcooldown" and data.GetParamCount() == 4 and data.GetParam(3).isdigit():
					with open(ChannelCooldownFile, "w+") as f:
						f.write(str(data.GetParam(3)))
						m_ChannelCooldownSeconds = int(data.GetParam(3))
						Message = "The channel cooldown for the command is now MyCooldown seconds."
						Message = Message.replace("MyCooldown", str(m_ChannelCooldownSeconds))
						Parent.SendTwitchMessage(Message)
						return
				
				if data.GetParam(2).lower() == "command" and data.GetParamCount() == 4:
					with open(CommandFile, "w+") as f:
						f.write(str(data.GetParam(3).lower()))
						m_Command = str(data.GetParam(3).lower())
						Message = "The the new command is now MyCommand."
						Message = Message.replace("MyCommand", str(m_Command))
						Parent.SendTwitchMessage(Message)
						return
						
				if data.GetParam(2).lower() == "2xwin" and data.GetParamCount() == 5 and data.GetParam(3).isdigit() and data.GetParam(4).isdigit():
					with open(HugeWinHighFile, "w+") as f:
						f.write(str(data.GetParam(4)))
						m_HugeWinHigh = int(data.GetParam(4))
					with open(HugeWinLowFile, "w+") as f:
						f.write(str(data.GetParam(3)))
						m_HugeWinLow = int(data.GetParam(3))
					Message = "When randomizer picks or picks between MyNumberLow and MyNumberHigh is there now a big win (2x gamble). Make sure the other numbers do not collide! >>> Have to be low - high!"
					Message = Message.replace("MyNumberLow", str(data.GetParam(3)))
					Message = Message.replace("MyNumberHigh", str(data.GetParam(4)))
					Parent.SendTwitchMessage(Message)
					Message = "Win: [1] - [2] | Loss: [3] - [4] | Big Win: [5] - [6] (Not the roll numbers!)"
					Message = Message.replace("[1]", str(m_WinLow))
					Message = Message.replace("[2]", str(m_WinHigh))
					Message = Message.replace("[3]", str(m_LossLow))
					Message = Message.replace("[4]", str(m_LossHigh))
					Message = Message.replace("[5]", str(m_HugeWinLow))
					Message = Message.replace("[6]", str(m_HugeWinHigh))
					Parent.SendTwitchMessage(Message)
					return
							
				if data.GetParam(2).lower() == "channelcooldownmessage" and data.GetParamCount() == 4:
					if data.GetParam(3).lower() == "true" or data.GetParam(3).lower() == "false":
						with open(IfChannelCooldownMessageFile, "w+") as f:
							f.write(str(data.GetParam(3).lower()))
							IfChannelCooldownMessage = str(data.GetParam(3).lower())
							Message = "Message for global cooldown is now set to MyStatus"
							Message = Message.replace("MyStatus", str(data.GetParam(3).lower()))
							Parent.SendTwitchMessage(Message)
							return
							
				if data.GetParam(2).lower() == "personalcooldownmessage" and data.GetParamCount() == 4:
					if data.GetParam(3).lower() == "true" or data.GetParam(3).lower() == "false":
						with open(IfPersonalCooldownMessageFile, "w+") as f:
							f.write(str(data.GetParam(3).lower()))
							IfPersonalCooldownMessage = str(data.GetParam(3).lower())
							Message = "Message for personal cooldown is now set to MyStatus"
							Message = Message.replace("MyStatus", str(data.GetParam(3).lower()))
							Parent.SendTwitchMessage(Message)
							return
				
				if data.GetParam(2).lower() == "loss" and data.GetParamCount() == 5 and data.GetParam(3).isdigit() and data.GetParam(4).isdigit():
					with open(LossHighFile, "w+") as f:
						f.write(str(data.GetParam(4)))
						m_LossHigh = int(data.GetParam(4))
					with open(LossLowFile, "w+") as f:
						f.write(str(data.GetParam(3)))
						m_LossLow = int(data.GetParam(3))
					Message = "When randomizer picks or picks between MyNumberLow and MyNumberHigh is there now a loss, make sure the other numbers do not collide!"
					Message = Message.replace("MyNumberLow", str(data.GetParam(3)))
					Message = Message.replace("MyNumberHigh", str(data.GetParam(4)))
					Parent.SendTwitchMessage(Message)
					Message = "Win: [1] - [2] | Loss: [3] - [4] | 2xWin: [5] - [6] (Not the roll numbers!)"
					Message = Message.replace("[1]", str(m_WinLow))
					Message = Message.replace("[2]", str(m_WinHigh))
					Message = Message.replace("[3]", str(m_LossLow))
					Message = Message.replace("[4]", str(m_LossHigh))
					Message = Message.replace("[5]", str(m_HugeWinLow))
					Message = Message.replace("[6]", str(m_HugeWinHigh))
					Parent.SendTwitchMessage(Message)
					return

				if data.GetParam(2).lower() == "commandofflinemessage" and data.GetParamCount() == 4:
					if data.GetParam(3).lower() == "true" or data.GetParam(3).lower() == "false":
						with open(OfflineMessageFile, "w+") as f:
							f.write(str(data.GetParam(3).lower()))
							m_CommandDown = str(data.GetParam(3).lower())
							Message = "Message when command goes offline is now set to MyStatus"
							Message = Message.replace("MyStatus", str(data.GetParam(3).lower()))
							Parent.SendTwitchMessage(Message)
							return

				if data.GetParam(2).lower() == "commandonlinemessage" and data.GetParamCount() == 4:
					if data.GetParam(3).lower() == "true" or data.GetParam(3).lower() == "false":
						with open(OnlineMessageFile, "w+") as f:
							f.write(str(data.GetParam(3).lower()))
							m_CommandUp = str(data.GetParam(3).lower())
							Message = "Message when command goes online is now set to MyStatus"
							Message = Message.replace("MyStatus", str(data.GetParam(3).lower()))
							Parent.SendTwitchMessage(Message)
							return

				if data.GetParam(2).lower() == "commandpermission" and data.GetParamCount() == 4:
					if data.GetParam(3).lower() == "everyone" or data.GetParam(3).lower() == "regular" or data.GetParam(3).lower() == "subscriber" or data.GetParam(3).lower() == "moderator" or data.GetParam(3).lower() == "editor" or data.GetParam(3).lower() == "caster":
						with open(PermissionFile, "w+") as f:
							f.write(str(data.GetParam(3).lower()))
							m_CommandPermission = str(data.GetParam(3).lower())
							Message = "The required permission for the command is now set to MyPermission"
							Message = Message.replace("MyPermission", str(data.GetParam(3).lower()))
							Parent.SendTwitchMessage(Message)
							return
					if data.GetParam(3).lower() == "gamewisp_subscriber":
						with open(PermissionFile, "w+") as f:
							f.write("GameWisp Subscriber")
							m_CommandPermission = "GameWisp Subscriber"
							Message = "The required permission for the command is now set to MyPermission"
							Message = Message.replace("MyPermission", "GameWisp Subscriber")
							Parent.SendTwitchMessage(Message)
							return
				
				if data.GetParam(2).lower() == "whocanshow" and data.GetParamCount() == 4:
					if data.GetParam(3).lower() == "everyone" or data.GetParam(3).lower() == "regular" or data.GetParam(3).lower() == "subscriber" or data.GetParam(3).lower() == "moderator" or data.GetParam(3).lower() == "editor" or data.GetParam(3).lower() == "caster":
						with open(ShowPermissionFile, "w+") as f:
							f.write(str(data.GetParam(3).lower()))
							m_ShowPermission = str(data.GetParam(3).lower())
							Message = "The required permission to use show is now set to MyPermission"
							Message = Message.replace("MyPermission", str(data.GetParam(3).lower()))
							Parent.SendTwitchMessage(Message)
							return
					if data.GetParam(3).lower() == "gamewisp_subscriber":
						with open(ShowPermissionFile, "w+") as f:
							f.write("GameWisp Subscriber")
							m_ShowPermission = "GameWisp Subscriber"
							Message = "The required permission to use show is now set to MyPermission"
							Message = Message.replace("MyPermission", "GameWisp Subscriber")
							Parent.SendTwitchMessage(Message)
							return

				if data.GetParam(2).lower() == "personalcooldown" and data.GetParamCount() == 4 and data.GetParam(3).isdigit():
					with open(PersonalCooldownFile, "w+") as f:
						f.write(str(data.GetParam(3)))
						m_PersonalCooldownSeconds = int(data.GetParam(3))
						Message = "The personal cooldown for the command is now MyCooldown seconds."
						Message = Message.replace("MyCooldown", str(m_PersonalCooldownSeconds))
						Parent.SendTwitchMessage(Message)
						return

				if data.GetParam(2).lower() == "win" and data.GetParamCount() == 5 and data.GetParam(3).isdigit() and data.GetParam(4).isdigit():
					with open(WinHighFile, "w+") as f:
						f.write(str(data.GetParam(4)))
						m_WinHigh = int(data.GetParam(4))
					with open(WinLowFile, "w+") as f:
						f.write(str(data.GetParam(3)))
						m_WinLow = int(data.GetParam(3))
					Message = "When randomizer picks or picks between MyNumberLow and MyNumberHigh is there now a win, make sure the other numbers do not collide!"
					Message = Message.replace("MyNumberLow", str(data.GetParam(3)))
					Message = Message.replace("MyNumberHigh", str(data.GetParam(4)))
					Parent.SendTwitchMessage(Message)
					Message = "Win: [1] - [2] | Loss: [3] - [4] | 2xWin: [5] - [6] (Not the roll numbers!)"
					Message = Message.replace("[1]", str(m_WinLow))
					Message = Message.replace("[2]", str(m_WinHigh))
					Message = Message.replace("[3]", str(m_LossLow))
					Message = Message.replace("[4]", str(m_LossHigh))
					Message = Message.replace("[5]", str(m_HugeWinLow))
					Message = Message.replace("[6]", str(m_HugeWinHigh))
					Parent.SendTwitchMessage(Message)
					return

				if data.GetParam(2).lower() == "minimumgamble" and data.GetParamCount() == 4 and data.GetParam(3).isdigit:
					with open(MinimumGambleFile, "w+") as f:
						f.write(str(data.GetParam(3)))
						m_MinimumGamble = int(data.GetParam(3))
						Message = "Minimum gamble is now set to MinGamble MyCurrency"
						Message = Message.replace("MinGamble", str(data.GetParam(3)))
						Message = Message.replace("MyCurrency", str(Parent.GetCurrencyName()))
						Parent.SendTwitchMessage(Message)
						return
		
		if data.GetParam(1).lower() == "show":
			if not Parent.HasPermission(data.User, m_ShowPermission, ""):
				Parent.SendTwitchMessage("/me No permission to show data...")
				return
			if data.GetParam(2).lower() == "winorloss" and data.GetParamCount() == 3:
				Message = "Win: [1] - [2] | Loss: [3] - [4] | 2xWin: [5] - [6] (Not the roll numbers!)"
				Message = Message.replace("[1]", str(m_WinLow))
				Message = Message.replace("[2]", str(m_WinHigh))
				Message = Message.replace("[3]", str(m_LossLow))
				Message = Message.replace("[4]", str(m_LossHigh))
				Message = Message.replace("[5]", str(m_HugeWinLow))
				Message = Message.replace("[6]", str(m_HugeWinHigh))
				Parent.SendTwitchMessage(Message)
				return

			if data.GetParam(2).lower() == "commandpermission" and data.GetParamCount() == 3:
				Message = "Current permission for the command: MyPermission"
				Message = Message.replace("MyPermission", str(m_CommandPermission))
				Parent.SendTwitchMessage(Message)
				return

			if data.GetParam(2).lower() == "minimumgamble" and data.GetParamCount() == 3:
				Message = "Minimum to gamble: MinimumGamble MyCurrency"
				Message = Message.replace("MinimumGamble", str(m_MinimumGamble))
				Message = Message.replace("MyCurrency", str(Parent.GetCurrencyName()))
				Parent.SendTwitchMessage(Message)
				return
				
			if data.GetParam(2).lower() == "channelcooldown" and data.GetParamCount() == 3:
				Message = "Current channel cooldown: MyChannelCooldown seconds"
				Message = Message.replace("MyChannelCooldown", str(m_ChannelCooldownSeconds))
				Parent.SendTwitchMessage(Message)
				return
			
			if data.GetParam(2).lower() == "personalcooldown" and data.GetParamCount() == 3:
				Message = "Current personal cooldown: MyPersonalCooldown seconds"
				Message = Message.replace("MyPersonalCooldown", str(m_PersonalCooldownSeconds))
				Parent.SendTwitchMessage(Message)
				return
			
			if data.GetParam(2).lower() == "personalcooldownmessage" and data.GetParamCount() == 3:
				Message = "Response on personal cooldown is set to MyStatus"
				Message = Message.replace("MyStatus", str(IfPersonalCooldownMessage))
				Parent.SendTwitchMessage(Message)
				return
			
			if data.GetParam(2).lower() == "channelcooldownmessage" and data.GetParamCount() == 3:
				Message = "Response on channel cooldown is set to MyStatus"
				Message = Message.replace("MyStatus", str(IfChannelCooldownMessage))
				Parent.SendTwitchMessage(Message)
				return
			
			if data.GetParam(2).lower() == "commandofflinemessage" and data.GetParamCount() == 3:
				Message = "Response when command goes offline is set to MyStatus"
				Message = Message.replace("MyStatus", str(m_CommandDown))
				Parent.SendTwitchMessage(Message)
				return
			
			if data.GetParam(2).lower() == "commandonlinemessage" and data.GetParamCount() == 3:
				Message = "Response when command goes online is set to MyStatus"
				Message = Message.replace("MyStatus", str(m_CommandUp))
				Parent.SendTwitchMessage(Message)
				return
			if data.GetParam(2).lower() == "editors" and data.GetParamCount() == 3:
				Message = "Current editors for the command: MyEditors"
				Message = Message.replace("MyEditors", str(m_Admins))
				Message = Message.replace("[", "")
				Message = Message.replace("]", "")
				Message = Message.replace("'", "")
				Parent.SendTwitchMessage(Message)
				return

			if data.GetParam(2).lower() == "whocanshow" and data.GetParamCount() == 3:
				Message = "The permission to use show is set to MyPermission"
				Message = Message.replace("MyPermission", str(m_ShowPermission))
				Parent.SendTwitchMessage(Message)
				return
				
		if data.GetParam(1).lower() == "download" and data.GetParamCount() == 2:
			Parent.SendTwitchMessage("Scripts from Yazaar can be found and downloaded here: https://github.com/Yazaar/Streamlabs-Chatbot-Scripts")
	if data.IsChatMessage() and data.GetParam(0).lower() == "!gamblescriptcommand" and data.GetParamCount() == 1:
		Message = "The command for the gamble script is MyCommand"
		Message = Message.replace("MyCommand", str(m_Command))
		Parent.SendTwitchMessage(Message)
		return

	if data.IsChatMessage() and data.GetParam(0).lower() == m_Command and data.GetParamCount() == 4:
		if data.GetParam(1).lower() == "editors" and data.GetParamCount() == 4:
			if data.User == Parent.GetChannelName().lower():
				if data.GetParam(2).lower() == "add":
					if not str(data.GetParam(3).lower()) in m_Admins:
						m_Admins.append(str(data.GetParam(3).lower()))
						with open(AdminsFile, "wb") as f:
							pickle.dump(m_Admins, f)
						Message = "MyUser is now an editor for the command!"
						Message = Message.replace("MyUser", str(data.GetParam(3).lower()))
						Parent.SendTwitchMessage(Message)
						return
					else:
						Message = "MyUser is already an editor for the command!"
						Message = Message.replace("MyUser", str(data.GetParam(3).lower()))
						Parent.SendTwitchMessage(Message)
						return
						
				if data.GetParam(2).lower() == "remove":
					if str(data.GetParam(3).lower()) in m_Admins:
						m_Admins.remove(str(data.GetParam(3).lower()))
						with open(AdminsFile, "wb") as f:
							pickle.dump(m_Admins, f)
						Message = "MyUser is no longer an editor for the command!"
						Message = Message.replace("MyUser", str(data.GetParam(3).lower()))
						Parent.SendTwitchMessage(Message)
						return
					else:
						Message = "MyUser is not an editor for the command!"
						Message = Message.replace("MyUser", str(data.GetParam(3).lower()))
						Parent.SendTwitchMessage(Message)
						return
			else:
				Message = "Only MyUser can manage editors for the command..."
				Message = Message.replace("MyUser", str(Parent.GetDisplayName((Parent.GetChannelName().lower()))))
				Parent.SendTwitchMessage(Message)
				return
#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return
 
#---------------------------------------
# Command Shutdown Function
#---------------------------------------
def Unload():
	if m_CommandDown == "true":
		Parent.SendTwitchMessage("/me Gamble went offline")
