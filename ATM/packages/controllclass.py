import re,random,pickle,getpass,os
from packages import cardclass as card
from packages import personclass as person

# from cardclass import Card


class Controller():
    def __init__(self):
        #数据存储格式
        self.userid_cardid = {} #{身份证id:银行卡id}
        self.cardid_userobj = {} #{银行卡id:用户对象}
        
        #数据存储url
        self.userid_cardid_url = "./databases/userid.txt"
        self.cardid_userobj_url = "./databases/bankid.txt"
        
        
        # 加载所有的数据信息
        self.load_data()
        
    def load_data(self):
        # 检测文件是否存在
        if os.path.exists(self.cardid_userobj_url):
            #读取数据
            with open(self.cardid_userobj_url, "rb") as f:
                self.cardid_userobj = pickle.load(f)  #将数据反序列化给{银行卡id:用户对象}
                # print(f"self.cardid_userobj: {self.cardid_userobj}")
        if os.path.exists(self.userid_cardid_url):
            with open(self.userid_cardid_url, "rb") as fl:
                self.userid_cardid = pickle.load(fl)
                # print(f"self.userid_cardid: {self.userid_cardid}")


        
# 1. 注册 ：regiser
    def register(self):
        
        # 获取用户输入的用户名,身份证号,手机号,密码
        while True:
            name = self.__getusername()
            phone = self.__getphone()
            userid = self.__getuserid()
            if not userid:
                pause()
                break
            pwd = self.__getpwd()
            str = f'''创建用户成功:
            用户名:{name}
            身份证:{userid}
            手机号:{phone}'''
            print(str)
            checkinput = input("请检测输入信息,正确请输入y:(y/n)")
            if checkinput != "y":
                print("请重新输入信息")
                continue
        
            print("用户创建成功...")
            #给用户创建银行卡
            cardid = self.__generate_cardid()
            if not cardid:
                pause()
                break
            cardobj = card.Card(cardid, pwd)
            print('银行卡创建成功')
        
            #创建用户对象,与银行卡进行绑定
            userobj = person.Person(name,userid,phone,cardobj)
        
            #保存用户的信息
            self.userid_cardid[userid] = cardid
            self.cardid_userobj[cardid] = userobj
            print(self.userid_cardid)
            print(self.cardid_userobj)
            print(f'恭喜用户{name}开户成功,卡号为{cardid},余额为{cardobj.money}元')
            pause()
            break

# 2. 查询：query
    def query(self):
        # 获取用户输入的卡号
        cardid = self.__check_cardid(prompt='请输入要查询的卡号:')
        if not cardid: 
            return
        cardobj = self.cardid_userobj[int(cardid)].card
        # 存在,则验证密码
        if self.__checkpwd(cardid):
            print("查询成功")
            print(f"持卡人: {self.cardid_userobj[cardobj.card_id].name}\n卡号: {cardobj.card_id}\n余额: {cardobj.money}")
            pause()
            return
            
        
# 3. 存款：add_money
    def add_money(self):
        while True:
            cardid = input("请输入要存款的卡号(按q返回上一层)：").strip()
            if cardid == "q":
                return
            valid_cardid = lambda x: not x.isdigit()
            if valid_cardid(cardid):
                print("请输入正确的卡号")
                pause()
                continue
            # 1. 验证卡号是否存在
            if int(cardid) not in self.cardid_userobj:
                print("卡号不存在，请重新输入")
                pause()
                continue
            # 2. 验证卡是否锁定
            cardobj = self.cardid_userobj[int(cardid)].card
            if cardobj.islocked: #验证是否锁卡
                print("卡已锁定,请解卡后再使用")
                pause()
                return
            # 3. 再次确定卡号是否正确
            print(f"请再次确定你输入的卡号")
            reinfo = input(f"卡号 {cardid} 是否正确(y/n):").strip()
            if reinfo != "y":
                return
            # 4.存款
            while True:
                money = get_input("请输入存款金额：",validation_func=lambda x:not x.isdigit(),error_message2="请输入正确的金额")
                cardobj.money += int(money)
                print(f"存款成功，卡号为 {cardobj.card_id} 的余额为：{cardobj.money} 元")
                remoney = input("是否继续存款?(y/n):")
                if remoney == "y":
                    continue
                pause()
                return

    
# 4. 取款：get_money
    def get_money(self):
        cardid = self.__check_cardid(prompt='请输入要取款的卡号(按q返回):')
        if not cardid: 
            return
          
        #验证密码取款
        if self.__checkpwd(cardid):
            cardobj = self.cardid_userobj[int(cardid)].card
            print(f"欢迎用户 {self.cardid_userobj[int(cardid)].name}, 你账户余额为 {cardobj.money} 元")
            while True:
                money = input("请输入取款金额(按q返回上一层)：").strip()
                if money == "q":
                    return
                valid_money = lambda x: not x.isdigit()
                if valid_money(money) or int(money) > cardobj.money:
                    print("请输入正确的金额")
                    pause()
                    continue
                
                cardobj.money -= int(money)
                print(f"取款成功，卡号为 {cardobj.card_id} 的余额为：{cardobj.money} 元")
                pause()
                remoney = input("是否继续取款?输入y继续(y/n):")
                if remoney == "y":
                    continue
                return


# 5. 转帐：trans_money
    def trans_money(self):
        # 1. 验证卡号是否合法
        cardid = self.__check_cardid("请输入你的卡号:")
        if not cardid: 
            return        
        #1.1.验证密码
        if self.__checkpwd(cardid):
            cardobj = self.cardid_userobj[int(cardid)].card
            print(f"欢迎用户 {self.cardid_userobj[int(cardid)].name}, 你账户余额为 {cardobj.money} 元")
        #2.输入别人的卡号
        other_cardid = self.__check_cardid("请输入要转账的卡号:", "对方银行卡已锁定,不能进行转账!")
        if not other_cardid:
            return
        #3.输入转帐金额
        while True:
            money = input("请输入转账金额(按q返回上一层)：").strip()
            if money == "q":
                return
            valid_money = lambda x: not x.isdigit() or int(x) > cardobj.money
            if valid_money(money):
                print("请输入正确的金额")
                pause()
                continue
            cardobj.money -= int(money)  # 自己的卡余额减少
            self.cardid_userobj[int(other_cardid)].card.money += int(money)  # 对方的卡余额增加
            print(f"转账成功,卡号为 {cardobj.card_id} 的余额为：{cardobj.money} 元")
            pause()
            remoney = input("是否继续转账?输入y继续(y/n):")
            if remoney == "y":
                    continue
            return


# 6. 解/锁卡：lock 
    def lock_or_unlock(self): 
        while True:
            print("1. 锁卡  2. 解卡")
            userchoice = input("请输入你的选择(按q返回主页):").strip()
            if userchoice == "q":
                return
            if userchoice == "1":
                # 锁卡：lock
                while True:
                    print("1. 使用身份证  2. 使用卡号密码(按q返回上一层)")
                    userchoice2 = input("请输入你的选择:").strip()
                    if userchoice2 == "q":
                        break
                    if userchoice2 == "1":
                        #使用身份证锁卡
                        cardobj = self.__check_userid()
                        if not cardobj: #cardobj为False表明银行卡已经被锁或者用户返回上一级
                            continue
                        reconfirm = input("确定锁卡吗?(y/n):")
                        if reconfirm == "y":
                            cardobj.islocked = True #锁卡
                            print("锁卡成功")
                            pause()
                        return
                    elif userchoice2 == "2":
                        cardid = self.__check_cardid("请输入你的卡号:")
                        if not cardid:
                            return
                        #1.1.验证密码
                        if self.__checkpwd(cardid):
                            #1.2. 锁卡
                            reconfirm = input("确定锁卡吗?(y/n):")
                            if reconfirm == "y":
                                cardobj.islocked = True #锁卡
                                print("锁卡成功")
                                pause()
                            return
            elif userchoice == "2":
                # 解卡：unlock
                while True:
                    cardobj = self.__check_userid(prompt2="",arg = True,prompt3="银行卡未锁定,不能进行解卡操作!") 
                    #False(返回上一层), True(锁了), cardobjobj(没锁)
                    if cardobj == False:
                        return
                    elif cardobj == True:
                        print("解卡成功")
                        pause()
                        return
                    

# 7. 补卡：new_card
    def new_card(self):
        while True:
            cardobj = self.__check_userid(prompt2 = "该银行卡已锁定,请解卡后补卡!")
            if cardobj == False:
                return
            newcardid = self.__generate_cardid() #重新生成卡号
            if not newcardid:
                return
            cardobj.card_id = newcardid
            print(f"补卡成功，新卡号为：{cardobj.card_id}")
            pwd = self.__getpwd()
            cardobj.password = pwd
            print("密码更新成功")
            pause()
            return

# 8. 改密：change_pwd
    def change_pwd(self):
        while True:
            print("1. 身份证  2. 密码")
            userchoice = input("请输入你的选择(按q退出):").strip()
            if userchoice == "q":
                return
            if userchoice == "1":
                cardobj = self.__check_userid()
                if not cardobj:
                    continue
                cardobj.password = self.__getpwd()
                print("密码更新成功")
                pause()
                return 
            elif userchoice == "2":
                cardid = self.__check_cardid()
                if not cardid: 
                    continue
                if self.__checkpwd(cardid):
                    pwd = self.__getpwd("请输入新的密码:")
                    self.cardid_userobj[int(cardid)].card.password = pwd
                    print("密码更新成功")
                    pause()
                    return
            else:
                print("请输入正确的选项")
            
            
            
            
# 9. 销户: close_account
    def close_account(self):
        while True:
            cardobj = self.__check_userid(prompt2 = "该银行卡已锁定,请解卡后销户!")
            if cardobj == False:
                return
            print(f"尊敬的 {self.cardid_userobj[cardobj.card_id].userid} 用户,当前银行卡余额还有 {cardobj.money} 元")
            reconfirm = input("确定销户吗?(y/n):")
            if reconfirm == "y":
                del self.userid_cardid[self.cardid_userobj[cardobj.card_id].userid]
                del self.cardid_userobj[cardobj.card_id]
                print("销户成功")
                pause()
                return
            else:
                print("销户失败")
                pause()
                return 
            
# 10. 退出： save
    def save(self):
        #把当前数据写入到文件中
        with open(self.userid_cardid_url,"wb+") as fp:
            pickle.dump(self.userid_cardid,fp)
        with open(self.cardid_userobj_url,"wb+") as fp:
            pickle.dump(self.cardid_userobj,fp)

        print("退出")
        exit()
        
#------------------------------------------------------------------------    
    def __getusername(self):
        # 获取用户名输入的名字
        return get_input("请输入用户名：", error_message="用户名不能为空")

    def __getuserid(self):
        # 获取用户身份证id
        return get_input("请输入身份证id：", validation_func = lambda x: x in self.userid_cardid, error_message="用户id不能为空")

    def __getphone(self):
        # 获取手机号
        # return get_input("请输入手机号：", validation_func=lambda x: re.match(r'^1\d{10}$', x), error_message="请输入正确的手机号")
        return get_input("请输入手机号：", error_message="请输入正确的手机号")

    def __getpwd(self,prompt = "请输入密码："):
        # 获取密码
        return get_password(prompt, error_message="密码不能为空")
    
    def __checkpwd(self, cardid):
        cardobj = self.cardid_userobj[int(cardid)].card
        num = 2
        #检测密码是否正确
        while True:
            password = getpass.getpass("请输入密码：").strip() #获取密码
            if password == cardobj.password: #判断密码是否正确
                return True
            else:
                if num == 0 :
                    #锁卡
                    cardobj.islocked = True
                    print("密码错误次数过多，账户已锁定")
                    pause()
                    break
                num -= 1
                print(f"密码错误，还有{num + 1}次机会重新输入")

    #检查卡号
    def __check_cardid(self,prompt = "请输入要存款的卡号(按q返回上一层)：", prompt2 = "卡已锁定,请解卡后再使用"): 
        while True:
            cardid = input(prompt).strip()
            if cardid == "q":
                return False

            valid_cardid = lambda x: x.isdigit()
            if not valid_cardid(cardid):
                print("请输入正确的卡号")
                continue
            # 验证卡号是否存在
            if int(cardid) not in self.cardid_userobj:
                print("卡号不存在，请重新输入")
                continue
            #验证卡号是否锁定
            cardobj = self.cardid_userobj[int(cardid)].card
            if cardobj.islocked:
                print(prompt2)
                pause()
                return False
            print("卡号验证通过")
            return cardid
    
    #检测身份证 
    def __check_userid(self,prompt = "请输入你的身份证卡号(按q返回上一层)：", prompt2 = "该银行卡已锁定,无需再次锁定!", arg = False,prompt3 = "银行卡验证通过"): 
        while True:
            userid = input(prompt).strip()
            if userid == "q":
                return False
            valid_cardid = lambda x: x.isdigit()
            if not valid_cardid(userid):
                print("请输入正确的身份证号")
                pause()
                continue
            # 验证身份证是否存在
            if userid not in self.userid_cardid:
                print("身份证不存在，请重新输入")
                pause()
                continue
            #验证身份证号的银行卡是否锁定
            cardid = self.userid_cardid[userid]
            cardobj = self.cardid_userobj[cardid].card
            if cardobj.islocked:
                print(prompt2,end="")
                pause()
                if arg:
                    reconfirm = input("确定解卡吗?(y/n):")
                    if reconfirm == "y":
                        cardobj.islocked = False
                        return True
                    return
                return False
            else:
                print(prompt3)
            return cardobj
        
    def __generate_cardid(self,Max = 9):
        while True:
            sorted_keys = sorted(self.cardid_userobj.keys())
            if sorted_keys[-1] == Max and sorted_keys[0] == 1:
                print("银行卡序号已满，请联系工作人员")
                pause()
                return False

            # cardid = random.randint(100000,999999)
            cardid = sorted_keys[-1] + 1
            if cardid not in self.cardid_userobj:
                return cardid

        
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
def get_input(prompt, validation_func = None, error_message="输入不能为空", error_message2='身份证号不能重复注册'):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print(error_message)
            continue
        if validation_func and  validation_func(user_input):
            print(error_message2)
            return False
        return user_input

def get_password(prompt, error_message="密码不能为空"):
        while True:
            pwd = getpass.getpass(prompt).strip()
            if not pwd:
                print(error_message)
                continue
            repwd = getpass.getpass("请再次输入密码：").strip()
            if repwd != pwd:
                print("两次密码不一致，请重新输入")
                continue
            return pwd
def pause():
    input("按回车键继续...")
    


if __name__ == '__main__':
    obj = Controller()
    obj.register()