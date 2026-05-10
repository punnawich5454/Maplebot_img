from Windowscapture import *
from matchTemplate import *
from time import *
from click import *
import threading
from datetime import datetime
import random
import json
import os


# --- Config ---

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "bot_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


CFG = load_config()


# --- Exceptions ---

class StopException(Exception):
    """Custom Exception สำหรับหยุดการทำงานของ Thread"""
    pass


# --- Utilities ---

def smart_sleep(seconds, checker=None):
    """
    ฟังก์ชัน Sleep แบบฉลาด (Smart Sleep)
    - ทำหน้าที่เหมือน sleep ปกติ แต่จะตรวจสอบสถานะ checker() ทุกๆ 0.1 วินาที
    - ถ้า checker() คืนค่า False (สั่งหยุด) จะโยน Error (StopException) เพื่อหยุดฟังก์ชันทันที
    """
    end_time = time() + seconds
    while time() < end_time:
        if checker is not None and not checker():
            raise StopException("ได้รับคำสั่งหยุดการทำงาน (Stop signal received)")
        sleep(max(0, min(0.1, end_time - time())))


def click_cfg(c, key):
    """คลิกตามพิกัดจาก config — ใช้ได้ทุกฟังก์ชัน"""
    win32_cickMaple(x=c[key][0], y=c[key][1])


# --- Menu ---

def bot_menu(checker=None):
    c = CFG["bot_menu"]
    delay_click = random.randint(2, 3)

    print(f"Click to Menu") 
    smart_sleep(delay_click, checker)
    click_cfg(c, "menu_button")
    smart_sleep(delay_click, checker)
    click_cfg(c, "menu_option")

    return


# --- Dungeon Functions ---

def Mu_Lung_Dojo(checker=None):
    if checker and not checker():  
        print("Skip Mu_Lung_Dojo")
        return 
    bot_menu(checker)
    c = CFG["Mu_Lung_Dojo"]
    day = datetime.today().strftime('%A')
    delay_click = random.randint(2,3)
    match day:
        case 'Monday':
            if checker and not checker():  
                print("Skip Mu_Lung_Dojo")
                return 
            start_time = time()
            print(f"Mu_Lung_Dojo")
            print(f"{day}")
            smart_sleep(delay_click, checker)
            # hwid = win32gui.FindWindow("UnityWndClass", "MapleStoryM")
            # check = drag_and_drop(hwid, start_pos=tuple(c["drag_start"]), end_pos=tuple(c["drag_end"]))
            # if not check:
            #     print("drag and drop failed")
            #     return
            # smart_sleep(delay_click, checker)
            
            click_cfg(c, "dojo_select")
            smart_sleep(delay_click, checker)
            click_cfg(c, "confirm")
            smart_sleep(delay_click, checker)
            click_cfg(c, "start")
            print(delay_click)
            smart_sleep(delay_click, checker)

            print("bot coldown 4 min")
            while time() - start_time < c["cooldown_monday"]:
                smart_sleep(1, checker)
            click_cfg(c, "exit")
            smart_sleep(delay_click, checker)
            smart_sleep(5, checker)
        case _:
            if checker and not checker():  
                print("Skip Mu_Lung_Dojo")
                return 
            print(f"Mu_Lung_Dojo")
            smart_sleep(delay_click, checker)
            click_cfg(c, "dojo_select")
            smart_sleep(delay_click, checker)
            click_cfg(c, "confirm")
            smart_sleep(delay_click, checker)
            click_cfg(c, "start")
            print(delay_click)

            print("bot cooldown 1.2 min")
            smart_sleep(c["cooldown_default"], checker)
            click_cfg(c, "exit")
            smart_sleep(delay_click, checker)
            smart_sleep(5, checker)

    return


def Mu_Lung_Dojo_time():
    pass


def slide(checker=None):
    c = CFG["slide"]
    delay_click = random.randint(2, 3)
    bot_menu(checker)
    # hwid = win32gui.FindWindow("UnityWndClass", "MapleStoryM")
    print("drag and drop to dungeon 3")
    smart_sleep(delay_click, checker)
    # check = drag_and_drop(hwid, start_pos=tuple(c["drag_start"]), end_pos=tuple(c["drag_end"]))
    # if not check:
    #     print("drag and drop failed")
    #     return
    # smart_sleep(delay_click, checker)
    click_cfg(c, "select")
    smart_sleep(delay_click, checker)
    click_cfg(c, "confirm")
    smart_sleep(delay_click, checker)
    click_cfg(c, "start")

    print("bot coldown 4.5 min")
    smart_sleep(c["cooldown"], checker)
    click_cfg(c, "exit")
    smart_sleep(5, checker)

    return


def Elite_dun(checker=None):
    c = CFG["Elite_dun"]
    delay_click = random.randint(2, 3)

    print(f"Elite_dun")
    bot_menu(checker)
    smart_sleep(delay_click, checker)
    click_cfg(c, "select")
    smart_sleep(delay_click, checker)
    click_cfg(c, "confirm")
    smart_sleep(delay_click, checker)
    click_cfg(c, "difficulty")
    smart_sleep(1, checker)
    click_cfg(c, "start")

    print("bot coldown 3 min")
    smart_sleep(c["cooldown"], checker)
    click_cfg(c, "exit")
    smart_sleep(delay_click, checker)
    smart_sleep(5, checker)
    return


def cooking(checker=None):
    c = CFG["cooking"]
    delay_click = random.randint(2, 3)
    print("Cooking_dun")
    bot_menu(checker)
    smart_sleep(delay_click, checker)
    click_cfg(c, "select")
    smart_sleep(delay_click, checker)
    click_cfg(c, "confirm")
    smart_sleep(delay_click, checker)
    click_cfg(c, "start")
    print("cooldown 2 min")
    smart_sleep(c["cooldown"], checker)
    click_cfg(c, "collect1")
    smart_sleep(delay_click, checker)
    click_cfg(c, "collect2")
    smart_sleep(delay_click, checker)
    click_cfg(c, "collect3")
    smart_sleep(delay_click, checker)
    click_cfg(c, "close")
    smart_sleep(delay_click, checker)


def Daily_dun(checker=None):
    c = CFG["Daily_dun"]
    delay_click = random.randint(2, 3)

    print(f"Daily_dun")
    bot_menu(checker)
    smart_sleep(5, checker)
    day = datetime.today().strftime('%A')
    match day:
        case 'Saturday' | 'Sunday':
            print("Saturday")
            smart_sleep(delay_click, checker)
            click_cfg(c, "select")
            smart_sleep(delay_click, checker)
            click_cfg(c, "tab_weekend")
            smart_sleep(delay_click, checker)
            click_cfg(c, "confirm")
            smart_sleep(delay_click, checker)
            click_cfg(c, "start")
            smart_sleep(2, checker)
            click_cfg(c, "start2")

            print("bot coldown 25 min")
            smart_sleep(c["cooldown_weekend"], checker)
            click_cfg(c, "exit")
            click_cfg(c, "oneclick")
        
        case _:
            print("evey day")
            smart_sleep(delay_click, checker)

            print(day)
            click_cfg(c, "select")
            smart_sleep(delay_click, checker)
            click_cfg(c, "confirm")
            smart_sleep(delay_click, checker)
            click_cfg(c, "start")
            smart_sleep(2, checker)
            click_cfg(c, "start2")
            print("bot coldown 25 min")
            smart_sleep(c["cooldown_default"], checker)
            click_cfg(c, "exit")
            click_cfg(c, "oneclick")

    return


# --- Guild dun ---

def guild_dun(checker=None):
    c = CFG["guild_dun"]
    delay_click = random.randint(2, 3)
    print("guild_dun")
   
    smart_sleep(delay_click, checker)
    click_cfg(c, "click_menu")

    smart_sleep(delay_click, checker)
    click_cfg(c, "select_guild")

    smart_sleep(delay_click, checker)
    click_cfg(c, "claim")

    smart_sleep(delay_click, checker)
    click_cfg(c, "claim_box")

    smart_sleep(delay_click, checker)
    click_cfg(c, "claim1")
    smart_sleep(delay_click, checker)
    click_cfg(c, "exit")

    smart_sleep(delay_click, checker)
    click_cfg(c, "honor")

    smart_sleep(delay_click, checker)
    click_cfg(c, "confirm")
    smart_sleep(5, checker)

    smart_sleep(delay_click, checker)
    click_cfg(c, "start")
    smart_sleep(c["cooldown"], checker)
    smart_sleep(10, checker)

# --- Quest & Mail ---

def daily_Quest(checker=None):
    c = CFG["daily_Quest"]
    print("daily_Quest")

    smart_sleep(5, checker)
    click_cfg(c, "open_menu")
    smart_sleep(2, checker)
    click_cfg(c, "quest_tab")
    smart_sleep(2, checker)
    click_cfg(c, "claim1")
    smart_sleep(2, checker)
    click_cfg(c, "ok1")
    smart_sleep(2, checker)
    click_cfg(c, "claim2")
    smart_sleep(2, checker)
    click_cfg(c, "ok2")
    smart_sleep(2, checker)
    click_cfg(c, "tab2")
    smart_sleep(2, checker)
    click_cfg(c, "claim3")
    smart_sleep(2, checker)
    click_cfg(c, "ok3")
    smart_sleep(2, checker)
    click_cfg(c, "claim4")
    smart_sleep(2, checker)
    click_cfg(c, "ok4")
    smart_sleep(2, checker)
    click_cfg(c, "close1")
    smart_sleep(2, checker)
    click_cfg(c, "close2")
    smart_sleep(5, checker)


def mail_box(checker=None):
    c = CFG["mail_box"]
    print("mail_box")
   
    smart_sleep(5, checker)
    click_cfg(c, "open")
    smart_sleep(2, checker)
    click_cfg(c, "claim_all")
    smart_sleep(2, checker)
    click_cfg(c, "ok1")
    smart_sleep(2, checker)
    click_cfg(c, "tab2")
    smart_sleep(2, checker)
    click_cfg(c, "claim_all2")
    smart_sleep(2, checker)
    click_cfg(c, "ok2")
    smart_sleep(2, checker)
    click_cfg(c, "close")


# --- Main Bot ---

def main(checker):
    print("Main bot started")
    try:
        if checker and not checker(): raise StopException()
        Mu_Lung_Dojo(checker)

        # if checker and not checker(): raise StopException()
        # cooking(checker)

        if checker and not checker(): raise StopException()
        Elite_dun(checker)

        if checker and not checker(): raise StopException()
        slide(checker)

        if checker and not checker(): raise StopException()
        Daily_dun(checker)

        if checker and not checker(): raise StopException()
        guild_dun(checker)

        if checker and not checker(): raise StopException()
        daily_Quest(checker)

        # if checker and not checker(): raise StopException()
        # mail_box(checker)

    except StopException:
        print("Bot stopped successfully (Main thread caught StopException)")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Test ---

def test():
    print("test")
    sleep(5)
    win32_cickMaple(x=357, y=313)
    sleep(2)
    win32_cickMaple(x=1125, y=673)
    sleep(2)
    win32_cickMaple(x=780, y=639)
    print("bot coldown 25 min")
    sleep(2)
    win32_cickMaple(x=449, y=585)


# --- Entry Point ---

if __name__ == "__main__":
    # main()
    # test()
    pass
