import ttkbootstrap as ttk
from messagebox import Messagebox
import login
import re
from data import write_data,data_path
from event_dispose import withdraw_or_deposit,transfer,displayPassword,click_revise

# 当鼠标移动到按钮上时，光标变为手型
def mouse_enter(event=None):
    if event:
        event.widget.config(cursor="hand2")


# 当鼠标离开按钮时，光标恢复为默认样式
def mouse_leave(event=None):
    if event:
        event.widget.config(cursor="")


class UserActions:
    def __init__(self, master, home_win, user):
        self.master = master
        self.home_win = home_win
        self.user = user

    def info_show(self):
        self.window_destroy()
        font = ("", 20)
        label_config = [
            {
                "text": "用户名：",
                "row": 0,
                "column": 0,
            },
            {
                "text": "账户：",
                "row": 1,
                "column": 0,
            },
            {
                "text": "余额：",
                "row": 2,
                "column": 0,
            },
            {
                "text": self.user["name"].values[0],
                "row": 0,
                "column": 1,
            },
            {
                "text": self.user["account"].values[0],
                "row": 1,
                "column": 1,
            },
            {
                "text": self.user["balance"].values[0],
                "row": 2,
                "column": 1,
                "foreground": "red" if self.user["balance"].values[0] < 10_000 else "green",
            },
            {
                "text": "个人信息",
                "row": 0,
                "column": 4,
            },
        ]
        for label in label_config:
            ttk.Label(self.home_win.frame1,
                    text=label["text"],
                    font=font,
                    foreground=label.get("foreground", ""),
                    ).grid(row=label["row"], column=label["column"], padx=10)
        self.button_return()
    def deposit(self):
        """
        存款
        :return:
        """
        self.window_destroy()
        config = [
            {
                "text": "100",
                "row": 0,
                "column": 0,
                "command": withdraw_or_deposit,
            },
            {
                "text": "500",
                "row": 0,
                "column": 4,
                "command":withdraw_or_deposit,
            },
            {
                "text": "1000",
                "row": 1,
                "column": 0,
                "command": withdraw_or_deposit,
            },
            {
                "text": "2000",
                "row": 1,
                "column": 4,
                "command": withdraw_or_deposit,
            },
            {
                "text": "5000",
                "row": 2,
                "column": 0,
                "command": withdraw_or_deposit,
            },
            {
                "text": "other",
                "row": 2,
                "column": 4,
                "command":withdraw_or_deposit,
            },
        ]
        for button in config:
            ttk.Button(self.home_win.frame1,
                       text=button["text"],
                       bootstyle="info-outline",
                       command= lambda amount=button["text"],
                                       btn=button["command"],
                                        master = self, : btn(self=master, amount=amount,mode="deposit"),
                       ).grid(row=button["row"], column=button["column"], padx=30, pady=50, ipadx=0, ipady=10, sticky="nsew")
        self.button_return()

    def withdrawal(self):
        """
        提款
        :return:
        """
        self.window_destroy()
        config = [
            {
                "text": "100",
                "row": 0,
                "column": 0,
                "command": withdraw_or_deposit,
            },
            {
                "text": "500",
                "row": 0,
                "column": 4,
                "command":withdraw_or_deposit,
            },
            {
                "text": "1000",
                "row": 1,
                "column": 0,
                "command": withdraw_or_deposit,
            },
            {
                "text": "2000",
                "row": 1,
                "column": 4,
                "command": withdraw_or_deposit,
            },
            {
                "text": "5000",
                "row": 2,
                "column": 0,
                "command": withdraw_or_deposit,
            },
            {
                "text": "other",
                "row": 2,
                "column": 4,
                "command":withdraw_or_deposit,
            },
        ]
        for button in config:
            ttk.Button(self.home_win.frame1,
                       text=button["text"],
                       bootstyle="info-outline",
                       command= lambda amount=button["text"],
                                       btn=button["command"],
                                        master = self, : btn(self=master, amount=amount,mode="withdrawal"),
                       ).grid(row=button["row"], column=button["column"], padx=30, pady=50, ipadx=0, ipady=10, sticky="nsew")
        self.button_return()

    def transfer(self):
        """
        转账
        :return:
        """
        self.window_destroy()
        font = ("", 18)
        other_account = ttk.StringVar()
        amount = ttk.StringVar()
        password = ttk.StringVar()
        label_or_entry = config =[
            {
                "text": "对方账户:",
                "row": 0,
                "column": 0,
            },
            {
                "textvariable": other_account,
                "row": 0,
                "column": 1,
            },
            {
                "text": "转账金额:",
                "row": 1,
                "column": 0,
            },
            {
                "textvariable": amount,
                "row": 1,
                "column": 1,
            },
            {
                "text": "确认密码:",
                "row": 2,
                "column": 0,
            },
            {
                "textvariable": password,
                "row": 2,
                "column": 1,
                "show": "*",
            },
        ]
        def click_button(event=None):
            transfer(self, other_account.get(), amount.get(), password.get())
            self.master.bind("<Return>", click_button)
        for widget in label_or_entry:
            if "textvariable" in widget:
                ttk.Entry(self.home_win.frame1,
                          textvariable=widget["textvariable"],
                          font=font,
                          width=30,
                          show=widget.get("show", ""),
                          ).grid(row=widget["row"], column=widget["column"], padx=10,columnspan=2)
            else:
                ttk.Label(self.home_win.frame1,
                          text=widget["text"],
                          font=font,
                          ).grid(row=widget["row"], column=widget["column"],padx = 30,sticky="e")
            # 创建按钮
            ttk.Button(self.home_win.frame1,
                       text="确认转账",
                       bootstyle="warning-outline",
                       command= click_button,
                       ).grid(row=3, column=2, padx=10, pady=10, ipadx=10, ipady=10)
            self.button_return(row=3, column=4)
            self.master.bind("<Return>", click_button)
    def info_revise(self):
        """
        修改密码
        :return:
        """
        self.window_destroy()
        font = ("", 18)
        self.entry_list = []
        # 密码显示状态 True: 显示明文，False: 显示密文
        self.password_show_status = False
        self.old_password = ttk.StringVar()
        self.new_password1 = ttk.StringVar()
        self.new_password2 = ttk.StringVar()
        entry_or_label_config = [
            {
                "text": "旧密码：",
                "row": 0,
                "column": 0,
            },
            {
                "textvariable":self.old_password,
                "row": 0,
                "column": 1,
            },
            {
                "text": "新密码：",
                "row": 1,
                "column": 0,
            },
            {
                "textvariable":self.new_password1,
                "row": 1,
                "column": 1,
            },
            {
                "text": "再次输入新密码：",
                "row": 2,
                "column": 0,
            },
            {
                "textvariable":self.new_password2,
                "row": 2,
                "column": 1,
            },
        ]
        btn_config = [
            {
                "text": "显示密码",
                "row": 3,
                "column": 1,
                "command":displayPassword,
                "bootstyle" : "warning-outline",
            },
            {
                "text": "确认修改",
                "row": 3,
                "column": 2,
                "command":click_revise,
                "bootstyle" : "warning-outline",
            },
        ]
        def revise(event=None,self=self,*args, **kwargs):
            click_revise(self=self, *args, **kwargs)
            self.master.bind("<Return>", revise)
        for widget in entry_or_label_config:
            if "textvariable" in widget:
                entry = ttk.Entry(self.home_win.frame1,
                        textvariable=widget["textvariable"],
                        font=font,
                        width=30,
                        show="*",)
                entry.grid(row=widget["row"], column=widget["column"], padx=10,columnspan=2)
                self.entry_list.append(entry)
            else:
                ttk.Label(self.home_win.frame1,
                        text=widget["text"],
                        font=font,
                        ).grid(row=widget["row"], column=widget["column"], padx=10)
        for widget in btn_config:
            btn = ttk.Button(self.home_win.frame1,
                             bootstyle=widget["bootstyle"],
                             text=widget["text"],)
            btn.grid(row=widget["row"], column=widget["column"], padx=10, pady=10, ipadx=10, ipady=10)
            btn.bind("<Button-1>", lambda event,b=btn,w=widget,s=self: w["command"](btn=b,self=s))

        self.button_return(row=3,column=3)

        self.master.bind("<Return>",revise)

    def message(self,master = None, title="提示",text="",button_text="确定",*args, **kwargs):
        if master == None:
            master = self.master
        self.master.unbind("<Return>")
        info = Messagebox(master=master,
                   title=title,
                   text=text,
                   button_text=button_text,
                   *args, **kwargs
                   )
        return info
    def get_handoff(self):
        """
        返回登录窗口
        :return:
        """
        self.home_win.destroy()
        login.Login(self.master)

    def window_destroy(self):
        """
        进入模块窗口时销毁frame1中的组件
        :return:
        """
        for widget in self.home_win.frame1.winfo_children():
            widget.destroy()

    def click_return(self, *args, **kwargs):
        """
        点击返回按钮,返回home窗口
        :param args:
        :param kwargs:
        :return:
        """
        self.window_destroy()
        self.home_win.create_framewidgets()
    def button_return(self,row = 3,column = 4,sticky="es"):
        """
        返回按钮
        :return:
        """
        btn = ttk.Button(self.home_win.frame1,
                          bootstyle="info-outline",
                          text="返回",
                          command=self.click_return,
                          )
        btn.grid(row=row, column=column, padx=30, pady=30, ipadx=10, ipady=10,sticky=sticky)
        return btn

if __name__ == '__main__':
    import messagebox
    messagebox.test()