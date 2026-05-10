import math
import random
import time
from typing import List, Dict, Any, Callable, Tuple
import pywintypes

import win32api
import win32con
import win32gui

from config import (
    CLICK_DELAY_SECONDS,
    LOOP_DELAY_SECONDS,
    PRESS_HOLD_SECONDS,
    START_DELAY_SECONDS,
)


def normalize_title(value: str) -> str:
    return value.strip().lower()


def is_candidate_window(hwnd: int) -> bool:
    try:
        if not win32gui.IsWindow(hwnd):
            return False
        if not win32gui.IsWindowVisible(hwnd):
            return False
        if not win32gui.IsWindowEnabled(hwnd):
            return False
        if win32gui.GetParent(hwnd):
            return False
        return bool(win32gui.GetWindowText(hwnd).strip())
    except pywintypes.error:
        return False


def find_target_window(title_keyword: str) -> int:
    normalized_keyword = normalize_title(title_keyword)
    if not normalized_keyword:
        raise ValueError("Target window title is empty.")

    exact_matches = []
    partial_matches = []
    for hwnd in list_visible_windows():
        try:
            title = win32gui.GetWindowText(hwnd).strip()
            normalized_title = normalize_title(title)

            if normalized_title == normalized_keyword:
                exact_matches.append(hwnd)
            elif normalized_keyword in normalized_title:
                partial_matches.append(hwnd)
        except pywintypes.error:
            continue

    matches = exact_matches or partial_matches

    if not matches:
        raise RuntimeError(f'No window found containing title: "{title_keyword}"')

    return matches[0]


def list_visible_windows() -> List[int]:
    windows = []

    def callback(hwnd: int, _: Any) -> bool:
        if is_candidate_window(hwnd):
            windows.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return windows


# --- ฟังก์ชันใหม่: เลื่อนเมาส์ให้เนียนเหมือนคน ---
def move_mouse_smoothly(target_x: int, target_y: int, stop_requested: Callable[[], bool]) -> bool:
    start_x, start_y = win32api.GetCursorPos()
    
    # สุ่มความเร็วในการสไลด์เมาส์ (0.15 - 0.4 วินาที)
    duration = random.uniform(0.15, 0.4)
    
    # คำนวณระยะห่าง ถ้าระยะใกล้มากอยู่แล้ว ให้วาร์ปไปเลยไม่เสียเวลา
    distance = math.hypot(target_x - start_x, target_y - start_y)
    if distance < 5:
        win32api.SetCursorPos((target_x, target_y))
        return True

    # แบ่งระยะทางเป็นสเต็ปย่อยๆ ยิ่งเฟรมเรทเยอะ ยิ่งเนียน (อิงจาก 60 เฟรมต่อวิ)
    steps = int(duration * 60) 
    if steps < 5:
        steps = 5

    for i in range(1, steps + 1):
        if stop_requested():
            return False
        
        t = i / steps
        # ใช้สมการ Sine (Ease-out) ทำให้เริ่มเลื่อนเร็ว แล้วชะลอช้าๆ ตอนปลายทาง
        t_eased = math.sin(t * math.pi / 2)
        
        current_x = int(start_x + (target_x - start_x) * t_eased)
        current_y = int(start_y + (target_y - start_y) * t_eased)
        
        win32api.SetCursorPos((current_x, current_y))
        time.sleep(duration / steps)
        
    # ให้ชัวร์ว่าลงตรงเป้าเป๊ะๆ ในเฟรมสุดท้าย
    win32api.SetCursorPos((target_x, target_y))
    return True


def click(hwnd: int, point: Dict[str, Any], stop_requested: Callable[[], bool], click_delay: float = CLICK_DELAY_SECONDS) -> bool:
    if not win32gui.IsWindow(hwnd):
        raise RuntimeError("Target window was closed or is no longer accessible.")

    screen_point = resolve_screen_point(hwnd, (point["x"], point["y"]))

    if not interruptible_sleep(0.02, stop_requested):
        return False

    # แทนที่จะวาร์ป เปลี่ยนมาเรียกใช้ฟังก์ชันสไลด์เมาส์แทน
    if not move_mouse_smoothly(screen_point[0], screen_point[1], stop_requested):
        return False

    # พักหายใจ 0.05 วิ ก่อนกดคลิกลงไป (จังหวะคนกดเมาส์)
    time.sleep(0.05)
    
    if not interruptible_sleep(0.05, stop_requested):
        return False

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    if not interruptible_sleep(PRESS_HOLD_SECONDS, stop_requested):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        return False
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    return interruptible_sleep(click_delay, stop_requested)


def interruptible_sleep(seconds: float, stop_requested: Callable[[], bool], interval: float = 0.1) -> bool:
    end_time = time.time() + max(0, seconds)
    while time.time() < end_time:
        if stop_requested():
            return False
        remaining = end_time - time.time()
        time.sleep(min(interval, remaining))
    return True


def to_screen_point(hwnd: int, point: Tuple[int, int]) -> Tuple[int, int]:
    return win32gui.ClientToScreen(hwnd, point)


def is_point_inside_window(hwnd: int, point: Tuple[int, int]) -> bool:
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        x, y = point
        return left <= x < right and top <= y < bottom
    except pywintypes.error:
        raise RuntimeError("Window is no longer accessible.")


def is_point_inside_client(hwnd: int, point: Tuple[int, int]) -> bool:
    try:
        client_x, client_y = point
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        return left <= client_x < right and top <= client_y < bottom
    except pywintypes.error:
        raise RuntimeError("Window is no longer accessible.")


def resolve_screen_point(hwnd: int, point: Tuple[int, int]) -> Tuple[int, int]:
    if is_point_inside_client(hwnd, point):
        return to_screen_point(hwnd, point)

    if is_point_inside_window(hwnd, point):
        return point

    raise ValueError(
        f"Point {point} is neither inside the current window nor a valid client coordinate."
    )


def prepare_target_window(hwnd: int, stop_requested: Callable[[], bool]) -> bool:
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        if not interruptible_sleep(0.5, stop_requested):
            return False

    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    return interruptible_sleep(0.3, stop_requested)


def capture_mouse_position(target_title: str) -> Tuple[int, int, bool]:
    try:
        screen_pos = win32api.GetCursorPos()
        try:
            hwnd = find_target_window(target_title)
            client_pos = win32gui.ScreenToClient(hwnd, screen_pos)
            return client_pos[0], client_pos[1], True
        except Exception:
            return screen_pos[0], screen_pos[1], False
    except Exception as e:
        raise RuntimeError(f"Could not read cursor position: {e}")


def run_step(hwnd: int, step: Dict[str, Any], stop_requested: Callable[[], bool]) -> bool:
    points = step.get("points", [])
    after_delay = float(step.get("after_delay", 0))

    for point in points:
        if stop_requested():
            return False
            
        if point.get("type") == "delay":
            delay_time = get_point_delay(point)
            if not interruptible_sleep(delay_time, stop_requested):
                return False
            continue

        if point["x"] == 0 and point["y"] == 0:
            raise ValueError(f'Placeholder point found in "{step["name"]}".')
        
        click_delay = get_point_delay(point)
        if not click(hwnd, point, stop_requested, click_delay):
            return False

    return interruptible_sleep(after_delay, stop_requested)


def get_point_delay(point: Dict[str, Any]) -> float:
    legacy_delay = float(point.get("delay", CLICK_DELAY_SECONDS))
    legacy_jitter = max(0.0, float(point.get("jitter", 0.0)))
    delay_min = float(point.get("delay_min", max(0.0, legacy_delay - legacy_jitter)))
    delay_max = float(point.get("delay_max", legacy_delay + legacy_jitter))
    delay_min = max(0.0, delay_min)
    delay_max = max(0.0, delay_max)
    if delay_min > delay_max:
        delay_min, delay_max = delay_max, delay_min
    return random.uniform(delay_min, delay_max)


def run_sequence(target_title: str, sequence: List[Dict[str, Any]], loop_enabled: bool, stop_requested: Callable[[], bool], log: Callable[[str], None]) -> None:
    log(f"Starting in {START_DELAY_SECONDS:.0f} seconds.")
    if not interruptible_sleep(START_DELAY_SECONDS, stop_requested):
        log("Run stopped.")
        return

    loop_count = 1
    while True:
        try:
            hwnd = find_target_window(target_title)
            if not prepare_target_window(hwnd, stop_requested):
                log("Run stopped.")
                return

            if loop_enabled:
                log(f"--- Loop #{loop_count} Started ---")

            for step in sequence:
                if stop_requested():
                    log("Run stopped.")
                    return

                log(f'Running "{step["name"]}"...')
                completed = run_step(hwnd, step, stop_requested)
                if not completed:
                    log("Run stopped.")
                    return

            if not loop_enabled or stop_requested():
                log("Run finished.")
                return

            log(f"Loop #{loop_count} completed. Waiting {LOOP_DELAY_SECONDS:.0f}s for next loop...")
            if not interruptible_sleep(LOOP_DELAY_SECONDS, stop_requested):
                log("Run stopped.")
                return

            loop_count += 1
            
        except Exception as e:
            log(f"Error during execution: {e}")
            log("Run stopped due to error.")
            return