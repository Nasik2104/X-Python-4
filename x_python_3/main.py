import tkinter as tk

from app import App


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, "large_dataset.csv")
    root.mainloop()
