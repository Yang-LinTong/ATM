import ttkbootstrap as ttk
from login import Login


def main():
    root = ttk.Window(themename="superhero")
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
