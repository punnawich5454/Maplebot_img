from time import *
from main import *
from click import *
from mylib import click
def dungeon():
    bot_menu()
    Mu_Lung_Dojo()
    Pyramid()
    Elite_dun()
    slide()
    Daily_dun()
    cooking()
    mail_box()
    daily_Quest()



if __name__ == "__main__":
    import keyboard
    running = True

    def stop_listener():
        global running
        keyboard.wait('-')  # กด - เพื่อหยุด
        running = False
        print("🛑 สั่งหยุดบอทแล้ว")

    threading.Thread(target=stop_listener, daemon=True).start()
    
    checker = lambda: running  # ← นี่คือ checker
    sleep(3)
    guild_dun(checker)
   
    
    
   
    # import pyautogui
    # import pygetwindow as gw
    # import time
    # import pydirectinput

    # # 1. ระบุชื่อหน้าต่างเกม (ต้องใส่ให้ถูก หรือใส่แค่บางส่วนก็ได้)
    # game_title = "MapleStory" 

    # try:
    #     # ค้นหาหน้าต่างเกมทั้งหมดที่มีชื่อนี้
    #     windows = gw.getWindowsWithTitle(game_title)
        
    #     if not windows:
    #         print(f"หาหน้าต่างเกม '{game_title}' ไม่เจอ! เปิดเกมหรือยัง?")
    #         exit()
            
    #     # เลือกหน้าต่างแรกที่เจอ
    #     game_window = windows[0]
        
    #     # ดึงพิกัดของหน้าต่างเกมมา (ซ้าย, บน, ความกว้าง, ความสูง)
    #     # นี่คือ "กรอบ" ที่เราจะอนุญาตให้บอททำงาน
    #     game_region = (game_window.left, game_window.top, game_window.width, game_window.height)
        
    #     print(f"เจอเกมแล้ว! พิกัดหน้าต่าง: {game_region}")
        
    #     # ทำให้หน้าต่างเกม Active (เด้งขึ้นมา) ก่อนทำงาน
    #     game_window.activate()
    #     time.sleep(1)

    #     # ---------------------------------------------------------
    #     # วิธีใช้ 1: หาภาพ "เฉพาะในกรอบเกม" (ใส่ parameter region=...)
    #     # ---------------------------------------------------------
    #     image_path = 'daily.png'
    #     location = pyautogui.locateOnScreen(image_path, confidence=0.8, region=game_region)
        
    #     if location:
    #         print("เจอเหรียญในเกม!")
    #         # คลิกตรงกลางภาพที่เจอ
    #         center = pyautogui.center(location)
    #         win32_cickMaple(center[0], center[1])
    #     else:
    #         print("ไม่เจอเหรียญในหน้าต่างเกม")

    # except Exception as e:
    #     print(f"เกิดข้อผิดพลาด: {e}")

    

        
        # main()
    
        # test()
        # Pyramid()
        # Mu_Lung_Dojo()
        # Daily_dun()
