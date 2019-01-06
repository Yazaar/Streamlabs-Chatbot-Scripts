#---------------------------------------
# Import Libraries
#---------------------------------------
import os
import datetime
import random
import json
import codecs

"""
DOWNLOAD LINK IF ISSUES:
https://github.com/Yazaar/Streamlabs-Chatbot-Scripts
"""
#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Warn&Announce"
Website = "https://www.twitch.tv/yazaar"
Description = "Send warnings and announcements on stream as an overlay!"
Creator = "Yazaar"
Version = "0.0.1"
#---------------------------------------
# Variables + Files
#---------------------------------------

css_colors = {'aliceblue': '#f0f8ff', 'antiquewhite': '#faebd7', 'aqua': '#00ffff', 'aquamarine': '#7fffd4', 'azure': '#f0ffff', 'beige': '#f5f5dc', 'bisque': '#ffe4c4', 'black': '#000000', 'blanchedalmond': '#ffebcd', 'blue': '#0000ff', 'blueviolet': '#8a2be2', 'brown': '#a52a2a', 'burlywood': '#deb887', 'cadetblue': '#5f9ea0', 'chartreuse': '#7fff00', 'chocolate': '#d2691e', 'coral': '#ff7f50', 'cornflowerblue': '#6495ed', 'cornsilk': '#fff8dc', 'crimson': '#dc143c', 'cyan': '#00ffff', 'darkblue': '#00008b', 'darkcyan': '#008b8b', 'darkgoldenrod': '#b8860b', 'darkgray': '#a9a9a9', 'darkgreen': '#006400', 'darkgrey': '#a9a9a9', 'darkkhaki': '#bdb76b', 'darkmagenta': '#8b008b', 'darkolivegreen': '#556b2f', 'darkorange': '#ff8c00', 'darkorchid': '#9932cc', 'darkred': '#8b0000', 'darksalmon': '#e9967a', 'darkseagreen': '#8fbc8f', 'darkslateblue': '#483d8b', 'darkslategray': '#2f4f4f', 'darkslategrey': '#2f4f4f', 'darkturquoise': '#00ced1', 'darkviolet': '#9400d3', 'deeppink': '#ff1493', 'deepskyblue': '#00bfff', 'dimgray': '#696969', 'dimgrey': '#696969', 'dodgerblue': '#1e90ff', 'firebrick': '#b22222', 'floralwhite': '#fffaf0', 'forestgreen': '#228b22', 'fuchsia': '#ff00ff', 'gainsboro': '#dcdcdc', 'ghostwhite': '#f8f8ff', 'gold': '#ffd700', 'goldenrod': '#daa520', 'gray': '#808080', 'green': '#008000', 'greenyellow': '#adff2f', 'grey': '#808080', 'honeydew': '#f0fff0', 'hotpink': '#ff69b4', 'indianred': '#cd5c5c', 'indigo': '#4b0082', 'ivory': '#fffff0', 'khaki': '#f0e68c', 'lavender': '#e6e6fa', 'lavenderblush': '#fff0f5', 'lawngreen': '#7cfc00', 'lemonchiffon': '#fffacd', 'lightblue': '#add8e6', 'lightcoral': '#f08080', 'lightcyan': '#e0ffff', 'lightgoldenrodyellow': '#fafad2', 'lightgray': '#d3d3d3', 'lightgreen': '#90ee90', 'lightgrey': '#d3d3d3', 'lightpink': '#ffb6c1', 'lightsalmon': '#ffa07a', 'lightseagreen': '#20b2aa', 'lightskyblue': '#87cefa', 'lightslategray': '#778899', 'lightslategrey': '#778899', 'lightsteelblue': '#b0c4de', 'lightyellow': '#ffffe0', 'lime': '#00ff00', 'limegreen': '#32cd32', 'linen': '#faf0e6', 'magenta': '#ff00ff', 'maroon': '#800000', 'mediumaquamarine': '#66cdaa', 'mediumblue': '#0000cd', 'mediumorchid': '#ba55d3', 'mediumpurple': '#9370db', 'mediumseagreen': '#3cb371', 'mediumslateblue': '#7b68ee', 'mediumspringgreen': '#00fa9a', 'mediumturquoise': '#48d1cc', 'mediumvioletred': '#c71585', 'midnightblue': '#191970', 'mintcream': '#f5fffa', 'mistyrose': '#ffe4e1', 'moccasin': '#ffe4b5', 'navajowhite': '#ffdead', 'navy': '#000080', 'oldlace': '#fdf5e6', 'olive': '#808000', 'olivedrab': '#6b8e23', 'orange': '#ffa500', 'orangered': '#ff4500', 'orchid': '#da70d6', 'palegoldenrod': '#eee8aa', 'palegreen': '#98fb98', 'paleturquoise': '#afeeee', 'palevioletred': '#db7093', 'papayawhip': '#ffefd5', 'peachpuff': '#ffdab9', 'peru': '#cd853f', 'pink': '#ffc0cb', 'plum': '#dda0dd', 'powderblue': '#b0e0e6', 'purple': '#800080', 'rebeccapurple': '#663399', 'red': '#ff0000', 'rosybrown': '#bc8f8f', 'royalblue': '#4169e1', 'saddlebrown': '#8b4513', 'salmon': '#fa8072', 'sandybrown': '#f4a460', 'seagreen': '#2e8b57', 'seashell': '#fff5ee', 'sienna': '#a0522d', 'silver': '#c0c0c0', 'skyblue': '#87ceeb', 'slateblue': '#6a5acd', 'slategray': '#708090', 'slategrey': '#708090', 'snow': '#fffafa', 'springgreen': '#00ff7f', 'steelblue': '#4682b4', 'tan': '#d2b48c', 'teal': '#008080', 'thistle': '#d8bfd8', 'tomato': '#ff6347', 'turquoise': '#40e0d0', 'violet': '#ee82ee', 'wheat': '#f5deb3', 'white': '#ffffff', 'whitesmoke': '#f5f5f5', 'yellow': '#ffff00', 'yellowgreen': '#9acd32'}

SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
informationfile = os.path.join(os.path.dirname(__file__), "information.txt")
freshinstallfile = os.path.join(os.path.dirname(__file__), "freshinstall.txt")
SoundPath = os.path.join(os.path.dirname(__file__), "sounds")

#---------------------------------------
# READ FILES
#---------------------------------------

with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
  Settings = json.load(f, encoding='utf-8-sig')

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
  with open(freshinstallfile, "r") as f:
    fresh = f.read()
  
  if fresh == "true":
    with open(informationfile, "r") as f:
      temp = f.read()
    temp = temp.replace("[NAME_OF_USER]", str(Parent.GetChannelName()))
    with open(informationfile, "w") as f:
      f.write(temp)
    with open(freshinstallfile, "w") as f:
      f.write("false")
    temp = ""
    fresh = "false"
    os.startfile(informationfile)
  return
	
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
  if data.GetParam(0).lower() == Settings["Command"].lower():

    if Parent.IsOnUserCooldown(ScriptName,Settings["Command"],data.User):
      return

    if NoPermission(data):
      return

    MyMessage = data.Message.lower().replace(Settings["Command"].lower() + " ", "")

    if MyMessage.split(" ")[0] == "-a":
      ActionType = "-a"
      ColorType = Settings["LightColorAnnounce"]
      MyMessage = MyMessage.replace("-a ", "")
    
    elif MyMessage.split(" ")[0] == "-w":
      ActionType = "-w"
      ColorType = Settings["LightColorWarning"]
      MyMessage = MyMessage.replace("-w ", "")

    elif len(MyMessage.split(" ")[0]) == 8 and MyMessage.split(" ")[0][1] == "#":
      for i in MyMessage.split(" ")[0][2:]:
        if i == "0" or i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9" or i.lower() == "a" or i.lower() == "b" or i.lower() == "c" or i.lower() == "d" or i.lower() == "e" or i.lower() == "f":
          pass
        else:
          Parent.SendStreamMessage("Send a valid request, include -w, -a, or valid HEXCODE as your second argument")
          return
      ColorType = MyMessage.split(" ")[0][1:]
      ActionType = "KeyCode"
      MyMessage = MyMessage.replace(MyMessage.split(" ")[0] + " ", "")

    elif MyMessage.split(" ")[0][1:] in css_colors:
      ActionType = "KeyCode"
      ColorType = MyMessage.split(" ")[0][1:]
      MyMessage = MyMessage.replace(MyMessage.split(" ")[0] + " ", "")
    
    else:
      Parent.SendStreamMessage("Send a valid request, include -w, -a, -[css-color name] (ex: -aquamarine) or -[HEXCODE] (ex: #a30ed1) as your second argument")
      return

    if MyMessage.split(" ")[0].lower() == "-mute":
      NoAudio = "true"
      MyMessage = MyMessage.replace("-mute ", "")
    else:
      NoAudio = "false"


    MyMessage = MyMessage.replace('"', '\\"').replace("<", "&lt").replace(">", "&gt")

    Parent.BroadcastWsEvent("Warnings&AnnouncementsByYazaar",'{"color": "[COLOR_TYPE]", "mute": "[STATUS_OF_MUTE]", "type": "[TYPE_OF_SOUND]", "message": "[SEND_MESSAGE]"}'.replace("[SEND_MESSAGE]", MyMessage).replace("[COLOR_TYPE]", ColorType.lower()).replace("[STATUS_OF_MUTE]", NoAudio).replace("[TYPE_OF_SOUND]", ActionType))
    return

def Tick():
 return



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

def ReloadWarnAnnounceScript():
  global Settings
  with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
    Settings = json.load(f, encoding='utf-8-sig')
  

def OpenWarnAnnounceInfo():
  os.startfile(informationfile)

def OpenWarnAnnounceSoundFiles():
  os.system('explorer "[PATH]"'.replace("[PATH]", SoundPath))