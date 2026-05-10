import copy
import json
import threading
from typing import List, Dict, Any, Optional, Tuple

import keyboard
import win32api
import win32gui
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from config import (
    APP_TITLE,
    CLICK_DELAY_SECONDS,
    DEFAULT_SEQUENCE,
    DEFAULT_TARGET_WINDOW_TITLE,
    USER_CONFIG_FILE,
)
from runner import run_sequence, find_target_window, capture_mouse_position


class ClickSequenceApp(QMainWindow):
    log_signal = Signal(str)
    run_finished_signal = Signal()
    
    hotkey_start_signal = Signal()
    hotkey_stop_signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1120, 720)

        self.sequence: List[Dict[str, Any]] = copy.deepcopy(DEFAULT_SEQUENCE)
        self.stop_requested: bool = False
        self.worker: Optional[threading.Thread] = None
        self.is_loading: bool = False

        self.selected_step_index: Optional[int] = None
        self.selected_point_index: Optional[int] = None
        self.countdown_value: int = 0

        self.log_signal.connect(self.append_log)
        self.run_finished_signal.connect(self.on_run_finished)
        self.hotkey_start_signal.connect(self.start_all)
        self.hotkey_stop_signal.connect(self.stop_run)

        self.build_ui()
        self.connect_auto_save()
        self.load_saved_data()
        self.refresh_step_list()
        
        self.update_hotkeys()
        self.set_ui_enabled(True)

    def connect_auto_save(self) -> None:
        self.target_window_input.editingFinished.connect(self.auto_save)
        self.step_name_input.editingFinished.connect(self.auto_save)
        self.after_delay_input.editingFinished.connect(self.auto_save)
        self.point_x_input.editingFinished.connect(self.auto_save)
        self.point_y_input.editingFinished.connect(self.auto_save)
        self.point_delay_min_input.editingFinished.connect(self.auto_save)
        self.point_delay_max_input.editingFinished.connect(self.auto_save)
        
        self.start_hotkey_combo.currentIndexChanged.connect(self.auto_save)
        self.stop_hotkey_combo.currentIndexChanged.connect(self.auto_save)

    def build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)
        self.setCentralWidget(root)

        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 14, 16, 14)
        top_layout.setSpacing(10)

        title = QLabel("Click Sequence Manager")
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title.setFont(title_font)
        top_layout.addWidget(title)

        top_layout.addStretch(1)

        top_layout.addWidget(QLabel("Target window"))
        self.target_window_input = QLineEdit(DEFAULT_TARGET_WINDOW_TITLE)
        self.target_window_input.setMinimumWidth(150)
        self.target_window_input.setMaximumWidth(200)
        top_layout.addWidget(self.target_window_input)

        hotkeys_options = [f"F{i}" for i in range(1, 13)]
        
        top_layout.addWidget(QLabel("Start Key:"))
        self.start_hotkey_combo = QComboBox()
        self.start_hotkey_combo.addItems(hotkeys_options)
        self.start_hotkey_combo.setCurrentText("F9")
        self.start_hotkey_combo.currentIndexChanged.connect(self.update_hotkeys)
        top_layout.addWidget(self.start_hotkey_combo)

        self.start_all_button = QPushButton("Start All")
        self.start_all_button.clicked.connect(self.start_all)
        top_layout.addWidget(self.start_all_button)

        top_layout.addWidget(QLabel("Stop Key:"))
        self.stop_hotkey_combo = QComboBox()
        self.stop_hotkey_combo.addItems(hotkeys_options)
        self.stop_hotkey_combo.setCurrentText("F10")
        self.stop_hotkey_combo.currentIndexChanged.connect(self.update_hotkeys)
        top_layout.addWidget(self.stop_hotkey_combo)

        self.run_step_button = QPushButton("Run Step")
        self.run_step_button.clicked.connect(self.run_selected_step)
        top_layout.addWidget(self.run_step_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_run)
        self.stop_button.setEnabled(False)
        top_layout.addWidget(self.stop_button)

        self.loop_checkbox = QCheckBox("Loop")
        top_layout.addWidget(self.loop_checkbox)

        root_layout.addWidget(top_bar)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        root_layout.addWidget(splitter, 1)

        left_panel = self.build_steps_panel()
        right_panel = self.build_editor_panel()
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([260, 820])

        self.status_label = QLabel("Ready.")
        self.status_label.setObjectName("statusLabel")
        root_layout.addWidget(self.status_label)

        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #101418;
                color: #edf2f7;
                font-size: 13px;
            }
            QListWidget#stepListCheckboxes::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #00aaff;
                border-radius: 4px;
                background-color: #0f1419;
            }
            QListWidget#stepListCheckboxes::indicator:hover {
                border: 2px solid #5ce6ff;
            }
            QListWidget#stepListCheckboxes::indicator:checked {
                background-color: #00aaff;
                border: 2px solid #00aaff;
            }
            QFrame#topBar, QGroupBox {
                background: #171d24;
                border: 1px solid #26303b;
                border-radius: 8px;
            }
            QGroupBox {
                font-weight: 600;
                margin-top: 10px;
                padding-top: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
            QLineEdit, QListWidget, QPlainTextEdit, QComboBox {
                background: #0f1419;
                border: 1px solid #2b3744;
                border-radius: 6px;
                padding: 6px;
                selection-background-color: #2a6df4;
            }
            QComboBox::drop-down {
                border-left: 1px solid #2b3744;
            }
            QPushButton {
                background: #1d2630;
                border: 1px solid #314152;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background: #273240;
            }
            QPushButton:pressed {
                background: #141b23;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: #2a6df4;
                color: white;
            }
            QLabel#statusLabel {
                color: #9fb0c3;
                padding-left: 4px;
            }
            """
        )

    def update_hotkeys(self) -> None:
        try:
            if hasattr(self, 'start_hotkey_hook') and self.start_hotkey_hook:
                try: keyboard.remove_hotkey(self.start_hotkey_hook)
                except Exception: pass
                
            if hasattr(self, 'stop_hotkey_hook') and self.stop_hotkey_hook:
                try: keyboard.remove_hotkey(self.stop_hotkey_hook)
                except Exception: pass
            
            start_key = self.start_hotkey_combo.currentText()
            stop_key = self.stop_hotkey_combo.currentText()
            
            self.start_hotkey_hook = keyboard.add_hotkey(start_key, lambda: self.hotkey_start_signal.emit())
            self.stop_hotkey_hook = keyboard.add_hotkey(stop_key, lambda: self.hotkey_stop_signal.emit())
            
            self.append_log(f"Hotkeys updated: Start={start_key}, Stop={stop_key}")
        except Exception as e:
            self.append_log(f"Error setting hotkeys: {e}")

    def build_steps_panel(self) -> QFrame:
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        box = QGroupBox("Quest / Click Sets")
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(10)

        self.step_list = QListWidget()
        self.step_list.setObjectName("stepListCheckboxes")
        self.step_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.step_list.setDragDropMode(QAbstractItemView.InternalMove)
        
        self.step_list.itemChanged.connect(self.on_step_item_changed)
        self.step_list.model().rowsMoved.connect(self.on_step_moved)
        self.step_list.currentRowChanged.connect(self.on_step_selected)
        box_layout.addWidget(self.step_list, 1)

        buttons = QHBoxLayout()
        self.add_step_btn = QPushButton("Add Step")
        self.add_step_btn.clicked.connect(self.add_step)
        
        self.duplicate_step_btn = QPushButton("Duplicate")
        self.duplicate_step_btn.clicked.connect(self.duplicate_step)
        
        self.delete_step_btn = QPushButton("Delete Step")
        self.delete_step_btn.clicked.connect(self.delete_step)
        
        buttons.addWidget(self.add_step_btn)
        buttons.addWidget(self.duplicate_step_btn)
        buttons.addWidget(self.delete_step_btn)
        box_layout.addLayout(buttons)

        layout.addWidget(box, 1)
        return panel

    def build_editor_panel(self) -> QFrame:
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        settings_box = QGroupBox("Step Settings")
        settings_layout = QFormLayout(settings_box)
        settings_layout.setHorizontalSpacing(16)
        settings_layout.setVerticalSpacing(12)

        self.after_delay_input = QLineEdit()
        self.step_name_input = QLineEdit()

        settings_layout.addRow("Step name", self.step_name_input)
        settings_layout.addRow("After delay", self.after_delay_input)

        points_box = QGroupBox("Click Points")
        points_layout = QVBoxLayout(points_box)
        points_layout.setSpacing(10)

        self.points_list = QListWidget()
        self.points_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.points_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.points_list.model().rowsMoved.connect(self.on_point_moved)
        self.points_list.currentRowChanged.connect(self.on_point_selected)
        points_layout.addWidget(self.points_list)

        point_form = QGridLayout()
        point_form.setHorizontalSpacing(12)
        point_form.setVerticalSpacing(10)
        
        # เพิ่มตัวแปร Label เพื่อให้สั่งซ่อน/แสดงได้
        self.label_x = QLabel("X")
        self.label_y = QLabel("Y")
        self.label_delay_min = QLabel("Delay min")
        self.label_delay_max = QLabel("Delay max")
        
        self.point_x_input = QLineEdit()
        self.point_y_input = QLineEdit()
        self.point_delay_min_input = QLineEdit()
        self.point_delay_max_input = QLineEdit()
        
        point_form.addWidget(self.label_x, 0, 0)
        point_form.addWidget(self.point_x_input, 0, 1)
        point_form.addWidget(self.label_y, 0, 2)
        point_form.addWidget(self.point_y_input, 0, 3)
        point_form.addWidget(self.label_delay_min, 1, 0)
        point_form.addWidget(self.point_delay_min_input, 1, 1)
        point_form.addWidget(self.label_delay_max, 1, 2)
        point_form.addWidget(self.point_delay_max_input, 1, 3)
        points_layout.addLayout(point_form)

        point_buttons = QHBoxLayout()
        self.add_point_btn = QPushButton("Add Point")
        self.add_point_btn.clicked.connect(self.add_point)
        
        self.add_delay_btn = QPushButton("Add Delay ⏳")
        self.add_delay_btn.setStyleSheet("background-color: #d97706; color: white; font-weight: bold;")
        self.add_delay_btn.clicked.connect(self.add_delay)
        
        self.capture_point_btn = QPushButton("Capture Point (3s) 🎯")
        self.capture_point_btn.setStyleSheet("background-color: #2b5797; color: white; font-weight: bold;")
        self.capture_point_btn.clicked.connect(self.start_capture_countdown)
        
        self.delete_point_btn = QPushButton("Delete Point")
        self.delete_point_btn.clicked.connect(self.delete_point)
        
        point_buttons.addWidget(self.add_point_btn)
        point_buttons.addWidget(self.add_delay_btn)
        point_buttons.addWidget(self.capture_point_btn)
        point_buttons.addWidget(self.delete_point_btn)
        point_buttons.addStretch(1)
        points_layout.addLayout(point_buttons)

        log_box = QGroupBox("Status")
        log_layout = QVBoxLayout(log_box)
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)

        layout.addWidget(settings_box)
        layout.addWidget(points_box, 1)
        layout.addWidget(log_box, 1)
        return panel

    def set_ui_enabled(self, enabled: bool) -> None:
        self.target_window_input.setEnabled(enabled)
        self.step_list.setEnabled(enabled)
        self.step_list.setDragEnabled(enabled)
        self.points_list.setEnabled(enabled)
        self.points_list.setDragEnabled(enabled)
        self.step_name_input.setEnabled(enabled)
        self.after_delay_input.setEnabled(enabled)
        
        self.point_x_input.setEnabled(enabled)
        self.point_y_input.setEnabled(enabled)
        self.point_delay_min_input.setEnabled(enabled)
        self.point_delay_max_input.setEnabled(enabled)
        
        self.start_hotkey_combo.setEnabled(enabled)
        self.stop_hotkey_combo.setEnabled(enabled)
        self.add_step_btn.setEnabled(enabled)
        self.duplicate_step_btn.setEnabled(enabled)
        self.delete_step_btn.setEnabled(enabled)
        self.add_point_btn.setEnabled(enabled)
        self.add_delay_btn.setEnabled(enabled)
        self.capture_point_btn.setEnabled(enabled)
        self.delete_point_btn.setEnabled(enabled)
        
        self.start_all_button.setEnabled(enabled)
        self.run_step_button.setEnabled(enabled)
        self.loop_checkbox.setEnabled(enabled)
        self.stop_button.setEnabled(not enabled)

    def on_run_finished(self) -> None:
        self.set_ui_enabled(True)
        self.append_log("Run ended. Ready.")

    def append_log(self, message: str) -> None:
        self.status_label.setText(message)
        self.log_output.appendPlainText(message)

    def show_error(self, message: str) -> None:
        QMessageBox.critical(self, APP_TITLE, message)

    def show_info(self, message: str) -> None:
        QMessageBox.information(self, APP_TITLE, message)

    def on_step_item_changed(self, item: QListWidgetItem) -> None:
        row = self.step_list.row(item)
        if row < 0 or row >= len(self.sequence):
            return
            
        step = self.sequence[row]
        is_checked = item.checkState() == Qt.Checked
        current_order = step.get("run_order", 0)
        
        if is_checked and current_order == 0:
            max_order = max([s.get("run_order", 0) for s in self.sequence] + [0])
            step["run_order"] = max_order + 1
        elif not is_checked and current_order > 0:
            for s in self.sequence:
                if s.get("run_order", 0) > current_order:
                    s["run_order"] -= 1
            step["run_order"] = 0
            
        self.update_step_list_texts()
        self.auto_save()

    def update_step_list_texts(self) -> None:
        self.step_list.blockSignals(True)
        for i, step in enumerate(self.sequence):
            item = self.step_list.item(i)
            if item:
                order = step.get("run_order", 0)
                prefix = f"[{order}]" if order > 0 else "[ ]"
                item.setText(f"{prefix} {step['name']}")
        self.step_list.blockSignals(False)

    def refresh_step_list(self) -> None:
        self.step_list.blockSignals(True)
        self.step_list.clear()
        for step in self.sequence:
            item = QListWidgetItem()
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            
            order = step.get("run_order", 0)
            item.setCheckState(Qt.Checked if order > 0 else Qt.Unchecked)
            prefix = f"[{order}]" if order > 0 else "[ ]"
            item.setText(f"{prefix} {step['name']}")
            
            self.step_list.addItem(item)
        self.step_list.blockSignals(False)

        if not self.sequence:
            self.selected_step_index = None
            self.refresh_points_list()
            return

        if self.selected_step_index is None or self.selected_step_index >= len(self.sequence):
            self.selected_step_index = 0

        self.step_list.setCurrentRow(self.selected_step_index)
        self.on_step_selected(self.selected_step_index)

    def refresh_points_list(self) -> None:
        self.points_list.blockSignals(True)
        self.points_list.clear()

        if self.selected_step_index is not None:
            step = self.sequence[self.selected_step_index]
            for index, point in enumerate(step["points"], start=1):
                if point.get("type") == "delay":
                    self.points_list.addItem(f'{index}. ⏳ [Wait] {point["delay_min"]}s')
                else:
                    self.points_list.addItem(
                        f'{index}. x={point["x"]}, y={point["y"]}, delay={point["delay_min"]}-{point["delay_max"]}'
                    )

        self.points_list.blockSignals(False)

        if self.selected_step_index is None:
            self.selected_point_index = None
            self.point_x_input.clear()
            self.point_y_input.clear()
            self.point_delay_min_input.clear()
            self.point_delay_max_input.clear()
            return

        step = self.sequence[self.selected_step_index]
        if not step["points"]:
            self.selected_point_index = None
            self.point_x_input.clear()
            self.point_y_input.clear()
            self.point_delay_min_input.clear()
            self.point_delay_max_input.clear()
            return

        if self.selected_point_index is None or self.selected_point_index >= len(step["points"]):
            self.selected_point_index = 0

        self.points_list.setCurrentRow(self.selected_point_index)
        self.on_point_selected(self.selected_point_index)

    def on_step_selected(self, row: int) -> None:
        if row < 0 or row >= len(self.sequence):
            self.selected_step_index = None
            return

        self.selected_step_index = row
        self.selected_point_index = None
        step = self.sequence[row]
        self.step_name_input.setText(step.get("name", ""))
        self.after_delay_input.setText(str(step.get("after_delay", 0)))
        self.refresh_points_list()

    def on_point_selected(self, row: int) -> None:
        if self.selected_step_index is None:
            return

        step = self.sequence[self.selected_step_index]
        if row < 0 or row >= len(step["points"]):
            self.selected_point_index = None
            return

        self.selected_point_index = row
        point = step["points"][row]
        
        is_delay = point.get("type") == "delay"
        
        if is_delay:
            # ซ่อนช่อง X, Y และ Max Delay ทิ้งไปเลย
            self.label_x.hide()
            self.point_x_input.hide()
            self.label_y.hide()
            self.point_y_input.hide()
            self.label_delay_max.hide()
            self.point_delay_max_input.hide()
            
            # โชว์แค่ช่องเวลา
            self.label_delay_min.setText("Wait Time (s)")
            self.point_delay_min_input.setText(str(point.get("delay_min", 1.0)))
        else:
            # แสดงช่องทั้งหมดกลับมาสำหรับจุดคลิกปกติ
            self.label_x.show()
            self.point_x_input.show()
            self.label_y.show()
            self.point_y_input.show()
            self.label_delay_max.show()
            self.point_delay_max_input.show()
            
            self.label_delay_min.setText("Delay min")
            self.point_x_input.setText(str(point.get("x", 0)))
            self.point_y_input.setText(str(point.get("y", 0)))
            self.point_delay_min_input.setText(str(point.get("delay_min", 2.0)))
            self.point_delay_max_input.setText(str(point.get("delay_max", point.get("delay_min", 3.0))))

    def add_point(self) -> None:
        if self.selected_step_index is None:
            return

        x_val = self.point_x_input.text().strip()
        y_val = self.point_y_input.text().strip()
        x = self.parse_int(x_val if x_val and x_val != "-" else "0", "X")
        y = self.parse_int(y_val if y_val and y_val != "-" else "0", "Y")
        
        delay_min = self.parse_non_negative_float(self.point_delay_min_input.text(), "Delay min")
        delay_max = self.parse_non_negative_float(self.point_delay_max_input.text(), "Delay max")
        delay_min, delay_max = self.normalize_delay_range(delay_min, delay_max)
        self.sequence[self.selected_step_index]["points"].append(
            {
                "x": x,
                "y": y,
                "delay_min": delay_min,
                "delay_max": delay_max,
            }
        )
        self.selected_point_index = len(self.sequence[self.selected_step_index]["points"]) - 1
        self.refresh_points_list()
        self.append_log("Point added.")
        self.auto_save()

    def add_delay(self) -> None:
        if self.selected_step_index is None:
            return

        self.sequence[self.selected_step_index]["points"].append(
            {
                "type": "delay",
                "x": 0,
                "y": 0,
                "delay_min": 5.0, # ค่า Default เริ่มที่ 5 วิ
                "delay_max": 5.0, 
            }
        )
        self.selected_point_index = len(self.sequence[self.selected_step_index]["points"]) - 1
        self.refresh_points_list()
        self.append_log("Delay item added. You can drag to reorder it.")
        self.auto_save()

    def add_step(self) -> None:
        step_number = len(self.sequence) + 1
        self.sequence.append(
            {
                "name": f"Step {step_number}",
                "run_order": 0,
                "points": [
                    {
                        "x": 0,
                        "y": 0,
                        "delay_min": 1.0,
                        "delay_max": 2.0,
                    }
                ],
                "after_delay": 1.0,
            }
        )
        self.selected_step_index = len(self.sequence) - 1
        self.refresh_step_list()
        self.append_log("Step added.")
        self.auto_save()

    def duplicate_step(self) -> None:
        if self.selected_step_index is None:
            self.show_info("Please select a step to duplicate.")
            return

        original_step = self.sequence[self.selected_step_index]
        new_step = copy.deepcopy(original_step)
        new_step["name"] = f"{original_step['name']} (Copy)"
        new_step["run_order"] = 0 
        
        self.sequence.append(new_step)
        self.refresh_step_list()
        
        self.step_list.setCurrentRow(len(self.sequence) - 1)
        self.append_log(f"Duplicated '{original_step['name']}'.")
        self.auto_save()

    def delete_step(self) -> None:
        if self.selected_step_index is None:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this step?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            deleted_order = self.sequence[self.selected_step_index].get("run_order", 0)
            del self.sequence[self.selected_step_index]
            
            if deleted_order > 0:
                for s in self.sequence:
                    if s.get("run_order", 0) > deleted_order:
                        s["run_order"] -= 1

            if not self.sequence:
                self.selected_step_index = None
            elif self.selected_step_index >= len(self.sequence):
                self.selected_step_index = len(self.sequence) - 1
                
            self.refresh_step_list()
            self.append_log("Step deleted.")
            self.auto_save()

    def on_step_moved(self, parent: Any, start: int, end: int, destination: Any, row: int) -> None:
        moved_step = self.sequence.pop(start)
        target_row = row - 1 if row > start else row
        self.sequence.insert(target_row, moved_step)
        
        self.selected_step_index = target_row
        self.update_step_list_texts()
        self.auto_save()
        QTimer.singleShot(0, lambda: self.step_list.setCurrentRow(self.selected_step_index))

    def on_point_moved(self, parent: Any, start: int, end: int, destination: Any, row: int) -> None:
        if self.selected_step_index is None:
            return
        
        points = self.sequence[self.selected_step_index]["points"]
        moved_point = points.pop(start)
        target_row = row - 1 if row > start else row
        points.insert(target_row, moved_point)
        
        self.selected_point_index = target_row
        self.auto_save()
        QTimer.singleShot(0, self.update_point_numbers)

    def update_point_numbers(self) -> None:
        if self.selected_step_index is None:
            return
        step = self.sequence[self.selected_step_index]
        
        self.points_list.blockSignals(True)
        for i, point in enumerate(step["points"]):
            item = self.points_list.item(i)
            if item:
                if point.get("type") == "delay":
                    item.setText(f'{i+1}. ⏳ [Wait] {point["delay_min"]}s')
                else:
                    item.setText(f'{i+1}. x={point["x"]}, y={point["y"]}, delay={point["delay_min"]}-{point["delay_max"]}')
        self.points_list.blockSignals(False)
        self.points_list.setCurrentRow(self.selected_point_index)

    def delete_point(self) -> None:
        if self.selected_step_index is None or self.selected_point_index is None:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this point?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            points = self.sequence[self.selected_step_index]["points"]
            del points[self.selected_point_index]
            if not points:
                self.selected_point_index = None
            elif self.selected_point_index >= len(points):
                self.selected_point_index = len(points) - 1
            self.refresh_points_list()
            self.append_log("Item deleted.")
            self.auto_save()

    def start_capture_countdown(self) -> None:
        if self.selected_step_index is None:
            self.show_info("Please select a step first to add the captured point.")
            return

        self.countdown_value = 3
        self.set_ui_enabled(False)
        
        self.capture_point_btn.setText(f"Capturing in {self.countdown_value}...")
        self.append_log(f"🎯 Move mouse to target! Capturing in {self.countdown_value}s...")

        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.update_capture_countdown)
        self.capture_timer.start(1000)

    def update_capture_countdown(self) -> None:
        self.countdown_value -= 1
        if self.countdown_value > 0:
            self.capture_point_btn.setText(f"Capturing in {self.countdown_value}...")
            self.append_log(f"⏳ {self.countdown_value}...")
        else:
            self.capture_timer.stop()
            self.capture_point_btn.setText("Capture Point (3s) 🎯")
            self.set_ui_enabled(True)
            self.execute_point_capture()

    def execute_point_capture(self) -> None:
        try:
            target_title = self.target_window_input.text().strip()
            
            x, y, is_client = capture_mouse_position(target_title)
            
            if is_client:
                self.append_log(f"✅ Captured (Client): X={x}, Y={y} on '{target_title}'")
            else:
                self.append_log(f"✅ Captured (Screen): X={x}, Y={y} (Game window not found)")

            new_point = self.create_default_point()
            new_point["x"] = x
            new_point["y"] = y
            
            self.sequence[self.selected_step_index]["points"].append(new_point)
            
            self.selected_point_index = len(self.sequence[self.selected_step_index]["points"]) - 1
            self.refresh_points_list()
            self.auto_save()
            
        except Exception as e:
            self.show_error(f"Failed to capture point: {str(e)}")

    def auto_save(self, silent: bool = True) -> None:
        if self.is_loading:
            return
        try:
            self.sync_selected_step_settings()
            self.sync_selected_point()
            if self.selected_step_index is not None:
                self.update_step_list_item(self.selected_step_index)
            
            payload = {
                "target_window_title": self.target_window_input.text().strip(),
                "start_hotkey": self.start_hotkey_combo.currentText(),
                "stop_hotkey": self.stop_hotkey_combo.currentText(),
                "sequence": self.sequence,
            }
            with USER_CONFIG_FILE.open("w", encoding="utf-8") as file:
                json.dump(payload, file, indent=2)
            if not silent:
                self.append_log(f"Saved all data to {USER_CONFIG_FILE.name}.")
        except Exception as exc:
            self.append_log(f"Auto-save skipped: {exc}")

    def load_saved_data(self) -> None:
        if not USER_CONFIG_FILE.exists():
            return

        try:
            self.is_loading = True
            with USER_CONFIG_FILE.open("r", encoding="utf-8") as file:
                payload = json.load(file)

            saved_title = payload.get("target_window_title", "").strip()
            saved_start_hotkey = payload.get("start_hotkey", "F9")
            saved_stop_hotkey = payload.get("stop_hotkey", "F10")
            saved_sequence = payload.get("sequence", [])

            if saved_title:
                self.target_window_input.setText(saved_title)
            
            self.start_hotkey_combo.setCurrentText(saved_start_hotkey)
            self.stop_hotkey_combo.setCurrentText(saved_stop_hotkey)

            if saved_sequence:
                normalized_sequence = []
                for step in saved_sequence:
                    points = []
                    for point in step.get("points", []):
                        points.append(self.normalize_point(point))

                    normalized_sequence.append(
                        {
                            "name": step.get("name", "Step"),
                            "run_order": int(step.get("run_order", 0)),
                            "points": points or [self.create_default_point()],
                            "after_delay": float(step.get("after_delay", 1.0)),
                        }
                    )
                self.sequence = normalized_sequence
        except Exception as exc:
            self.append_log(f"Could not load saved data: {exc}")
        finally:
            self.is_loading = False

    def start_all(self) -> None:
        self.start_worker(run_all=True)

    def run_selected_step(self) -> None:
        if self.selected_step_index is None:
            self.show_info("Select a step first.")
            return
        self.start_worker(run_all=False)

    def stop_run(self) -> None:
        self.stop_requested = True
        self.append_log("Stop requested.")

    def start_worker(self, run_all: bool) -> None:
        if self.worker and self.worker.is_alive():
            return

        try:
            self.sync_selected_step_settings()
            self.sync_selected_point()
        except Exception as exc:
            self.show_error(str(exc))
            return

        self.stop_requested = False
        
        if run_all:
            sequence_to_run = [s for s in self.sequence if s.get("run_order", 0) > 0]
            sequence_to_run.sort(key=lambda x: x.get("run_order", 0))
            
            if not sequence_to_run:
                self.show_info("Please check at least one step in the list to run.")
                return
                
            sequence = copy.deepcopy(sequence_to_run)
            self.append_log(f"Starting {len(sequence)} selected steps...")
        else:
            sequence = copy.deepcopy([self.sequence[self.selected_step_index]])

        target_title = self.target_window_input.text().strip()
        loop_enabled = self.loop_checkbox.isChecked()
        
        self.set_ui_enabled(False)

        self.worker = threading.Thread(
            target=self.run_sequence_worker,
            args=(target_title, sequence, loop_enabled),
            daemon=True,
        )
        self.worker.start()

    def run_sequence_worker(self, target_title: str, sequence: List[Dict[str, Any]], loop_enabled: bool) -> None:
        try:
            run_sequence(
                target_title=target_title,
                sequence=sequence,
                loop_enabled=loop_enabled,
                stop_requested=lambda: self.stop_requested,
                log=self.safe_log,
            )
        except Exception as exc:
            self.safe_log(f"Error: {exc}")
        finally:
            self.run_finished_signal.emit()

    def safe_log(self, message: str) -> None:
        self.log_signal.emit(message)

    def closeEvent(self, event) -> None:
        self.stop_requested = True
        if hasattr(self, 'start_hotkey_hook') and self.start_hotkey_hook:
            try: keyboard.remove_hotkey(self.start_hotkey_hook)
            except Exception: pass
        if hasattr(self, 'stop_hotkey_hook') and self.stop_hotkey_hook:
            try: keyboard.remove_hotkey(self.stop_hotkey_hook)
            except Exception: pass
        
        worker = self.worker
        if worker and worker.is_alive():
            worker.join(timeout=2)
            if worker.is_alive():
                event.ignore()
                self.show_info("Please wait a moment for the current run to stop.")
                return
        event.accept()

    def sync_selected_step_settings(self) -> None:
        if self.selected_step_index is None:
            return

        step = self.sequence[self.selected_step_index]
        step_name = self.step_name_input.text().strip()
        if not step_name:
            raise ValueError("Step name cannot be empty.")
        step["name"] = step_name
        step["after_delay"] = self.parse_float(self.after_delay_input.text(), "After delay")

    def update_step_list_item(self, index: int) -> None:
        if index is None or index < 0 or index >= len(self.sequence):
            return

        item = self.step_list.item(index)
        if item is None:
            self.refresh_step_list()
            return
            
        order = self.sequence[index].get("run_order", 0)
        prefix = f"[{order}]" if order > 0 else "[ ]"
        item.setText(f"{prefix} {self.sequence[index]['name']}")

    def sync_selected_point(self) -> None:
        if self.selected_step_index is None or self.selected_point_index is None:
            return

        current_point = self.sequence[self.selected_step_index]["points"][self.selected_point_index]
        is_delay = current_point.get("type") == "delay"

        if is_delay:
            x = 0
            y = 0
            # สำหรับ delay ให้อ่านค่าจากช่อง min เป็นเวลาเดียว แล้วปรับให้ min=max
            val = self.parse_non_negative_float(self.point_delay_min_input.text() or "0", "Wait time")
            delay_min = val
            delay_max = val
        else:
            x_value = self.point_x_input.text().strip()
            y_value = self.point_y_input.text().strip()
            if not x_value and not y_value:
                return
            x = self.parse_int(x_value, "X") if x_value else 0
            y = self.parse_int(y_value, "Y") if y_value else 0
            delay_min = self.parse_non_negative_float(self.point_delay_min_input.text() or "0", "Delay min")
            delay_max = self.parse_non_negative_float(self.point_delay_max_input.text() or "0", "Delay max")
            delay_min, delay_max = self.normalize_delay_range(delay_min, delay_max)
            
        updated_point = {
            "x": x,
            "y": y,
            "delay_min": delay_min,
            "delay_max": delay_max,
        }
        if is_delay:
            updated_point["type"] = "delay"
            
        self.sequence[self.selected_step_index]["points"][self.selected_point_index] = updated_point
        self.refresh_points_list()

    def parse_int(self, value: str, label: str) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"{label} must be an integer.") from exc

    def parse_float(self, value: str, label: str) -> float:
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"{label} must be a number.") from exc

    def parse_non_negative_float(self, value: str, label: str) -> float:
        parsed = self.parse_float(value, label)
        if parsed < 0:
            raise ValueError(f"{label} must be zero or greater.")
        return parsed

    def create_default_point(self) -> Dict[str, float]:
        return {
            "x": 0,
            "y": 0,
            "delay_min": 1.0,
            "delay_max": 2.0,
        }

    def normalize_point(self, point: Any) -> Dict[str, Any]:
        if isinstance(point, dict):
            legacy_delay = float(point.get("delay", CLICK_DELAY_SECONDS))
            legacy_jitter = max(0.0, float(point.get("jitter", 0.0)))
            delay_min = float(point.get("delay_min", max(0.0, legacy_delay - legacy_jitter)))
            delay_max = float(point.get("delay_max", legacy_delay + legacy_jitter))
            delay_min, delay_max = self.normalize_delay_range(delay_min, delay_max)
            
            result = {
                "x": int(point.get("x", 0)),
                "y": int(point.get("y", 0)),
                "delay_min": delay_min,
                "delay_max": delay_max,
            }
            if "type" in point:
                result["type"] = str(point["type"])
            return result

        return {
            "x": int(point[0]),
            "y": int(point[1]),
            "delay_min": 1.0,
            "delay_max": 2.0,
        }

    def normalize_delay_range(self, delay_min: float, delay_max: float) -> Tuple[float, float]:
        if delay_min <= delay_max:
            return delay_min, delay_max
        return delay_max, delay_min


def create_app() -> Tuple[QApplication, ClickSequenceApp]:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    window = ClickSequenceApp()
    return app, window