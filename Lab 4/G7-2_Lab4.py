import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class Property:
    def __init__(self,type,dic): 
        super().__init__(type,dic)        
        self.dictionary = dic
        self.type = type  
        self.square_meter = self.dictionary["square_meter"]
        self.num_bedrooms = self.dictionary["num_bedrooms"]
        self.num_bathrooms = self.dictionary["num_bathrooms"]

    def display(self,type,dic): 
        cls()
        self.dictionary = dic 
            
        print("Insert property for agent.\n")
        print("Name : [",self.dictionary["name"],"]","\nType : ",type[1])
        print("\n Square(Meter) : ",self.dictionary["square_meter"],"\n Bedrooms      : ",self.dictionary["num_bedrooms"],"\n Bathrooms     : ",self.dictionary["num_bathrooms"])      
        if type[0] == 'house':
            print(" Garage        : ",self.dictionary["garage"] ,"\n Fenced Yard   : ",self.dictionary["fenced_yard"])         
        elif type[0] == "apartment":
            print(" Balcony       : ",self.dictionary["balcony"],"\n Laundry       : ",self.dictionary["laundry"])  
    def promt_init(self,list_,type):   
       
        lists = ["name","square_meter","num_bedrooms","num_bathrooms"]
        lists.extend(list_)
        op = { i : "" for i in lists }        
        self.dictionary = op
        for key in lists:
            self.display(type,self.dictionary)      
            print("\nInsert [",key,"]",sep='')
            inputs = input("  Input : ")
            self.dictionary[key] = inputs 
            
        return self.dictionary
        
class Apartment(Property):
    def __init__(self,type,dic):
        lists = ['balcony','laundry']  
        self.apartment = self.promt_init(lists,type)      
        dic = self.apartment
        super().__init__(type,dic)
        self.balcony = self.dictionary["balcony"]
        self.laundry = self.dictionary["laundry"] 

class House(Property):
    def __init__(self,type,dic):       
        lists = ['garage','fenced_yard']      
        self.house = self.promt_init(lists,type)      
        dic = self.house
        super().__init__(type,dic)
        self.garage = dic["garage"] #ที่จอดรถ บอกว่ามีที่จอดรถได้กี่คัน 
        self.fenced_yard = dic["fenced_yard"] #รั้ว บอกว่ามีรั้วหรือไม่ (บ้านฝรั่งบางทีไม่มีรั้ว)    
        

class Rent:
    def __init__(self,type,dic):
        super().__init__()             
        dic.update({'furnished':'','rent':''} )   
        self.furnished = self.dictionary['furnished'] #ตกแต่งพร้อมอยู่หรือไม
        self.rent =self.dictionary['rent'] # ค่าเช่าต่อเดือน    
    def display(self):
        cls()
        self.display(self.type,self.dictionary)
        print(" \n Furnished     : ",self.dictionary['furnished'],"\n Rent          : ",self.dictionary['rent'])         
    def promt_init(self,type,dic):

        #House.promt_init(self,dic,type)
        if len(type) == 3:
            lists = dic
        else:
            lists = ['furnished','rent'] 
        for key in lists: 
            Rent.display(self)
            print("\nInsert [",key,"]",sep='')
            inputs = input("  Input : ")
            dic[key] = inputs 
            
            

class Purchase:
    def __init__(self,type,dic):
        super().__init__()             
        dic.update({'price':'','taxes':''} )   
        self.price = self.dictionary['price'] #ตกแต่งพร้อมอยู่หรือไม
        self.taxes =self.dictionary['taxes'] # ค่าเช่าต่อเดือน    
    def display(self):
        cls()
        self.display(self.type,self.dictionary)
        print(" \n Price         : ",self.dictionary['price'],"\n Taxes         : ",self.dictionary['taxes'])         
    def promt_init(self,type,dic):

        if len(type) == 3:
            lists = dic
        else:
            lists = ['price','taxes'] 
        for key in lists: 
            Purchase.display(self)
            print("\nInsert [",key,"]",sep='')
            inputs = input("  Input : ")
            dic[key] = inputs 

class HouseRental(House,Rent):
    def __init__(self,dic,type,controller):           
        if controller == "add":                   
            House.__init__(self,type,dic)
            self.own = self.house
            Rent.promt_init(self,type,self.own)         
        elif controller == "show":           
            self.dictionary = dic   
            self.type = type
            Rent.display(self)
        elif controller == "edit":
            self.dictionary = dic   
            self.type = type
            Rent.promt_init(self,type,dic)
            
class HousePurchase(House,Purchase):
    def __init__(self,dic,type,controller):           
        if controller == "add":                   
            House.__init__(self,type,dic)
            self.own = self.house
            Purchase.promt_init(self,type,self.own)         
        elif controller == "show":           
            self.dictionary = dic   
            self.type = type
            Purchase.display(self) 
        elif controller == "edit":
            self.dictionary = dic   
            self.type = type
            Purchase.promt_init(self,type,dic)
        elif controller == "edit":
            self.dictionary = dic   
            self.type = type
            Purchase.promt_init(self,type,dic)


class ApartmentRental(Apartment,Rent):
    def __init__(self,dic,type,controller):           
        if controller == "add":                   
            Apartment.__init__(self,type,dic)
            self.own = self.apartment
            Rent.promt_init(self,type,self.own)         
        elif controller == "show":           
            self.dictionary = dic   
            self.type = type
            Rent.display(self)   
        elif controller == "edit":
            self.dictionary = dic   
            self.type = type
            Rent.promt_init(self,type,dic)

class ApartmentPurchase(Apartment,Purchase):
    def __init__(self,dic,type,controller):           
        if controller == "add":                   
            Apartment.__init__(self,type,dic)
            self.own = self.apartment
            Purchase.promt_init(self,type,self.own)         
        elif controller == "show":           
            self.dictionary = dic   
            self.type = type
            Purchase.display(self) 
        elif controller == "edit":
            self.dictionary = dic   
            self.type = type
            Purchase.promt_init(self,type,dic)
        

class Agent:
    def __init__(self,dic):
        self.dic = dic
        self.type_map = { 
            ("house", "rental"): HouseRental,
            ("house", "purchase"): HousePurchase,
            ("apartment", "rental"): ApartmentRental,
            ("apartment", "purchase"): ApartmentPurchase
                   }  
    def property_list(self,show_all):              

        if show_all == {}:
            print("\n!!You don't have an asset yet, please add it with the add command.")
        else:
            num = 0
            for key in show_all.keys():        
                show = show_all[key]           
                print(' [',num,'] : ',"  Name ",key[0],"(",key[1],")  __",show["name"],"__",sep='')    
                num += 1  
    def add_property(self,property_type,purchase_type):
        select = tuple([property_type,purchase_type])            
              
        dict = self.type_map[select]({},select,"add")   
        self.dic.update({(tuple([property_type,purchase_type,dict.own['name']])):dict.own})      
        return self.dic
    
    


              
    def list_property(self,agent_own,inputs,menu,show_all=False):
        lists = [] 
        for num in agent_own.keys():
            lists.append(num)
        if inputs >= len(lists):   
            pass
        else:   
            cls()   
            type_map = { 
            ("house", "rental",str(lists[inputs][2])): HouseRental,
            ("house", "purchase",str(lists[inputs][2])): HousePurchase,
            ("apartment", "rental",str(lists[inputs][2])): ApartmentRental,
            ("apartment", "purchase",str(lists[inputs][2])): ApartmentPurchase
            }  
            
            type_map[lists[inputs]](agent_own[lists[inputs]],lists[inputs],"show")
            choice = menu()
            if choice == "return":
                pass
            elif choice == 'delect':
             
                agent_own.pop(lists[inputs])
            elif choice == 'edit':
                type_map[lists[inputs]](agent_own[lists[inputs]],lists[inputs],"edit")

                  
            else:
                self.list_property(agent_own,inputs,menu)
            
class Menu():
    def __init__(self):
        pass
    def menu(self):
        print("\n\n[add]        [exit]")
        choice = input("\nYour choice : ")
        return choice

    def sub_menu(self):
        print("\n[return]        [exit]")
        choice = input("\nYour choice : ")
        return choice

    def config_menu(self):
        print("\n[return]    [edit]    [delect]")
        choice = input("\nYour choice : ")
        return choice

    def confirm_menu(self):
        print("\n[confirm]        [cancel]")
        choice = input("\nYour choice : ")
        return choice
        

class Main():
    def __init__(self) -> None:
        
        self.agent_own = {}
        self.now = ""
        self.before = self.index
        self.add_select = []
        self.agent = Agent(self.agent_own)
        self.menu = Menu()
    def exit(self):
        cls()
        print("Do you want to exit? \n\n [1] correct.\n [2] return.")
        i = input("\nYour choice : ")
        if i == "1" or i == "correct":
            cls()
            exit()
        elif i == "2" or i == "return":
            
            self.now()
        else:
            self.exit()

    def index(self):
        cls()
        self.add_select = []
        self.now = self.index
        print("Welcome to programe agent.\n")   
        self.agent.property_list(self.agent_own)      
        choice = self.menu.menu()
        self.controller(choice)
    
    def add_page(self):  
        cls()   
        if self.add_select == []:
            self.now = self.add_page 
            self.before = self.index
            print("Menu add property for programe agent. \n\n[1] House \n[2] Apartment     \n ") 
            choice = self.menu.sub_menu()    
            self.controller(choice)
                       
        elif self.add_select != [] :
            cls()
            self.before = self.add_page        
            print("Menu add property for programe agent. \n\n[1] Rent \n[2] Purchase  \n")
            choice = self.menu.sub_menu()    
           
            self.controller(choice)

    def controller(self,inputs):
        if inputs == "add":
            self.add_page()        
        elif inputs == "use":
           self.agent.list_property()
        elif inputs == "exit":
            self.exit()          
        elif inputs == "return":
            self.add_select = []
            self.before()
        elif inputs == "":
            self.now()    

        if self.now == self.index: #       
            if(inputs.isnumeric()):
                self.agent.list_property(self.agent_own,int(inputs),self.menu.config_menu)
                
                self.now()

        if self.now == self.add_page:#
            if self.add_select == []:
                if inputs == "1" or inputs == "house":
                    self.add_select.append("house")
                    self.add_page()
                elif inputs == "2" or input == "apartment":
                    self.add_select.append("apartment")
                    self.add_page()
                else :
                    self.now()
            elif self.add_select != []:
                if inputs == "1" or inputs == "rent":
                    self.add_select.append("rental")
                    self.agent_own = self.agent.add_property(self.add_select[0],self.add_select[1])
                    self.now = self.index
                elif inputs == "2" or input == "purchase":
                    self.add_select.append("purchase")
                    self.agent_own = self.agent.add_property(self.add_select[0],self.add_select[1])
                    self.now = self.index
                else :
                    self.now()
            elif inputs == "return" and self.before == self.add_page:
                self.before()
              
        else :
            self.now()  
        
show = Main()

while True:
    show.index()


