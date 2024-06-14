import ttkbootstrap as ttk


class Messagebox(ttk.Toplevel):
    """
    弹窗
    """
    def __new__(cls, *args, **kwargs):   # 单例模式
        if hasattr(cls, "instance"):
            return cls.instance
        else:
            cls.instance = super().__new__(cls)
            return cls.instance
    def __call__(self, *args, **kwargs) -> None: # ()调用返回点击值
        if hasattr(self, "return_value"):
            return self.return_value
        else:
            return False
    def __init__(self,
                 master,
                 title="Messagebox",
                 text="",
                 mode = "read", # 模式，read表示只读，write表示可写
                 text_color="red",
                 text_font=("", 14,"bold"),
                 button_font=("", 14),
                 button_text_color="white",
                 button_text="确定",
                 button_text2 = None,
                 button_command=None,
                 button_style="info-outline",
                 text_line_max_length = 20,
                 progressbar = False,
                 progressbar_text = ""):
        super().__init__(master)
        self.master = master
        self.mode = mode
        self.text = text
        self.text_color = text_color
        self.text_font = text_font
        self.button_font = button_font
        self.button_text_color = button_text_color
        self.button_text = button_text
        self.button_text2 = button_text2
        self.button_command = button_command
        self.button_style = button_style
        self.text_line_max_length = text_line_max_length
        self.progressbar = progressbar
        self.progressbar_text = progressbar_text

        if self.button_command is None:
            self.button_command = self.click_button
        self.title(title)
        # 设置弹窗大小，弹出位置为屏幕中心
        self.geometry(f"+{int(self.winfo_screenwidth() / 2 - 200)}+{int(self.winfo_screenheight() / 2 - 100)}")
        self.resizable(False, False)

        self.grid_columnconfigure([0,1], weight=1,minsize=200)
        self.grid_rowconfigure([0,1], weight=1,minsize=100)
        if not self.progressbar:
            self.create_label_or_entry()
            self.create_button()
            self.bind("<Return>", lambda event: self.click_button(event, return_value=True))
        else:
            fg = ttk.Progressbar(self,
                            maximum=100,
                            length=500,
                            bootstyle="success",)
            fg.grid(row=0,column=0,columnspan=2,padx=20,pady=20,sticky="nsew")
            la = ttk.Label(self,text="",bootstyle="success",justify="center",anchor="center",font=("", 14,"bold"))
            la.grid(row=1,column=0,columnspan=2,padx=20,pady=20,sticky="nsew")
            self.update_progress(fg,la,0)
        self.protocol("WM_DELETE_WINDOW", lambda: self.click_button(return_value=False))
        self.focus_set()
        self.master.wait_window(self)
    def update_progress(self,fg,la,value:int) -> None:
        self.value = value
        self.focus_set()
        if value <= 100:
            fg.configure(value=value)
            la.configure(text=f"模拟{self.progressbar_text}中 {value}%")
            if value == 100:
                self.click_button(return_value=True)
                return
            self.after(25, lambda: self.update_progress(fg,la, value + 1))
    def create_label_or_entry(self) -> None:
        text = self.insert_newlines(self.text, self.text_line_max_length)
        if self.mode == "read":
            ttk.Style().configure("Messagebox.TLabel", font=self.text_font, foreground=self.text_color)
            lab = ttk.Label(self,
                            text=text,
                            style="Messagebox.TLabel").grid(rowspan=1,
                                                            columnspan=2,
                                                            padx=20,
                                                            pady=20,
                                                            sticky="nsew")
        elif self.mode == "write":
            self.text_var = ttk.StringVar()
            self.text_var.set(text)
            ttk.Style().configure("Messagebox.TEntry", foreground=self.text_color)
            entry = ttk.Entry(self,
                            textvariable=self.text_var,
                            font=self.text_font,
                            style="Messagebox.TEntry").grid(rowspan=1,
                                                           columnspan=2,
                                                           padx=20,
                                                           pady=20,
                                                           sticky="nsew")
    def create_button(self) -> None:
        ttk.Button(self,
                   text=self.button_text,
                   command=lambda: [self.button_command(), self.click_button(return_value=True)],
                   bootstyle=self.button_style, ).grid(row=1,
                                                  column=1,
                                                  sticky="se",
                                                  ipadx=10,
                                                  ipady=10,
                                                  padx=20,
                                                  pady=20)
        if not self.button_text2 is None:
            ttk.Button(self,
                       text=self.button_text2,
                       command=lambda: [self.click_button(return_value=False)],
                       bootstyle=self.button_style, ).grid(row=1,
                                                      column=0,
                                                      sticky="sw",
                                                      ipadx=10,
                                                      ipady=10,
                                                      padx=20,
                                                      pady=20)
    def click_button(self, event=None,return_value = None) ->bool|str:
        if self.progressbar:
            if self.value != 100:
                return False
        self.return_value = return_value
        self.grab_release()
        self.destroy()
        self.master.unbind("Return")
        if self.return_value == True:
            if self.mode == "write":
                self.return_value = self.text_var.get() if self.text_var.get() else "0"


    def insert_newlines(self,text:str, max_length:int) -> str:
        # 初始化结果字符串
        result = ""
        # 遍历原始文本
        if len(text) <= max_length:
            return text
        for i in range(len(text)):
            # 如果当前字符是空格或者我们达到了最大长度（除了最后一个字符），则插入换行符
            if (i > 0 and text[i - 1] == ' ') or ( i % max_length == 0):
                result += "\n"
                # 添加当前字符到结果字符串
            result += text[i]
            # 移除开头可能多余的换行符（如果文本从空格开始）
        if result.startswith("\n"):
            result = result[1:]
        return result

def test(title="弹窗演示", text = "请运行main.py"):
    test = ttk.Window(title=title, themename="superhero")
    # 隐藏root窗口
    test.withdraw()
    Messagebox(test, text = text)
    test.mainloop()


if __name__ == '__main__':

    root = ttk.Window(title="弹窗演示", themename="superhero")
    root.withdraw()
    Messagebox(root, text="弹窗演示")
    Messagebox(root, progressbar=True)
    # root.mainloop()
