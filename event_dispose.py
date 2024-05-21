import re
from data import data_path, write_data, read_data


def withdraw_or_deposit(self, amount, mode="deposit"):
    if mode == "deposit":
        title = "存款"
        text = "存入"
    else:
        title = "取款"
        text = "取出"
    if amount == "other":
        get_input = self.message(title=title,
                                 text="",
                                 button_text="确定",
                                 button_text2="取消",
                                 mode="write",
                                 text_color="white",
                                 )
        get_input = get_input()  # 调用__call__方法，返回用户输入的金额
        if get_input:
            if re.match(r"^\d+$", get_input):
                get_input = int(get_input)
                if mode == "deposit":
                    choose = self.message(title=title,
                                          text=f"确认是否{text}{get_input}元",
                                          button_text="确定",
                                          button_text2="取消", )
                    if not choose():
                        return
                    self.user["balance"].values[0] = self.user["balance"].values[0] + get_input
                    self.message(title=title,
                                 progressbar=True,
                                 progressbar_text=title)
                    if write_data(data_path, self.user):
                        self.message(title=title,
                                     text=f"{text}{get_input}元成功",
                                     button_text="确定",
                                     )
                    else:
                        self.message(title=title,
                                     text=f"{text}失败",
                                     button_text="确定",
                                     )
                        self.user["balance"].values[0] = self.user["balance"].values[0] - get_input
                else:
                    if self.user["balance"].values[0] >= get_input:
                        choose = self.message(title=title,
                                              text=f"确认是否{text}{get_input}元",
                                              button_text="确定",
                                              button_text2="取消", )
                        if not choose():
                            return
                        self.user["balance"].values[0] = self.user["balance"].values[0] - get_input
                        self.message(title=title,
                                     progressbar=True,
                                     progressbar_text=title)
                        if write_data(data_path, self.user):
                            self.message(title=title,
                                         text=f"{text}{get_input}元成功",
                                         button_text="确定",
                                         )
                        else:
                            self.message(title=title,
                                         text=f"{text}失败",
                                         button_text="确定",
                                         )
                            self.user["balance"].values[0] = self.user["balance"].values[0] + get_input
                    else:
                        self.message(title=title,
                                     text="余额不足",
                                     button_text="确定",
                                     )
            else:
                self.message(title=title,
                             text=f"{text}金额必须为正整数",
                             button_text="确定",
                             )
    else:
        choose = self.message(title=title,
                              text=f"确认是否{text}{amount}元",
                              button_text="确定",
                              button_text2="取消", )
        if not choose():
            return
        amount = int(amount)
        if mode == "deposit":
            self.user["balance"].values[0] = self.user["balance"].values[0] + amount
            if not self.message(title=title,
                                progressbar=True,
                                progressbar_text=title)():
                return
            if write_data(data_path, self.user):
                self.message(title=title,
                             text=f"{text}{amount}元成功",
                             button_text="确定",
                             )
        else:
            if self.user["balance"].values[0] >= amount:
                self.user["balance"].values[0] = self.user["balance"].values[0] - amount
                if not self.message(title=title,
                                    progressbar=True,
                                    progressbar_text=title)():
                    return
                if write_data(data_path, self.user):
                    self.message(title=title,
                                 text=f"{text}{amount}元成功",
                                 button_text="确定",
                                 )
            else:
                self.message(title=title,
                             text="余额不足",
                             button_text="确定",
                             )


def transfer(self, other_account, amount, password):
    users_info = read_data(data_path)
    other_user = users_info[users_info["account"] == other_account]
    if other_user.empty:
        self.message(text="对方账户不存在")
        return
    if other_account == self.user["account"].values[0]:
        self.message(text="不能给自己转账")
        return
    choose = self.message(text=f"确认向{other_user['name'].values[0]}转账{amount}元",
                          button_text="确认",
                          button_text2="取消", )
    if choose():
        if self.user["password"].values[0] == password:
            if re.match(r"^\d+$", amount):
                if self.user["balance"].values[0] >= int(amount):
                    self.user["balance"].values[0] = self.user["balance"].values[0] - int(amount)
                    other_user["balance"].values[0] = other_user["balance"].values[0] + int(amount)
                    if self.message(title="转账",
                                    progressbar=True,
                                    progressbar_text="转账")():
                        if write_data(data_path, (self.user, other_user)):
                            self.message(title="转账",
                                         text="转账成功",
                                         button_text="确定",
                                         )
                        else:
                            self.message(title="转账",
                                         text="转账失败",
                                         button_text="确定",
                                         )
                else:
                    self.message(text="余额不足")
                    return
            else:
                self.message(text="金额必须为正整数")
        else:
            self.message(text="密码错误")


def displayPassword(btn=None, self=None, *args, **kwargs):
    if self.password_show_status:
        for entry in self.entry_list:
            entry.config(show="*")
        self.password_show_status = False
        btn.config(text="显示密码")
    else:
        for entry in self.entry_list:
            entry.config(show="")
        self.password_show_status = True
        btn.config(text="隐藏密码")


def click_revise(self=None, *args, **kwargs):
    # 使用re判断old_password，new_password1，new_password2都为纯数字
    if (
            re.match(r"^\d+$", self.old_password.get())
            and re.match(r"^\d+$", self.new_password1.get())
            and re.match(r"^\d+$", self.new_password1.get())
    ):
        if self.new_password1.get() == self.new_password2.get():
            if len(self.new_password1.get()) < 6 or len(self.new_password2.get()) < 6:
                self.message(title="错误", text="密码长度不能小于6位", )
            elif self.old_password.get() == self.new_password1.get():
                self.message(title="错误", text="新密码不能与旧密码相同", )
            # 修改密码
            elif self.old_password.get() == self.user["password"].values[0]:
                self.user["password"].values[0] = self.new_password1.get()
                if write_data(data_path, self.user):
                    self.message(title="成功", text="修改成功\n请重新登陆", text_color="green", )
                    # 修改成功后让用户重新登录
                    self.get_handoff()
            else:
                self.message(title="错误", text="密码错误", )
        else:
            self.message(title="错误", text="密码不一致", )
    else:
        self.message(title="错误", text="密码只能为纯数字", )
