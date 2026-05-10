
def c_cickRo(x,y):
    from ctypes import windll, POINTER, c_long,c_wchar_p
    import win32api
    from time import sleep
    # ระบุ path ของไลบรารี AutoItX3_x64.dll หรือ AutoItX3.dll
    path = r".\AutoItX3_x64.dll"
    # โหลดไลบรารี AutoItX3_x64.dll หรือ AutoItX3.dll
    autoit = windll.LoadLibrary(path)
    # ดึงค่า x และ y ของตำแหน่งปัจจุบันของเมาส์
    # พิมพ์ค่า x และ y ที่ได้
    print(f"Current Mouse Position: ({x}, {y})")
    autoit.AU3_MouseClick(None, int(x), int(y), 1, 1, 0)
    #autoit.AU3_Send("{ENTER}", 0)
    #autoit.AU3_Send("{F1}", 0)





#################################
import win32api
import win32con
import win32gui
from time import sleep
# from keyboardData import VK_CODE

def send_keys(key,hold_duration=0.1):
    hwnd = win32gui.FindWindow('Ragnarok Landverse', 'Ragnarok Landverse')
    keycode = VK_CODE[key]
    #print(VK_CODE[key])
    #OX70 คือ F11 เอามาจาก 
    #http://www.kbdedit.com/manual/low_level_vk_list.html
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN,keycode, 0)
    sleep(hold_duration)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP,keycode, 0)

def control_click(x,y):
    hwnd = win32gui.FindWindow('UnityWndClass', 'MapleStoryM')
    l_param = win32api.MAKELONG(x,y)
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,l_param)
    sleep(0.1)
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,l_param)
    
    
def win32_cickRo(class_hwid,hwid,x, y):
    hwnd = win32gui.FindWindow(class_hwid, hwid)  # Change t
    # Get the window's client area position (top-left corner)
    rect = win32gui.GetWindowRect(hwnd)
    # Calculate the absolute screen coordinates of the point to click
    screen_x = rect[0] + x
    screen_y = rect[1] + y
    # Move the mouse to the specified coordinates
    win32api.SetCursorPos((screen_x, screen_y))
    # Adding a short delay can help ensure the click is registered
    sleep(0.1)
    # Perform a left mouse button click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
    
def win32_cickMaple(x, y,class_hwid='UnityWndClass',hwid='MapleStoryM'):
    hwnd = win32gui.FindWindow(class_hwid, hwid)  # Change t
    # Get the window's client area position (top-left corner)
    rect = win32gui.GetWindowRect(hwnd)
    # Calculate the absolute screen coordinates of the point to click
    screen_x = rect[0] + x
    screen_y = rect[1] + y
    # Move the mouse to the specified coordinates
    # x = int(x)
    # y = int(y)
    win32api.SetCursorPos((screen_x, screen_y))
    # Adding a short delay can help ensure the click is registered
    sleep(0.1)
    # Perform a left mouse button click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)

def send_input(hwid, msg):
    for c in msg:
        if c == "\n":
            win32api.SendMessage(hwid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            sleep(0.1)
            win32api.SendMessage(hwid, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            win32api.SendMessage(hwid, win32con.WM_CHAR, ord(c), 0)
             
def drag_and_drop(hwnd, start_pos, end_pos) -> bool:
    cout:int = 0
    while cout < 3:
        try:
            # ดึงตำแหน่งหน้าต่างจริงบนจอ
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            # start
            sx = left + start_pos[0]
            sy = top  + start_pos[1]
            # end
            ex = left + end_pos[0]
            ey = top  + end_pos[1]

            # ไปจุดเริ่ม
            win32api.SetCursorPos((sx, sy))
            sleep(0.05)

            # กดลง
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            sleep(0.05)

            # ลากแบบ smooth
            steps = 20
            for i in range(steps):
                nx = int(sx + (ex - sx) * i / steps)
                ny = int(sy + (ey - sy) * i / steps)
                win32api.SetCursorPos((nx, ny))
                sleep(0.01)

            # ปล่อยเมาส์
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            return True
        except Exception as e:
            cout += 1
            print(f"Error: {e}")
            
            sleep(5)
    return False