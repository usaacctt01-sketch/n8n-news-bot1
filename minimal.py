import tkinter as tk
from tkinter import messagebox

print("Starting Minimal GUI...")

try:
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("300x200")
    
    label = tk.Label(root, text="ถ้าเห็นหน้านี้ แปลว่า GUI ใช้ได้", font=("Arial", 14))
    label.pack(pady=50)
    
    print("GUI Created successfully")
    root.mainloop()
except Exception as e:
    print(f"Error: {e}")
    input("Press Enter to exit...")
