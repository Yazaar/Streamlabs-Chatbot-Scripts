let queue = []
let running = false

let soundAnnounce = new Howl({
    src: ['sounds\\' + settings.SoundAnnounce],
    volume: settings.SoundAnnounceVolume / 100
})

let soundWarning = new Howl({
    src: ['sounds\\' + settings.SoundWarning],
    volume: settings.SoundWarningVolume / 100
})

let soundKeyCode = new Howl({
    src: ['sounds\\' + settings.SoundKeyCode],
    volume: settings.SoundKeyCodeVolume / 100
})

function RunEngine(userType, name, message, actionType, time, alt = false) {
    if (userType === undefined || name === undefined || message === undefined) {
        return
    }
    running = true

    if (actionType.toLowerCase() === '-w') {
        document.documentElement.style.setProperty('--backgroundColor', settings.BackgroundColorWarning)
        document.querySelector('.bubble .txt .name span:nth-child(1)').style.color = settings.LightColorWarning
        document.querySelector('.message').style.color = settings.TextColorWarning
        soundWarning.play()
    } else if (actionType.toLowerCase() === '-a') {
        document.documentElement.style.setProperty('--backgroundColor', settings.BackgroundColorAnnounce)
        document.querySelector('.bubble .txt .name span:nth-child(1)').style.color = settings.LightColorAnnounce
        document.querySelector('.message').style.color = settings.TextColorAnnounce
        soundAnnounce.play()
    } else {
        document.documentElement.style.setProperty('--backgroundColor', settings.BackgroundColorKeyCode)
        document.querySelector('.bubble .txt .name span:nth-child(1)').style.color = actionType
        document.querySelector('.message').style.color = settings.TextColorKeyCode
        soundKeyCode.play()
    }

    document.querySelector('.name span:nth-child(1)').innerText = userType
    document.querySelector('.name span:nth-child(2)').innerText = ' ~ ' + name
    document.querySelector('.message').innerText = message
    document.querySelector('.timestamp').innerText = time
    
    if (alt !== false) {
        document.querySelector('.bubble').classList.add('alt')
        document.querySelector('.bubble').style.animation = 'revealRight 1s forwards'
    } else {
        document.querySelector('.bubble').classList.remove('alt')
        document.querySelector('.bubble').style.animation = 'revealLeft 1s forwards'
    }
    
    setTimeout(() => {
        if (document.querySelector('.bubble').classList.contains('alt')) {
            document.querySelector('.bubble').style.animation = 'hideRight 1s forwards'
        } else {
            document.querySelector('.bubble').style.animation = 'hideLeft 1s forwards'
        }

        setTimeout(() => {
            if(queue.length > 0) {
                let next = queue.splice(0, 1)[0]
                RunEngine(next.userType, next.username, next.message, next.type, next.time, settings.ReverseMessage)
            } else {
                running = false
            }
        }, 2000)

    }, 10000)
}

//---------------------------------
//  Variables
//---------------------------------
var socket = new WebSocket(API_Socket);
//---------------------------------
//  Open Event
//---------------------------------
socket.onopen = function () {
    // Format your Authentication Information
    var auth = {
        author: "AnkhHeart",
        website: "https://Streamlabs.com",
        api_key: API_Key,
        events: [
            "Warnings&AnnouncementsByYazaar",
            "Warnings&AnnouncementsByYazaarRELOAD"
        ]
    }

    //  Send your Data to the server
    socket.send(JSON.stringify(auth));
};
//---------------------------------
//  Error Event
//---------------------------------
socket.onerror = function (error) {
    //  Something went terribly wrong... Respond?!
    console.log("Error: " + error);
}
//---------------------------------
//  Message Event
//---------------------------------
socket.onmessage = function (message) {
    if (JSON.parse(message.data).event !== "Warnings&AnnouncementsByYazaar") {
        return
    }
    let data = JSON.parse(JSON.parse(message.data).data)


    let MyUsername = data.username
    let MyMessage = data.message
    let MyMute = data.mute
    let MyType = data.type
    let MyUserType = data.userType
    let MyTime = new Date().toLocaleTimeString().split(':', 2).join(':')

    if (MyType === 'KeyCode') {
        MyType = data.color
    }

    if (running === true) {
        queue.push({
            message: MyMessage,
            mute: MyMute,
            type: MyType,
            userType: MyUserType,
            username: MyUsername,
            time: MyTime
        })
    } else {
        RunEngine(MyUserType, MyUsername, MyMessage, MyType, MyTime, settings.ReverseMessage)
    }

}
//---------------------------------
//  Close Event
//---------------------------------
socket.onclose = function () {
    // Connection has been closed by you or the server
    console.log("Connection Closed!");
}