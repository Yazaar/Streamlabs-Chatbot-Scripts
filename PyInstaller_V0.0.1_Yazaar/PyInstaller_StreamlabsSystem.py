#---------------------------------------
# Import Libraries
#---------------------------------------
import codecs, json, os, zipfile

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts
"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "PyInstaller"
Website = "https://www.twitch.tv/yazaar"
Description = "PyInstaller - Install scripts thru the chat"
Creator = "Yazaar"
Version = "0.0.1"
#---------------------------------------
# Variables + Files
#---------------------------------------

SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
PyInstallerFile = os.path.join(os.path.dirname(__file__), "PyInstaller.py")
PyInstallerZip = os.path.join(os.path.dirname(__file__), "PyInstallerSoftware.zip")
FreshInstallFile = os.path.join(os.path.dirname(__file__), "FreshInstall.txt")
InformationFile = os.path.join(os.path.dirname(__file__), "Information.txt")
InstallConfirmerFile = os.path.join(os.path.dirname(__file__), "InstallConfirmer.txt")


with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
  Settings = json.load(f, encoding='utf-8-sig')
  Settings["PyPath"] = os.__file__[:-9] + "Python"

with open(FreshInstallFile, 'r') as f:
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
  if data.GetParam(0).lower() == Settings["Command"] and data.GetParamCount() == 1:
    if NoPermission(data):
      return
    Parent.SendStreamMessage("Take a look here for available scripts: https://yazaar.github.io/Streamlabs-PyInstaller-Properties/")
    return

  if data.GetParam(0).lower() == Settings["Command"] and data.GetParamCount() == 2:

    if Parent.IsOnUserCooldown(ScriptName,Settings["Command"],data.User):
      return

    if NoPermission(data):
      return

    root_json = Parent.GetRequest('https://raw.githubusercontent.com/Yazaar/Streamlabs-PyInstaller-Properties/master/data.json', {})
    root_json = json.loads(root_json)

    if not os.path.isfile(PyInstallerFile):
      with zipfile.ZipFile(PyInstallerZip, 'r') as f:
        f.extractall(path=os.path.dirname(__file__))

    try:
      json_download = json.loads(root_json["response"])[str(data.GetParam(1)).lower()]["download"]
      os.system("cd Services\Scripts\PyInstaller & " + Settings["PyPath"] + " PyInstaller.py " + str(json_download))
      Parent.SendStreamMessage("/me [PyInstaller] Installation of " + str(data.GetParam(1)) + " should be complete.")

    except Exception:
      Parent.SendStreamMessage("Does not exist, take a look here for available scripts: https://yazaar.github.io/Streamlabs-PyInstaller-Properties/")

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
  return


#---------------------------------------
# OTHER SCRIPT FUNCTIONS
#---------------------------------------
def NoPermission(data):
  if Settings["Permission"] == "User_Specific":
    if data.User in Settings["PermissionInfo"].lower().split(" "):
      return False
    else:
      Parent.SendStreamMessage("No permission!")
      Parent.AddUserCooldown(ScriptName,Settings["Command"],data.User,Settings["Cooldown"])
      return True

  if not Parent.HasPermission(data.User, Settings["Permission"], Settings["PermissionInfo"]):
    Parent.SendStreamMessage("No permission!")
    Parent.AddUserCooldown(ScriptName,Settings["Command"],data.User,Settings["Cooldown"])
    return True
  else:
    return False

def ReloadPyInstallerScript():
  global Settings
  with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
    Settings = json.load(f, encoding='utf-8-sig')
  return

def OpenPyInstallerInfo():
  os.startfile(InformationFile)
  return