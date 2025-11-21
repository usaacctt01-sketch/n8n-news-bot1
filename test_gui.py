import tkinter as tk
from tkinter import messagebox

def main():
    try:
        root = tk.Tk()
        root.title("Test GUI")
        root.geometry("300x200")
        
        label = tk.Label(root, text="Hello! If you see this, GUI works.", font=("Arial", 12))
        label.pack(pady=50)
        
        btn = tk.Button(root, text="Click Me", command=lambda: messagebox.showinfo("Info", "It works!"))
        btn.pack()
        
        print("GUI Started")
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter...")

if __name__ == "__main__":
    main()
