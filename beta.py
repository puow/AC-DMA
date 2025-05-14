import serial
import time
import math
import threading
import keyboard

# MacKu device settings
MACCU_PORT = "COM5"
BAUD_RATE = 4000000
PIXELS_PER_360 = 3960  # Calibrated value
SENSITIVITY = 1.2      # Adjust for smoother movement
AIM_KEY = "ctrl"       # Hotkey for aiming
aimbot_enabled = False

# Connect to MacKu device
def connect_macku():
    try:
        makcu = serial.Serial(MACCU_PORT, BAUD_RATE, timeout=1)
        print(f"[+] Connected to MacKu on {MACCU_PORT} at {BAUD_RATE} baud")
        return makcu
    except serial.SerialException as e:
        print(f"[-] Failed to connect to MacKu: {e}")
        return None

# MacKu move command
def macku_move(dx, dy):
    if makcu:
        command = f"km.move({int(dx)}, {int(dy)})\r".encode()
        makcu.write(command)
        makcu.flush()

# Toggle aimbot
def toggle_aimbot():
    global aimbot_enabled
    aimbot_enabled = not aimbot_enabled
    print(f"[+] Aimbot {'enabled' if aimbot_enabled else 'disabled'}")

# Normalize angle difference to [-180, 180]
def normalize_angle(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

# Calculate the pixel movement based on angle difference
def calculate_pixel_movement(angle):
    return angle * (PIXELS_PER_360 / 360) * SENSITIVITY

# Aimbot loop
def aimbot_loop():
    while True:
        if aimbot_enabled:
            # Simulated target data (replace with DMA data)
            target_angle = 90  # Example: target is to the right
            current_angle = 0  # Example: current aim direction
            
            # Calculate the difference
            delta_angle = normalize_angle(target_angle - current_angle)
            pixel_move = calculate_pixel_movement(delta_angle)

            # Move the MacKu device
            macku_move(pixel_move, 0)
            print(f"[+] Moving {pixel_move} pixels to adjust aim")
        
        time.sleep(0.01)

# Start the aimbot loop in a separate thread
def start_aimbot():
    threading.Thread(target=aimbot_loop, daemon=True).start()

# Hotkey listener
def hotkey_listener():
    print("[*] Press 'ctrl' to toggle the aimbot.")
    keyboard.add_hotkey(AIM_KEY, toggle_aimbot)

# Initialize MacKu
makcu = connect_macku()

# Start aimbot and hotkey listener
start_aimbot()
hotkey_listener()

# Keep the program running
print("[*] Aimbot is ready. Use 'ctrl' to toggle.")
keyboard.wait()
