import ttkbootstrap as ttk
import time
from user_actions import UserActions,mouse_enter,mouse_leave

class Home(ttk.Frame):
    """
    主界面
    """
    win_width = 1200           # 宽度
    win_height = 1000          # 高度
    win_row = 2                # 列数
    win_column = 10            # 行数
    # frame1
    frame1_row = 3             # 行数
    frame1_column = 5          # 列数
    # frame2
    frame2_row = 1             # 行数
    frame2_column = 2          # 列数
    frame2_font = ("", 16)     # 字体

    # 总权重
    row_weight = 100
    # 窗口权重
    frame1_row_weight = 90      # 0-100
    frame2_row_weight = row_weight-frame1_row_weight
    frame1_row_minsize = int(frame1_row_weight/row_weight*win_height)
    frame2_row_minsize = int(frame2_row_weight/row_weight*win_height)
    # button
    button_background = "#5bc0de"
    button_foreground = "white"   # 字体颜色
    button_font = ("", 23)
    button_padx = 20    # 横向填充
    button_pady = 80    # 纵向填充

    def __init__(self, master,user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.user_actions = UserActions(self.master, self,self.user)
        # 获取当前时间
        self.time = ttk.StringVar()
        self.update_time()
        self.master.title("ATM模拟")
        # 取消回车键触发
        self.master.unbind("<Return>")
        # 显示到屏幕中心
        self.master.geometry(f"{self.win_width}x{self.win_height}+{int((self.master.winfo_screenwidth() - self.win_width) / 2)}"
                             f"+{int((self.master.winfo_screenheight() - self.win_height) / 2)}")
        self.master.resizable(False, False)
        self.pack(fill=ttk.BOTH, expand=True)

        # 设置行列权重
        self.grid_rowconfigure(0, weight=self.frame1_row_weight, minsize=self.frame1_row_minsize)
        self.grid_rowconfigure(1, weight=self.frame2_row_weight,minsize=self.frame2_row_minsize)
        self.grid_columnconfigure([*range(self.win_column)], weight=1)

        # 创建样式
        self.button_style()

        # 初始化frame1, frame2
        self.frame1 = ttk.Frame(self,height=self.frame1_row_minsize)
        self.frame2 = ttk.Frame(self,bootstyle="secondary",height=self.frame2_row_minsize)
        self.create_widgets()
    def button_style(self, *args, **kwargs):
        ttk.Style().configure("TButton",
                              font=self.button_font,)

    def create_widgets(self):
        # 初始化frame1, frame2
        self.frame1.grid(row=0, column=0, columnspan=self.win_column, sticky=ttk.NSEW)
        self.frame2.grid(row=self.win_row-1, column=0, columnspan=self.win_column, sticky=ttk.NSEW)

        # 设置frame1, frame2的行列权重
        self.frame1.grid_rowconfigure([*range(self.frame1_row)], weight=1)
        self.frame1.grid_columnconfigure([*range(self.frame1_column)], weight=1)
        self.frame2.grid_rowconfigure([*range(self.frame2_row)], weight=1, minsize=self.frame2_row_minsize)
        self.frame2.grid_columnconfigure([*range(self.frame2_column)], weight=1)

        self.create_framewidgets()
    def create_framewidgets(self):
        # frame1的组件
        self.frame1_widgets(self.frame1)

        # frame2的组件
        self.frame2_widgets(self.frame2)

    def frame1_widgets(self, frame1):
        buttons_config = [
            {
                "text": "个人信息",
                "command": self.user_actions.info_show,
                "row": 0,
                "column": 0,
            },
            {
                "text": "存款",
                "command": self.user_actions.deposit,
                "row": 0,
                "column": self.frame1_column - 1,
            },
            {
                "text": "取款",
                "command": self.user_actions.withdrawal,
                "row": 1,
                "column": 0,
            },
            {
                "text": "转账",
                "command": self.user_actions.transfer,
                "row": 1,
                "column": self.frame1_column - 1,
            },
            {
                "text": "修改密码",
                "command": self.user_actions.info_revise,
                "row": 2,
                "column": 0,
            },
            {
                "text": "切换用户",
                "command": self.user_actions.get_handoff,
                "row": 2,
                "column": self.frame1_column - 1,
            }
        ]

        # 辅助函数，用于创建和配置按钮
        def create_button(frame, config):
            button = ttk.Button(frame, text=config["text"], command=config["command"], bootstyle="info-outline")
            button.grid(row=config["row"], column=config["column"], padx=self.button_padx, pady=self.button_pady, sticky=ttk.NSEW)
            return button

        # 使用循环创建和配置按钮，并为所有按钮绑定鼠标进入和离开事件
        for i, config in enumerate(buttons_config):
            button = create_button(self.frame1, config)
            button.bind("<Enter>", mouse_enter)
            button.bind("<Leave>", mouse_leave)



    def frame2_widgets(self, frame2):
        # 在frame2左侧显示当前用户名
        frame2_label_name = ttk.Label(self.frame2,
                                      text=f" 当前用户: {self.user['name'].values[0]}",
                                      bootstyle="inverse-secondary",
                                      font=self.frame2_font)
        frame2_label_name.grid(row=0, column=0, sticky="w")

        # frame2右侧显示当前系统时间
        frame2_label_time = ttk.Label(self.frame2,
                                      textvariable=self.time,
                                      bootstyle="inverse-secondary",
                                      font=self.frame2_font)
        frame2_label_time.grid(row=0, column=1,padx=20, sticky="e")

    def update_time(self):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.time.set(f"当前时间: {now_time}")
        self.master.after(1000, self.update_time)
