def execute_steps(steps):
    """ฟังก์ชันช่วยรันชุดคำสั่งพิกัด เพื่อลดการเขียนลูปซ้ำๆ"""
    for delay, x, y in steps:
        sleep(delay)
        win32_cickMaple(x=x, y=y)

def test_dojo_dungeon():
    print("🚀 เริ่มลุยดันเจี้ยน Dojo")
    steps = [
        (3, 1239, 50),   # menu
        (3, 1080, 296),  # dojo menu
        (2, 262, 263),   # dojo_select
        (2, 1075, 660),  # confirm
        (2, 790, 640),   # start
    ]
    execute_steps(steps)
    
    sleep(3)
    wait_for_img("img_maple/exit.png",threshold=0.8,timeout=555)
    print(" จบดันเจี้ยน Dojo")

def test_dimension_dungeon():
    print("🚀 เริ่มลุยดันเจี้ยน dimension_dungeon")
    steps = [
        (3, 1234, 40),   # menu_button
        (3, 1082, 310),  # menu_option
        (2, 352, 596),   # select
        (2, 1142, 662),  # confirm
        (2, 788, 563),  # start
    ]
    execute_steps(steps)
    
    sleep(3)
    wait_for_img("img_maple/exit.png",threshold=0.8,timeout=555)
    print(" dimension_dungeon")
def elite_dungeon():
    print("🚀 เริ่มลุยดันเจี้ยน elite_dungeon")
    steps = [
        (3, 1234, 40),   # menu_button
        (3, 1082, 310),  # menu_option
        (2, 96, 493),    # select
        (2, 1139, 664),  # confirm
        (2, 851, 446),   # difficulty
        (2, 779, 529),   # start
    ]
    execute_steps(steps)
    sleep(3)
    wait_for_img("img_maple/exit.png",threshold=0.8,timeout=555)
    print(" elite_dungeon")

def guild_dun():
    print("🚀 เริ่มลุยดันเจี้ยน guild_dun")
    steps = [
        (3, 1234, 45),   # click_menu
        (3, 1200, 480),  # select_guild
        (2, 1172, 130),  # claim
        (2, 1105, 354),  # claim_box
        (2, 1182, 690),  # claim1
        (2, 38, 43),     # exit
        (2, 1109, 448),  # honor
        (2, 787, 646),   # confirm
        (3, 500, 667),   # start
        (2, 500, 667),   # start
    ]
    execute_steps(steps)
    sleep(90.0)
    # wait_for_img("img_maple/exit.png", threshold=0.8, timeout=555)
    print(" จบดันเจี้ยน guild_dun")

def daily_Quest():
    print("🚀 เริ่มทำ daily_Quest")
    steps = [
        (3, 1234, 40),   # menu_button
     
        (2, 858, 291),   # quest_tab
        (2, 1172, 673),  # claim1
        (2, 637, 515),   # ok1
        (2, 1172, 673),  # claim2
        (2, 637, 515),   # ok2
        (2, 105, 221),   # tab2
        (2, 1181, 671),  # claim3
        (2, 637, 515),   # ok3
        (2, 1181, 671),  # claim4
        (2, 637, 515),   # ok4
        (2, 1246, 48),   # close1
        (2, 1235, 37),   # close2
    ]
    execute_steps(steps)
    sleep(2.0)
    print(" จบ daily_Quest")

def mail_box():
    print("🚀 เริ่มเปิด mail_box")
    steps = [
        (3, 987, 44),    # open
        (3, 972, 648),   # claim_all
        (2, 641, 532),   # ok1
        (2, 646, 158),   # tab2
        (2, 972, 648),   # claim_all2
        (2, 641, 532),   # ok2
        (2, 1036, 74),   # close
    ]
    execute_steps(steps)
    sleep(2.0)
    print(" จบ mail_box")

def main():
    print("🚀 เริ่มรันบอทแบบ Auto (Main)")
    # sleep(3)
    # test_dojo_dungeon()
    sleep(2)
    test_dimension_dungeon()
    sleep(2)
    elite_dungeon()
    sleep(2)
    guild_dun()
    sleep(2)
    daily_Quest()
    sleep(2)
    mail_box()
    print("✅ ทำงานครบทุกดันเจี้ยน/เควสแล้ว")

if __name__ == "__main__":
    main()