class Catalog:
    def __init__(self):
        self.author_name = []
        self.book_catalog = []
        
    def add_book(self):
        amount = 0
        print("")
        print("----------------------------")
        print("\t1.เพิ่มหนังสือ")
        print("----------------------------")
        name_author = str(input("ชื่อผู้แต่ง: "))
        if len(self.author_name) == 0:
            self.author_name.append(Author(name_author))
            book_title = input("ชื่อเรื่อง: ")
            self.book_catalog.append(Book(self.author_name[0], book_title, input("หมวดหนังสือ: "),str(input("เลขชนิดหนังสือ: "))))
        else:
            amount2 = 0
            for name in self.author_name:
                if name.name == name_author:
                    book_title = input("ชื่อเรื่อง: ")
                    if len(self.book_catalog) == 0:
                        self.book_catalog.append(Book(name, book_title, input("หมวดหนังสือ: "),str(input("เลขชนิดหนังสือ: "))))
                    else:
                        for bookcatalog in self.book_catalog:
                            if bookcatalog.title != book_title:
                                amount2 += 1
                        if amount2 == len(self.book_catalog):
                            self.book_catalog.append(
                                Book(name, book_title, input("หมวดหนังสือ: "),str(input("เลขชนิดหนังสือ: "))))
                elif name.name != name_author:
                    amount += 1
            if amount == len(self.author_name):
                self.author_name.append(Author(name_author))
                book_title = input("ชื่อเรื่อง: ")
                self.book_catalog.append(Book(self.author_name[len(self.author_name) - 1], book_title,input("หมวดหนังสือ: "),str(input("เลขชนิดหนังสือ: "))))
        print("----------------------------")
        print("\tเพิ่มหนังสือสำเร็จ")
        print("----------------------------")
        print("")

    def search(self,search):
        for catalog in self.book_catalog:
            if catalog.isnb == search or catalog.title == search:
                print("----------------------------")
                catalog.show()
                print("----------------------------")
                print("")
            elif catalog.subject == search:
                print("----------------------------")
                catalog.show()
                print("----------------------------")
                print("")
            elif catalog.authors.name == search:
                print("----------------------------")
                catalog.show()
                print("----------------------------")
                print("")
            else:
                print("----------------------------")
                print("ไม่พบหนังสือ")
                print("----------------------------")
                print("")

    def del_book(self,search):
        for i, delete in enumerate(self.book_catalog):
            if delete.title == search or delete.isnb == search:
                self.book_catalog.pop(i)
                print("----------------------------")
                print("ลบหนังสือเรียบร้อย")
                print("----------------------------")
                print("")

class Book:
    isnb = 1
    def __init__(self,authors,title,subject,ddsnumber):
       self.isnb = Book.isnb
       self.authors = authors
       self.title = title
       self.subject = subject
       self.ddsnumber = ddsnumber
       Book.isnb += 1

    def show(self):
        data = [self.isnb,self.authors.name,self.title,self.subject,self.ddsnumber]
        title = ["เลขประจำหนังสือ: ","\nผู้แต่ง: ","\nชื่อหนังสือ: ","\nหมวดหมู่: ","\nหมวดหมู่หนังสือในห้องสมุด: "]
        print("\tรายละเอียดหนังสือ")
        print("----------------------------")
        print("")
        for i,data in enumerate(data):
            print(title[i] + str(data),end= " ")
        print()

class Author:
    def __init__(self,name):
        self._name = name
    @property
    def name(self):
        return self._name

def main():
    book_catalog = Catalog()
    while True:
        print("----------------------------")
        print("\tBook Catalog")
        print("----------------------------")
        print("\t1.เพิ่มหนังสือ \n\t2.ลบหนังสือ \n\t3.ค้นหาหนังสือ \n\t4.ออกจากโปรแกรม")
        print("----------------------------")
        choice = int(input("คุณต้องการทำอะไร(1-4): "))
        print("----------------------------")
        if choice == 1:
            book_catalog.add_book()
        elif choice == 2:
            book_catalog.del_book(input("ชื่อหนังสือที่ต้องการลบ: "))
        elif choice == 3:
            book_catalog.search(str(input("ค้นหาหนังสือ: ")))
        elif choice == 4:
            break
        else:
            print("*กรุณาใส่เฉพาะตัวเลข 1-4 เท่านั้น*")

main()

