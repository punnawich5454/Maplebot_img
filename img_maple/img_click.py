"""
ฟังก์ชันสำเร็จรูปสำหรับ ตรวจจับรูปภาพแล้วคลิก
เรียกใช้ง่ายๆ: find_and_click("m1.png")
"""
import time
import os
from Windowscapture import WindowCapture
from matchTemplate import Classbot
from click import win32_cickMaple

# ชื่อหน้าต่างเกม (เปลี่ยนตรงนี้ที่เดียว ใช้ได้ทั้งไฟล์)
GAME_WINDOW = "MapleStoryM"

# โฟลเดอร์ที่เก็บรูปภาพ template
IMG_DIR = os.path.dirname(os.path.abspath(__file__))


def find_and_click(
    img_name: str,
    threshold=0.8,
    scan_time=5,
    click_all=False,
    click_delay=0.3,
) -> bool:
    """
    หารูปภาพบนหน้าจอเกม แล้วคลิก
    
    Args:
        img_name:    ชื่อไฟล์รูป เช่น "m1.png"
        threshold:   ความแม่นยำ 0.0-1.0 (ค่าเริ่มต้น 0.8 = 80%)
        scan_time:   สแกนกี่วินาที ถ้าไม่เจอก็หยุด (ค่าเริ่มต้น 5 วินาที)
        click_all:   True = คลิกทุกจุดที่เจอ, False = คลิกแค่จุดแรก
        click_delay: หน่วงเวลาระหว่างคลิกแต่ละครั้ง (วินาที)
    
    Returns:
        True ถ้าเจอและคลิกแล้ว, False ถ้าไม่เจอ
    """
    template_path = os.path.join(IMG_DIR, img_name)

    start = time.time()
    while time.time() - start < scan_time:
        screenshot_img = WindowCapture(GAME_WINDOW).screenshot()
        bot = Classbot(mainimg=screenshot_img, tempimg=template_path)
        point = bot.search(threshold=threshold)

        if point:
            if click_all:
                for p in point:
                    print(f"✅ [{img_name}] คลิกที่ X:{p[0]}, Y:{p[1]}")
                    win32_cickMaple(p[0], p[1])
                    time.sleep(click_delay)
            else:
                print(f"✅ [{img_name}] คลิกที่ X:{point[0][0]}, Y:{point[0][1]}")
                win32_cickMaple(point[0][0], point[0][1])
            return True

        time.sleep(0.5)

    print(f"❌ [{img_name}] ไม่เจอภาพภายใน {scan_time} วินาที")
    return False


def wait_for_img(
    img_name: str,
    threshold=0.8,
    timeout=30,
) -> bool:
    """
    รอจนกว่าจะเจอรูปภาพ (ไม่คลิก แค่เช็คว่าเจอหรือยัง)
    
    Args:
        img_name:   ชื่อไฟล์รูป เช่น "loading.png"
        threshold:  ความแม่นยำ
        timeout:    รอนานสุดกี่วินาที
    
    Returns:
        True ถ้าเจอ, False ถ้าหมดเวลา
    """
    template_path = os.path.join(IMG_DIR, img_name)

    start = time.time()
    while time.time() - start < timeout:
        screenshot_img = WindowCapture(GAME_WINDOW).screenshot()
        bot = Classbot(mainimg=screenshot_img, tempimg=template_path)
        point = bot.search(threshold=threshold)

        if point:
            for p in point:
                print(f"✅ [{img_name}] เจอภาพแล้ว!")
                win32_cickMaple(p[0], p[1])
                return True

        time.sleep(0.5)

    print(f"❌ [{img_name}] รอหมดเวลา {timeout} วินาที")
    return False
