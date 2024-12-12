from packages.viewclass import Views
from packages.controllclass import Controller
# from packages.cardclass import Card
# from packages.personclass import Person
import time
class Main():
    def __init__(self):
        #实例化视图对象
        view = Views()
        #实例化控制类
        control = Controller()
        
        choiceNum = {
            '1': control.register,
            '2': control.query,
            '3': control.add_money,
            '4': control.get_money,
            '5': control.trans_money,
            '6': control.lock_or_unlock,
            '7': control.new_card,
            '8': control.change_pwd,
            '9': control.close_account,
            '0': control.save
        }
        while True:
            value = input("请输入操作序号:")
            #验证用户输入是否正确
            if value in choiceNum:
                choiceNum[value]()
                view.show_operation()
            else :
                print("输入有误，请重新输入")

if __name__ == '__main__':
    Main()