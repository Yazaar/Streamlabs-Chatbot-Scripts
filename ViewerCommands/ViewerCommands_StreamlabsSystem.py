#---------------------------------------
# Import Libraries
#---------------------------------------
import os
import pickle

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts
"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "ViewerComs"
Website = "https://www.twitch.tv/yazaar"
Description = "Create a command that a specific user can control"
Creator = "Yazaar"
Version = "0.0.1"
#---------------------------------------
# Variables + Files
#---------------------------------------

UsersFile = os.path.join(os.path.dirname(__file__), "Settings\Users.pickle")
FreshInstallFile = os.path.join(os.path.dirname(__file__), "Settings\FreshInstall.txt")
InformationFile = os.path.join(os.path.dirname(__file__), "Information.txt")

#---------------------------------------
# READ FILES
#---------------------------------------
with open(UsersFile, "rb") as f:
    m_Users = pickle.load(f)

with open(FreshInstallFile, "r") as f:
    m_FreshInstall = f.read()
#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	global m_FreshInstall
	if m_FreshInstall == "true":
		m_FreshInstall = "false"
	
		with open(FreshInstallFile, "w+") as f:
			f.write(m_FreshInstall)
	
		os.startfile(InformationFile)
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global m_Users
	if data.IsChatMessage() and data.GetParam(0).lower() == "!mycom":
	
		if Parent.IsOnUserCooldown(ScriptName, "!viewercom", data.User) and not Parent.HasPermission(data.User, "moderator", ""):
			Message = "MyUser got a cooldown on MyCooldown seconds..."
			Message = Message.replace("MyUser", str(Parent.GetDisplayName(data.User)))
			Message = Message.replace("MyCooldown", str(Parent.GetUserCooldownDuration(ScriptName, "!viewercom", data.User)))
			Parent.SendTwitchMessage(Message)
			return
		
		if Parent.IsOnCooldown(ScriptName, "!viewercom"):
			Message = "There are a general cooldown on MyCooldown seconds..."
			Message = Message.replace("MyCooldown", str(Parent.GetCooldownDuration(ScriptName, "!viewercom")))
			Parent.SendTwitchMessage(Message)
			return

		if data.GetParam(1).lower() == "add" and data.GetParamCount() == 3:

			if not Parent.HasPermission(data.User, "moderator", ""):
				Parent.SendTwitchMessage("/me No permission to add user commands")
				Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 60)
				return

			if str(data.GetParam(2).lower()) in m_Users:
				Message = "/me MyUser got a command already"
				Message = Message.replace("MyUser", str(Parent.GetDisplayName(data.GetParam(2).lower())))
				Parent.SendTwitchMessage(Message)
				return

			m_Users.append(str(data.GetParam(2).lower()))
			with open(UsersFile, "wb") as f:
				pickle.dump(m_Users, f)
			Parent.SendTwitchMessage(str("!addcom !" + str(data.GetParam(2).lower()) + " NEW"))
			Parent.AddCooldown(ScriptName, "!viewercom", 5)
			return
		
		if data.GetParam(1).lower() == "users" and data.GetParamCount() == 2:

			if not Parent.HasPermission(data.User, "moderator", ""):
				Parent.SendTwitchMessage("/me No permission to show users with commands")
				Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 60)
				return
		
			Message = "Current users with command: MyUser"
			Message = Message.replace("MyUser", str(m_Users))
			Message = Message.replace("[", "")
			Message = Message.replace("]", "")
			Message = Message.replace("'", "")
			Parent.SendTwitchMessage(Message)
			return

		if data.GetParam(1).lower() == "remove" and data.GetParamCount() == 3 or data.GetParam(1).lower() == "delete" and data.GetParamCount() == 3:
		
			if not Parent.HasPermission(data.User, "moderator", ""):
				Parent.SendTwitchMessage("/me No permission to remove user commands")
				Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 60)
				return
			
			if not str(data.GetParam(2).lower()) in m_Users:
				Message = "/me MyUser got no command"
				Message = Message.replace("MyUser", str(Parent.GetDisplayName(data.GetParam(2).lower())))
				Parent.SendTwitchMessage(Message)
				return
			
			m_Users.remove(str(data.GetParam(2).lower()))
			with open(UsersFile, "wb") as f:
				pickle.dump(m_Users, f)
			Parent.SendTwitchMessage(str("!delcom !" + str(data.GetParam(2).lower()) + " NEW"))
			Parent.AddCooldown(ScriptName, "!viewercom", 5)
			return
		
		if data.GetParam(1).lower() == "set":
			if not data.User in m_Users:
				Parent.SendTwitchMessage("You need a personal command to use this function")
				Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 20)
				return
			
			Message = data.Message
			Message = Message.replace("!mycom set ", "")
			if Message.find("!") == 0:
				Parent.SendTwitchMessage("You can not start with: !")
				Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 10)
				return
			if Message.find("/") == 0:
				Parent.SendTwitchMessage("You can not start with: /")
				Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 10)
				return
			
			Message = str("!editcom !" + str(data.User) + " " + str(Message))
			Parent.SendTwitchMessage(Message)
			Parent.AddUserCooldown(ScriptName, "!viewercom", str(data.User), 120)
			Parent.AddCooldown(ScriptName, "!viewercom", 5)
			
	
		if data.GetParam(1).lower() == "information" and data.GetParamCount() == 2 and data.User == Parent.GetChannelName().lower():
			os.startfile(InformationFile)
			return
		
		if data.GetParam(1).lower() == "download" and data.GetParamCount() == 2:
			Parent.SendTwitchMessage("Downlaod this and other scripts by Yazaar on https://github.com/Yazaar/Streamlabs-Chatbot-Scripts")
			
#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return
 
#---------------------------------------
# Command Shutdown Function
#---------------------------------------
def Unload():
 return