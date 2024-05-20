import ttkbootstrap as ttk
from home import Home
from data import *
from messagebox import Messagebox


class Login(ttk.Frame):
    """
    登录界面
    """
    font = ("", 14)
    tip_font = ("Arial", 11)
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("登录")
        # 显示到屏幕中心
        self.master.geometry(f"600x400+{(self.master.winfo_screenwidth() - 600) // 2}"
                             f"+{(self.master.winfo_screenheight() - 400) // 2}")
        self.master.resizable(False, False)
        self.pack(pady=70, anchor="center")

        self.button_style()

        # 初始化变量
        self.tip_text = ttk.StringVar()
        self.account_var = ttk.StringVar()
        self.password_var = ttk.StringVar()

        self.create_widgets()
        self.master.bind("<Return>", self.click_login_button)

    def button_style(self, *args, **kwargs):
        ttk.Style().configure("TButton", font=self.font)

    def create_widgets(self):
        # 创建提示label
        self.tip_text.set("请输入账号密码")
        tip_label = ttk.Label(self, textvariable=self.tip_text, font=self.tip_font, foreground="red")
        tip_label.grid(row=0, column=2)
        # 创建账号输入框
        account_label = ttk.Label(self, text="账号:", font=self.font)
        account_label.grid(row=1, column=0, padx=10, pady=20)
        account_entry = ttk.Entry(self, font=self.font,textvariable=self.account_var)
        account_entry.grid(row=1, column=1, padx=10, pady=20, columnspan=4)

        # 创建密码输入框
        password_label = ttk.Label(self, text="密码:", font=self.font)
        password_label.grid(row=2, column=0, padx=10, pady=20)
        password_entry = ttk.Entry(self, show="*", font=self.font, textvariable=self.password_var)
        password_entry.grid(row=2, column=1, padx=10, pady=20, columnspan=4)

        # 创建登录按钮
        login_button = ttk.Button(self, text="登录", bootstyle="info-outline")
        login_button.bind("<Button-1>", self.click_login_button)
        login_button.grid(row=3, column=2, pady=25)

    def click_login_button(self, event=None):
        """

        :param event:
        :return:
        """
        login_verification = self.login_verification()
        # 登录成功
        if login_verification:
            self.destroy()
            self.master.unbind("Return")
            Home(self.master,self.user)

    def message(self,master = None, title="提示",text="",button_text="确定",*args, **kwargs):
        if master is None:
            master = self.master
        self.master.unbind("Return")
        Messagebox(master,
                   title=title,
                   text=text,
                   button_text=button_text,
                   *args, **kwargs)
        self.master.bind("<Return>", self.click_login_button)


    # 登录验证
    def login_verification(self):

        account = self.account_var.get()
        password = self.password_var.get()
        if not account or not password:
            self.tip_text.set("未输入账号或密码")
            self.message(text="未输入账号或密码")
            return False

        self.users_info = read_data(data_path) # 使用pandas读取数据
        if self.users_info is None:
            return False
        else:
            # 账号密码验证
            user = self.users_info[self.users_info["account"] == account]
            if user.empty:
                self.tip_text.set("账号不存在")
                self.message(text="账号不存在,请重新输入")
                return False
            elif user["password"].values[0] != password:
                self.tip_text.set("密码错误")
                self.message(text="密码错误,请重新输入")
                return False
            else:
                self.user = user
                return True
