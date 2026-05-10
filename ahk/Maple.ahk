#Requires AutoHotkey v2.0
CoordMode("Mouse", "Client")

^F1:: {
    WinActivate("MapleStoryM")
    WinWaitActive("MapleStoryM")
    Sleep(300)
    MouseMove 853, 289,100
    MouseClick "left"
    MouseClick "left"

    
}
