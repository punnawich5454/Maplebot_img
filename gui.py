from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget,
                                QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
                                QScrollArea, QFrame, QCheckBox
                                )
from PySide6.QtCore import Qt
from main import *
import threading


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.threads = {}  # เก็บ thread ทั้งหมดด้วย dict
        self.running = True

        self.setWindowTitle("Bot_Maples Controller")
        self.setMinimumWidth(380)

        # menubar
        menubar = self.menuBar()
        exit_menu = menubar.addMenu("File")
        exit_action = exit_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # --- Central Widget with Scroll ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(6)
        scroll.setWidget(container)
        self.setCentralWidget(scroll)

        # --- Title ---
        title = QLabel("🍁 Bot Maples Controller")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 8px;")
        layout.addWidget(title)

        # ==========================================
        # 1. Run All & Stop Section
        # ==========================================
        layout.addWidget(self._separator("▶ Run All & Stop"))
        
        row_top = QHBoxLayout()
        # Run All (main) Button
        btn_run_all = QPushButton("🚀 Run All")
        btn_run_all.setToolTip("รันฟังก์ชันทั้งหมดตั้งแต่ต้นจนจบ")
        btn_run_all.setCursor(Qt.PointingHandCursor)
        btn_run_all.setStyleSheet(
            "background-color: #388e3c; color: white; font-weight: bold; "
            "font-size: 14px; padding: 8px; border-radius: 4px;"
        )
        btn_run_all.clicked.connect(lambda checked, k="main", f=main: self._run_in_thread(k, f))
        row_top.addWidget(btn_run_all)

        # Stop Button
        btn_stop = QPushButton("🛑 STOP")
        btn_stop.setToolTip("หยุดการทำงานของบอททั้งหมดทันที")
        btn_stop.setCursor(Qt.PointingHandCursor)
        btn_stop.setStyleSheet(
            "background-color: #d32f2f; color: white; font-weight: bold; "
            "font-size: 14px; padding: 8px; border-radius: 4px;"
        )
        btn_stop.clicked.connect(self.stop_function)
        row_top.addWidget(btn_stop)
        
        layout.addLayout(row_top)

        sub_functions = [
            ("🏯 Mu Lung Dojo",   "mu_lung_dojo", Mu_Lung_Dojo,),
            ("⚔️ Elite Dungeon",   "elite_dun",    Elite_dun, ),
            ("🎢 Slide Dungeon",  "slide",        slide,        ),
            ("🍳 Cooking",        "cooking",      cooking,      ),
            ("📅 Daily Dungeon",  "daily_dun",    Daily_dun,    ),
            ("🏰 Guild Dungeon",  "guild_dun",    guild_dun,   ),
            ("📜 Daily Quest",    "daily_quest",  daily_Quest,  ),
            ("📮 Mail Box",       "mail_box",     mail_box,     ),
        ]

        # ==========================================
        # 2. Individual Sub Functions (ปุ่มกดแยกทีละอัน)
        # ==========================================
        layout.addWidget(self._separator("📋 รันทีละดันเจี้ยน (Individual Run)"))

        for label_text, key, func in sub_functions:
            self._add_button_row(layout, label_text, key, func)

        # ==========================================
        # 3. Custom Run Checkboxes (เลือกดันเจี้ยนเอง)
        # ==========================================
        layout.addWidget(self._separator("☑️ รันแบบกำหนดคิวเอง (Run Selected)"))

        # Select All / Deselect All Buttons
        select_btns_layout = QHBoxLayout()
        btn_select_all = QPushButton("☑️ เลือกทั้งหมด")
        btn_select_all.setCursor(Qt.PointingHandCursor)
        btn_select_all.clicked.connect(self._select_all_checkboxes)
        btn_deselect_all = QPushButton("🔲 ยกเลิกทั้งหมด")
        btn_deselect_all.setCursor(Qt.PointingHandCursor)
        btn_deselect_all.clicked.connect(self._deselect_all_checkboxes)
        select_btns_layout.addWidget(btn_select_all)
        select_btns_layout.addWidget(btn_deselect_all)
        layout.addLayout(select_btns_layout)

        self.sub_function_checkboxes = []
        # Create a grid for checkboxes to look more compact
        grid_checkboxes = QGridLayout()
        row_idx, col_idx = 0, 0
        
        for label_text, key, func in sub_functions:
            cb = QCheckBox(label_text)
            cb.setStyleSheet("font-size: 13px; padding: 2px;")
            cb.setCursor(Qt.PointingHandCursor)
            grid_checkboxes.addWidget(cb, row_idx, col_idx)
            self.sub_function_checkboxes.append((cb, func))
            
            col_idx += 1
            if col_idx > 1:  # 2 columns
                col_idx = 0
                row_idx += 1
                
        layout.addLayout(grid_checkboxes)

        # Run Selected Button
        btn_run_selected = QPushButton("▶ เริ่มทำงานเฉพาะที่เลือก (Start Selected)")
        btn_run_selected.setCursor(Qt.PointingHandCursor)
        btn_run_selected.setStyleSheet(
            "background-color: #1976d2; color: white; font-weight: bold; "
            "font-size: 14px; padding: 8px; border-radius: 4px; margin-top: 5px;"
        )
        btn_run_selected.clicked.connect(self._run_selected)
        layout.addWidget(btn_run_selected)

        layout.addStretch()

    # --------------------------------------------------
    # Helper: สร้าง separator label
    # --------------------------------------------------
    def _separator(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #666; "
            "padding: 10px 0 2px 0; border-bottom: 1px solid #ccc; margin-top: 5px;"
        )
        return lbl

    # --------------------------------------------------
    # Helper: สร้างแถว [Label] [Button]
    # --------------------------------------------------
    def _add_button_row(self, parent_layout, label_text, thread_key, target_func, tooltip_text=""):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-size: 13px;")
        btn = QPushButton("▶ Run")
        if tooltip_text:
            btn.setToolTip(tooltip_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedWidth(60)
        btn.setStyleSheet(
            "background-color: #388e3c; color: white; font-weight: bold; "
            "padding: 2px; border-radius: 3px;"
        )
        btn.clicked.connect(lambda checked, k=thread_key, f=target_func: self._run_in_thread(k, f))
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(btn)
        parent_layout.addLayout(row)

    def _select_all_checkboxes(self):
        for cb, _ in self.sub_function_checkboxes:
            cb.setChecked(True)

    def _deselect_all_checkboxes(self):
        for cb, _ in self.sub_function_checkboxes:
            cb.setChecked(False)

    # --------------------------------------------------
    # Logic: นำฟังก์ชันที่ถูกเลือกมารันทีละอันใน Thread เดียว
    # --------------------------------------------------
    def _run_selected(self):
        existing = self.threads.get("selected")
        if existing is not None and existing.is_alive():
            print("⚠️ หน้าต่างกำลังถูกรันอยู่แล้ว (Task is already running)")
            return

        funcs_to_run = []
        for cb, func in self.sub_function_checkboxes:
            if cb.isChecked():
                funcs_to_run.append((cb.text(), func))

        if not funcs_to_run:
            print("⚠️ ไม่ได้เลือกฟังก์ชันใดเลย (No functions selected)")
            return

        self.running = True
        checker = lambda: self.running

        def task_runner():
            print("🚀 เริ่มรันฟังก์ชันที่เลือก...")
            for idx, (name, func) in enumerate(funcs_to_run):
                if not checker():
                    print("🔴 หยุดการทำงานก่อนเริ่มฟังก์ชันถัดไป")
                    break
                try:
                    print(f"🟢 [ {idx+1}/{len(funcs_to_run)} ] Starting: {name}")
                    func(checker)
                except Exception as e:
                    if type(e).__name__ == "StopException":
                        print("🔴 รับคำสั่งหยุดการทำงาน (Stop exception caught)")
                        break
                    else:
                        print(f"⚠️ พบข้อผิดพลาดใน {name}: {e}")
            print("✅ รันคำสั่งที่เลือกทั้งหมดเสร็จสิ้น หรือถูกสั่งหยุด")

        t = threading.Thread(target=task_runner, daemon=True)
        self.threads["selected"] = t
        t.start()

    # --------------------------------------------------
    # Generic: รันฟังก์ชันใน thread ใหม่
    # --------------------------------------------------
    def _run_in_thread(self, key, func):
        # ตรวจว่ามี thread เก่าอยู่ไหม
        existing = self.threads.get(key)
        if existing is not None and existing.is_alive():
            print(f"⚠️ {key} กำลังทำงานอยู่แล้ว (already running)")
            return

        self.running = True
        checker = lambda: self.running
        print(f"🟢 Starting: {key}")
        t = threading.Thread(target=func, args=(checker,), daemon=True)
        self.threads[key] = t
        t.start()

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------
    def stop_function(self):
        self.running = False
        print("🔴 Stop signal sent")


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()