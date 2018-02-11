# -*- coding: utf-8 -*-
# @Time    : 2017/11/23 9:43
# @Author  : ZTS
# @Software: PyCharm

from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import ImageTk

import random

class Layout(Frame):
    # 获取输入的人数
    run_flag = False
    str_num = 0
    words = []
    undercover = ''
    civilian = ''
    show_word_count = 0
    show_undercover = 0
    player_num = 0
    # 查看词语和描述匹配
    view_macth = 0
    desscribe_macth = 0
    v = ''
    v1 = ''
    player_remain = 1
    vote_result = []
    player_list = []
    name = ''
    vote_count = []
    players_dict = {}
    myundercover = 0
    count_start = 1
    click_count = 0
    get_values = []
    re_describe = False
    remove_player = 0
    vote_flag = False
    def __init__(self, master, frame):
        Frame.__init__(self)
        self.frame = frame
        # self.frame = Frame(master, bg="light sea green", width=636, height=530)
        # self.frame.pack_propagate(0)
        # self.frame.pack()
        self.frame2 = Frame(master, bg="light sea green", width=636, height=40)
        self.frame2.pack_propagate(0)
        self.frame2.pack()
        self.frame3 = Frame(master, bg="light sea green", width=636, height=40)
        self.frame3.pack_propagate(0)
        self.frame3.pack()

    def createWidgets(self, words):
        ''' 创建整体的布局 '''
        self.words = words
        # 顶部图片
        # img = ImageTk.PhotoImage(file = "t.jpg")
        # imgLabel = Label(self.frame, image=img, text="谁是卧底", compound=CENTER,)
        # imgLabel.pack(side=TOP)

        # 中间文字规则介绍
        t = StringVar()
        t.set("游戏规则如下：\n1.游戏有卧底和平民 2 种身份(游戏3-5人,本程序卧底一人)。\n2.游戏根据在场人数大部分玩家拿到同一词语，\
其余玩家拿到与之相关的另一词语。\n3.每人每轮用一句话描述自己拿到的词语，既不能让卧底察觉，\
也要给同伴以暗示。\n4.每轮描述完毕，所有在场的人投票选出怀疑谁是卧底，得票最多的人出局。\n5.若卧底\
全部出局，则游戏结束。若卧底未全部出局，游戏继续。\n6.并反复此流程。若卧底撑到最后一轮\
（剩余总人数小于卧底初始人数的二倍时），则卧底获胜，反之，则平民胜利")
        textLabel = Label(self.frame, textvariable=t, justify=LEFT)
        textLabel.pack(anchor=W, padx=10)

        str_n = StringVar()
        # 操作显示
        input_player = Label(self.frame, text="请输入玩家数：", bg="light sea green")
        input_player.pack(side=LEFT, pady=10, padx=10)
        self.input_entry = Entry(self.frame, textvariable=str_n, width=5)
        self.input_entry.pack(side=LEFT, pady=10)

        start_btn = Button(self.frame, text="开始游戏", width=10, command=self.run)
        start_btn.pack(side=RIGHT, padx=10)

        see_word = Button(self.frame2, text="查看词语", width=10, height=1, command=self.show_word)
        see_word.pack(side=LEFT, padx=10)
        see_describe = Button(self.frame2, text="查看描述", width=10, command=self.view_describe)
        see_describe.pack(side=RIGHT, padx=10)
        # describe_ok = Button(self.frame2, text="保存描述", width=10, command=self.save_describe)
        describe_ok = Button(self.frame2, text="保存描述", width=10, command=self.describe_count)
        describe_ok.pack(side=RIGHT, padx=10)

        self.describe_text = Text(self.frame2, width=30, height=2)
        self.describe_text.pack(side=RIGHT)

        describe_label = Label(self.frame2, text="描述你的词语：", bg="light sea green")
        describe_label.pack(side=RIGHT)
        self.name = StringVar()
        self.name.set("选择玩家")
        self.players = ttk.Combobox(self.frame3, textvariable=self.name, width=12)
        self.players["values"] = [""]
        self.players["state"] = "readonly"

        self.players.pack(side=LEFT, padx=10)
        vote_btn = Button(self.frame3, text="投票", width=10, command=self.vote)
        vote_btn.pack(side=LEFT)

        remain_player = Label(self.frame3, text="        剩 余 人 数 ：", bg="light sea green")
        remain_player.pack(side=LEFT)
        self.v = StringVar()
        self.v.set(self.str_num)
        remain_player_entry = Entry(self.frame3, width=10, textvariable=self.v, state="readonly")
        remain_player_entry.pack(side=LEFT)
        over = Button(self.frame3, text="结束游戏", width=10, command=self.game_over)
        over.pack(side=RIGHT, padx=10)

    def run(self):
        self.run_flag = True
        self.get_value()
        for i in range(self.str_num):
            self.player_list.append(i+1)
        self.players["values"]=self.player_list
        self.players_genrate()

    def get_value(self):
        if len(self.input_entry.get()) == 0:
            showinfo('人数', '人数不能为空.')
        else:
            self.str_num = int(self.input_entry.get())
            if self.str_num < 3:
                showwarning('人数', '人数不能少于3人\n请重新输入.')
            if self.str_num > 5:
                showwarning('人数', '人数不能多于5人\n请重新输入.')
            else:
                self.v.set(self.str_num)
                self.input_entry["state"] = "readonly"

    def describe_count(self):
        if self.count_start == 1:
            self.save_describe()
        elif self.count_start != 1:
            print(self.str_num)
            if self.re_describe:
                self.c_describe()
            else:
                self.describe_resave()

    def c_describe(self):
        player_total = len(self.get_values)
        if player_total >= (self.click_count + 1):
            if self.click_count == 0:
                self.player_num = self.get_values[0]
            elif self.click_count == 1:
                self.player_num = self.get_values[1]
            elif self.click_count == 2:
                self.player_num = self.get_values[2]
            elif self.click_count == 3:
                self.player_num = self.get_values[3]
            elif self.click_count == 4:
                self.player_num = self.get_values[4]
            save_describe = self.describe_text.get("0.0", "end")
            if len(save_describe) == 1:
                showwarning('谁是卧底', '描述不能为空.')
            else:
                with open("describe.txt", "a+", encoding='utf-8') as f:
                    f.write(str(self.player_num) + '.' + save_describe)
                self.describe_text.delete(0.0, END)
                showinfo("谁是卧底", "保存成功")
                self.click_count += 1
            if player_total < (self.click_count + 1):
                self.get_values = []
        else:
            showwarning("谁是卧底", "已经描述完毕")

    def describe_resave(self):
        player = []
        for key in self.players_dict:
            player.append(key)
        # self.name.set("选择玩家")
        # self.players["values"] = player
        player_total = len(player)
        if player_total >= (self.click_count + 1):
            if self.click_count == 0:
                self.player_num = player[0]
            elif self.click_count == 1:
                self.player_num = player[1]
            elif self.click_count == 2:
                self.player_num = player[2]
            elif self.click_count == 3:
                self.player_num = player[3]
            save_describe = self.describe_text.get("0.0", "end")
            if len(save_describe) == 1:
                showwarning('谁是卧底', '描述不能为空.')
            else:
                with open("describe.txt", "a+", encoding='utf-8') as f:
                    f.write(str(self.player_num) + '.' + save_describe)
                self.desscribe_macth += 1
                self.describe_text.delete(0.0, END)
                showinfo("谁是卧底", "保存成功")
                self.click_count += 1
            if player_total < (self.click_count + 1):
                self.vote_flag = True
        else:
            showwarning("谁是卧底", "已经描述完毕")


    def update(self):
        return self.str_num

    def show_word(self):
        if self.str_num == None or self.str_num < 3:
            showwarning('谁是卧底', '不满足查看条件，请重新开始.')
        else:
            if self.view_macth == self.desscribe_macth:
                self.undercover = self.words[0]
                self.civilian = self.words[1]
                if self.show_word_count == 0:
                    self.show_undercover = random.randint(1, self.str_num)
                if self.show_word_count < self.str_num:
                    if self.show_word_count+1 == self.show_undercover:
                        showinfo('谁是卧底', '%s' % self.undercover)
                        self.player_num += 1
                        self.view_macth += 1
                        self.myundercover = self.player_num
                        print("卧底:", self.myundercover)
                    else:
                        showinfo('谁是卧底', '%s' % self.civilian)
                        self.player_num += 1
                        self.view_macth += 1
                    self.show_word_count += 1
                else:
                    showwarning('谁是卧底', '词语已经查看完毕.')
            else:
                showwarning("谁是卧底", "上一个词语没有描述\n请先描述.")

    def save_describe(self):
        if self.run_flag:
            if self.view_macth-1 == self.desscribe_macth:
                save_describe = self.describe_text.get("0.0", "end")
                if len(save_describe) == 1:
                    showwarning('谁是卧底', '描述不能为空.')
                else:
                    with open("describe.txt", "a+", encoding='utf-8') as f:
                        f.write(str(self.player_num) + '.' + save_describe)
                    self.desscribe_macth += 1
                    self.describe_text.delete(0.0, END)
                    showinfo("谁是卧底", "保存成功")
                if (self.desscribe_macth+1) == self.str_num:
                     self.vote_flag = True
            else:
                showwarning("谁是卧底", "你还没有查看词语\n请先查看词语再来描述.")
        else:
            showwarning("谁是卧底","还没有开始游戏.")

    def view_describe(self):
        window = Toplevel(self)
        label = Label(window, text="描述的词语")
        label.pack()
        f = open("describe.txt", "r", encoding='utf-8')
        f_content = f.readlines()
        lb = Listbox(window)
        for item in f_content:
            lb.insert(END, item)
        lb.pack()

    def vote(self):
        if self.vote_flag:
            if self.player_remain <= self.str_num:
                showinfo("123", "%s" % self.players.get())
                self.player_remain += 1
                self.get_vote_value(self.players.get())
                if self.player_remain-1 == self.str_num :
                    self.choice_remove()
            else:
                showwarning("谁是卧底", "已经投票完毕.")
        else:
            showwarning("谁是卧底", "还不能投票")

    def get_vote_value(self, vote_value):
        for key in self.players_dict:
            if int(vote_value) == key:
                self.players_dict[key] += 1
        print("start:", self.players_dict)
        print(max(self.players_dict, key=self.players_dict.get))

    def choice_remove(self):
        self.remove_player = max(self.players_dict, key=self.players_dict.get)
        get_value = self.players_dict[self.remove_player]
        key_list = []
        value_list = []
        self.get_values = []
        for key, value in self.players_dict.items():
            key_list.append(key)
            value_list.append(value)
        for i in range(len(key_list)):
            if get_value in value_list:
                get_value_index = value_list.index(get_value)
                self.get_values.append(key_list[get_value_index])
                value_list.remove(value_list[get_value_index])
                key_list.remove(key_list[get_value_index])
            else:
                continue
        print(self.get_values)
        if len(self.get_values) > 1:
            self.re_describe = True
            showinfo('谁是卧底', "%s再次描述" % self.get_values)
            self.name.set("选择玩家")
            self.players["values"] = self.get_values
            self.count_start += 1
            self.player_remain = 1
            self.click_count = 0
        else:
            self.remove_play()

    def remove_play(self):
        self.re_describe = False
        self.players_dict.pop(self.remove_player)
        print("end:", self.players_dict)
        for key in self.players_dict:
            self.players_dict[key] = 0
        print("remian:",self.players_dict)
        showinfo("谁是卧底", "%s号被淘汰"%self.remove_player)
        remainlist = []
        for key in self.players_dict:
            remainlist.append(key)
        print("卧底号：%s, %s"% (self.myundercover, type(self.myundercover)))
        if self.myundercover in remainlist:
            self.str_num = len(remainlist)
            if self.str_num == 2:
                showinfo("谁是卧底", "人数只剩下两人\n卧底胜利!")
                self.game_over()
            else:
                self.count_start += 1
                showinfo("谁是卧底", "剩下的人请再次描述")
                player = []
                for key in self.players_dict:
                    player.append(key)
                self.name.set("选择玩家")
                self.players["values"] = player
                self.player_remain = 1
                self.click_count = 0
            self.v.set(self.str_num)
        else:
            self.show_vector()
            self.game_over()

    def players_genrate(self):
        players_list = []
        for i in range(self.str_num):
            # players_list.append('player_%s' % (i+1))
            players_list.append(i+1)
        self.players_dict = dict.fromkeys(players_list, 0)
        # showinfo("谁是卧底", self.players_dict)
        showinfo("谁是卧底", "游戏开始")

    def show_vector(self):
        showinfo('胜利者', '平民胜利')

    def game_over(self):
        with open("describe.txt", "w", encoding="utf-8") as f:
            f.truncate()
        self.frame3.quit()

class Player(object):
    ''' 玩家 '''
    def __init__(self):
        self.__identify = ['undercover','civilian']
        self.words = None

    def my_word(self, words, num):
        ''' 玩家得到的词语 '''
        print(words)
        random_whonum = random.randint(0,1)
        self.__identify[0] = words[random_whonum]
        print(self.__identify[0])
        for i in words:
            if self.__identify[1] not in words and self.__identify[0] != i:
                self.__identify[1] = i
        print(self.__identify[1])
        return self.__identify

class Umpire(object):
    ''' 裁判 '''
    def __init__(self):
        self.words = None
        self.current_player = None

    def generate_random_words(self):
        ''' 产生随机词语 '''
        total_words = [['钢笔','铅笔'],['月亮','太阳'],['美人痣','青春痘'],['陈奕迅','张学友'],['鸭脖','鸡爪'],['风衣','毛衣']
            , ['苹果', '安卓'],['孟非','乐嘉'],['胡海泉','陈羽凡'],['唇膏','口红'],['最炫名族风','江南style']]
        random_num = random.randint(0,10)
        self.words = total_words[random_num]
        print(self.words)
        return self.words

if __name__ == '__main__':
    root = Tk()
    root.title("谁是卧底")
    frame = Frame(root, bg="light sea green", width=636, height=530)
    frame.pack_propagate(0)
    frame.pack()
    img = ImageTk.PhotoImage(file="wodi2.jpg")
    # imgLabel = Label(frame, image=img, text="谁是卧底", compound=CENTER, )
    imgLabel = Label(frame, image=img)
    imgLabel.pack(side=TOP)
    app = Layout(master=root, frame=frame)
    player = Player()
    umpire = Umpire()
    words = umpire.generate_random_words()
    p = player.my_word(words, app.str_num)
    app.createWidgets(p)
    root.mainloop()