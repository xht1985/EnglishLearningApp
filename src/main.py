import tkinter as tk
from gui import GUI

def main():
    root = tk.Tk()
    app = GUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()

if __name__ == "__main__":
    main()