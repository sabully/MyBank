class Card():
    '''
    卡号,密码,余额,是否锁卡
    '''
    card_id = None
    password = None
    money = None
    islocked = None
    
    def __init__(self,card_id,password,money = 10,islocked = False):
        self.card_id = card_id #卡号
        self.password = password #密码
        self.money = money #余额
        self.islocked = islocked #是否锁卡,False为没有锁卡,True为锁卡

if __name__ == '__main__':
    card = Card('1',123456)
    # print(card)
