from pathlib import Path

APP_TITLE = "Click Sequence Manager"
USER_CONFIG_FILE = Path("saved_sequence.json")

# ตั้งค่าพื้นฐาน
DEFAULT_TARGET_WINDOW_TITLE = "MapleStory"
CLICK_DELAY_SECONDS = 0.5
LOOP_DELAY_SECONDS = 5.0
PRESS_HOLD_SECONDS = 0.05
START_DELAY_SECONDS = 3.0

# ข้อมูลชุดคำสั่งเริ่มต้น (ดึงมาจาก JSON ของคุณ)
DEFAULT_SEQUENCE = [
    {
        "name": "bot_menu",
        "after_delay": 1.0,
        "points": [
            {"x": 1234, "y": 40, "delay_min": 0.5, "delay_max": 1.0},   # menu_button
            {"x": 1082, "y": 310, "delay_min": 0.5, "delay_max": 1.0}   # menu_option
        ]
    },
    {
        "name": "Mu_Lung_Dojo",
        "after_delay": 110.0, # ดึงมาจาก cooldown_default
        "points": [
            {"x": 1234, "y": 40, "delay_min": 0.5, "delay_max": 1.0},   # menu_button
            {"x": 1082, "y": 310, "delay_min": 0.5, "delay_max": 1.0},   # menu_option
            {"x": 645, "y": 433, "delay_min": 0.5, "delay_max": 1.0},   # drag_start
            {"x": 49, "y": 433, "delay_min": 0.5, "delay_max": 1.0},    # drag_end
            {"x": 262, "y": 263, "delay_min": 0.5, "delay_max": 1.0},   # dojo_select
            {"x": 1075, "y": 660, "delay_min": 0.5, "delay_max": 1.0},  # confirm
            {"x": 790, "y": 640, "delay_min": 0.5, "delay_max": 1.0},   # start
            {"x": 386, "y": 644, "delay_min": 0.5, "delay_max": 1.0}    # exit
        ]
    },
    {
        "name": "slide",
        "after_delay": 255.0, # ดึงมาจาก cooldown
        "points": [
            {"x": 1234, "y": 40, "delay_min": 0.5, "delay_max": 1.0},   # menu_button
            {"x": 1082, "y": 310, "delay_min": 0.5, "delay_max": 1.0},   # menu_option
            {"x": 645, "y": 433, "delay_min": 0.5, "delay_max": 1.0},   # drag_start
            {"x": 49, "y": 433, "delay_min": 0.5, "delay_max": 1.0},    # drag_end
            {"x": 352, "y": 596, "delay_min": 0.5, "delay_max": 1.0},   # select
            {"x": 1142, "y": 662, "delay_min": 0.5, "delay_max": 1.0},  # confirm
            {"x": 788, "y": 563, "delay_min": 0.5, "delay_max": 1.0},   # start
            {"x": 441, "y": 593, "delay_min": 0.5, "delay_max": 1.0}    # exit
        ]
    },
    {
        "name": "Elite_dun",
        "after_delay": 190.0, # ดึงมาจาก cooldown
        "points": [
            {"x": 1234, "y": 40, "delay_min": 0.5, "delay_max": 1.0},   # menu_button
            {"x": 1082, "y": 310, "delay_min": 0.5, "delay_max": 1.0},   # menu_option
            {"x": 96, "y": 493, "delay_min": 0.5, "delay_max": 1.0},    # select
            {"x": 1139, "y": 664, "delay_min": 0.5, "delay_max": 1.0},  # confirm
            {"x": 851, "y": 446, "delay_min": 0.5, "delay_max": 1.0},   # difficulty
            {"x": 779, "y": 529, "delay_min": 0.5, "delay_max": 1.0},   # start
            {"x": 433, "y": 606, "delay_min": 0.5, "delay_max": 1.0}    # exit
        ]
    },
    {
        "name": "cooking",
        "after_delay": 80.0, # ดึงมาจาก cooldown
        "points": [
            {"x": 1022, "y": 599, "delay_min": 0.5, "delay_max": 1.0},  # select
            {"x": 1122, "y": 672, "delay_min": 0.5, "delay_max": 1.0},  # confirm
            {"x": 776, "y": 651, "delay_min": 0.5, "delay_max": 1.0},   # start
            {"x": 652, "y": 546, "delay_min": 0.5, "delay_max": 1.0},   # collect1
            {"x": 640, "y": 651, "delay_min": 0.5, "delay_max": 1.0},   # collect2
            {"x": 857, "y": 669, "delay_min": 0.5, "delay_max": 1.0},   # collect3
            {"x": 1244, "y": 41, "delay_min": 0.5, "delay_max": 1.0}    # close
        ]
    },
    {
        "name": "Daily_dun",
        "after_delay": 40.0, # ดึงมาจาก cooldown_default
        "points": [
            {"x": 1234, "y": 40, "delay_min": 0.5, "delay_max": 1.0},   # menu_button
            {"x": 1082, "y": 310, "delay_min": 0.5, "delay_max": 1.0},   # menu_option
            {"x": 571, "y": 321, "delay_min": 0.5, "delay_max": 1.0},   # select
            {"x": 395, "y": 156, "delay_min": 0.5, "delay_max": 1.0},   # tab_weekend
            {"x": 1125, "y": 673, "delay_min": 0.5, "delay_max": 1.0},  # confirm
            {"x": 780, "y": 639, "delay_min": 0.5, "delay_max": 1.0},   # start
            {"x": 781, "y": 539, "delay_min": 0.5, "delay_max": 1.0},   # start2
            {"x": 449, "y": 585, "delay_min": 0.5, "delay_max": 1.0},   # exit
            {"x": 436, "y": 581, "delay_min": 0.5, "delay_max": 1.0}    # oneclick
        ]
    },
    {
        "name": "guild_dun",
        "after_delay": 75.0, # ดึงมาจาก cooldown
        "points": [
            {"x": 1234, "y": 45, "delay_min": 0.5, "delay_max": 1.0},   # click_menu
            {"x": 1200, "y": 480, "delay_min": 0.5, "delay_max": 1.0},  # select_guild
            {"x": 1172, "y": 130, "delay_min": 0.5, "delay_max": 1.0},  # claim
            {"x": 1105, "y": 354, "delay_min": 0.5, "delay_max": 1.0},  # claim_box
            {"x": 1182, "y": 690, "delay_min": 0.5, "delay_max": 1.0},  # claim1
            {"x": 38, "y": 43, "delay_min": 0.5, "delay_max": 1.0},     # exit
            {"x": 1109, "y": 448, "delay_min": 0.5, "delay_max": 1.0},  # honor
            {"x": 787, "y": 646, "delay_min": 0.5, "delay_max": 1.0},   # confirm
            {"x": 500, "y": 667, "delay_min": 0.5, "delay_max": 1.0}    # start
        ]
    },
    {
        "name": "daily_Quest",
        "after_delay": 2.0,
        "points": [
            {"x": 1234, "y": 40, "delay_min": 0.5, "delay_max": 1.0},   # menu_button
            {"x": 1082, "y": 310, "delay_min": 0.5, "delay_max": 1.0},   # menu_option
            {"x": 1236, "y": 34, "delay_min": 0.5, "delay_max": 1.0},   # open_menu
            {"x": 858, "y": 291, "delay_min": 0.5, "delay_max": 1.0},   # quest_tab
            {"x": 1172, "y": 673, "delay_min": 0.5, "delay_max": 1.0},  # claim1
            {"x": 637, "y": 515, "delay_min": 0.5, "delay_max": 1.0},   # ok1
            {"x": 1172, "y": 673, "delay_min": 0.5, "delay_max": 1.0},  # claim2
            {"x": 637, "y": 515, "delay_min": 0.5, "delay_max": 1.0},   # ok2
            {"x": 105, "y": 221, "delay_min": 0.5, "delay_max": 1.0},   # tab2
            {"x": 1181, "y": 671, "delay_min": 0.5, "delay_max": 1.0},  # claim3
            {"x": 637, "y": 515, "delay_min": 0.5, "delay_max": 1.0},   # ok3
            {"x": 1181, "y": 671, "delay_min": 0.5, "delay_max": 1.0},  # claim4
            {"x": 637, "y": 515, "delay_min": 0.5, "delay_max": 1.0},   # ok4
            {"x": 1246, "y": 48, "delay_min": 0.5, "delay_max": 1.0},   # close1
            {"x": 1235, "y": 37, "delay_min": 0.5, "delay_max": 1.0}    # close2
        ]
    },
    {
        "name": "mail_box",
        "after_delay": 2.0,
        "points": [
            {"x": 987, "y": 44, "delay_min": 0.5, "delay_max": 1.0},    # open
            {"x": 972, "y": 648, "delay_min": 0.5, "delay_max": 1.0},   # claim_all
            {"x": 641, "y": 532, "delay_min": 0.5, "delay_max": 1.0},   # ok1
            {"x": 646, "y": 158, "delay_min": 0.5, "delay_max": 1.0},   # tab2
            {"x": 972, "y": 648, "delay_min": 0.5, "delay_max": 1.0},   # claim_all2
            {"x": 641, "y": 532, "delay_min": 0.5, "delay_max": 1.0},   # ok2
            {"x": 1036, "y": 74, "delay_min": 0.5, "delay_max": 1.0}    # close
        ]
    }
]