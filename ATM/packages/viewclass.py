import time
class Views():
    
    def __init__(self):
        self.show_welcome()
        self.show_operation()
    
    #显示欢迎界面
    def show_welcome(self):
        strx = "*" * 47 + '\n'
        varstr = '''*                                             *\n*               欢迎使用ATM v1.0              * 
*                                             *       
'''
        varstr = strx + varstr
        print(varstr,end='')
    
    # 显示操作界面
    def show_operation(self):
        strx = "*" * 47 + '\n'
        varstr = '''*                                             *\n*            1️⃣  注册    2️⃣  查询               *
*                                             *
*            3️⃣  存款    4️⃣  取款               * 
*                                             *
*            5️⃣  转账    6️⃣  解/锁卡            *
*                                             *
*            7️⃣  补卡    8️⃣  改密               *
*                                             *
*            9️⃣  注销    0️⃣  退出               *
*                                             *
***********************************************'''
        print(strx + varstr)
if __name__ == '__main__':
    obj = Views()
