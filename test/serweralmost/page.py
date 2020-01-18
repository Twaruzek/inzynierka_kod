class page:
    pages = {       
        0  : {'name' : 'index'         , 'number': 0},
        1  : {'name' : 'control'       , 'number': 1},
        2  : {'name' : 'characteristic', 'number': 2},
        3  : {'name' : 'reg'           , 'number': 3},
        4  : {'name' : 'log'           , 'number': 4},
        5  : {'name' : 'assumptions'   , 'number': 5}
        }
    active = []
        
    def __init__(self,page):
        for i in self.pages:
            if page == self.pages[i]['name']:
                self.active_page(self.pages[i]['number'])
    
    def active_page(x):
        x=int(x)
        for i in range(len(self.pages)):
            if i == x :
                self.active[i] = "active"
            else:
                self.active[i] = ""
        return self.active