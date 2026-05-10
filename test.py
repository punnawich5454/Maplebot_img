class EM:
    def __init__(self,age):
        self.age = age
        self.name = "em"
        self.id = 1
    def __eq__(self,object2):
        return self.age == object2.age
    # def __str__(self):
    #     return str(self.age)   
    def __repr__(self):
        # return f"{self.__class__.__name__} {repr((self.age))}"
        a = vars(self)
        # print(a) 
        s = [f"{k} = {v}" for k,v in a.items()]
        
        
        attrs = ("name","age","id")
        g = [f"{a} = {getattr(self,a)}" for a in attrs]
        return "\n".join(s)

if __name__ == "__main__":
   names = ["Somchai", "Somsri", "Somsak"]
   ages = [25, 30, 35]

   # ใช้ zip จับคู่กัน
   f = zip(names, ages)
   zipped_data = [*zip(names, ages)]

   # ต้องแปลงเป็น list ก่อนถึงจะเห็นผลลัพธ์ชัดเจน (เพราะ zip คืนค่าเป็น iterator)
   print(f)
   print(f)
   print(f)