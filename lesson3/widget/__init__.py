MON = 1
TUE = 2
WED = 3
THU = 4
FRI = 5
SAT = 6
SUN = 7

class Person(object):
    #自訂的init,建立內建的attribute
    def __init__(self,name:str,age:int): #type hint
        self.__name = name #private attribute
        self.__age = age #private attribute

    #自訂實體被print()時的輸出
    def __repr__(self)->str:
        return f'我的名字是:{self.name}\n我的age是{self.age}'
    
    @property
    def name(self)->str:
        return self.__name
    
    @name.setter
    def name(self,n):
        print(f"不可以改名為{n}")

    @property
    def age(self)->int: #getter
        return self.__age
    
    @age.setter
    def age(self,value): #setter
        if value > 100 or value < 0:
            print("不合法的值")
        else:
            self.__age = value

class Student(Person): #繼承Person
    @classmethod
    def echo(cls):
        print("Hello!我是StudentClass")
        
    def __init__(self, age:int, name:str, chinese:int=0, english:int=0, math:int=0):
        super().__init__(name=name,age=age) #執行父類別的初始化
        self.chinese = chinese
        self.english = english
        self.math = math
    
    @property
    def total(self)->int:
        return self.chinese + self.english + self.math
    
    #instance method實體方法
    def average(self) -> float:
        return round(self.total / 3,ndigits=2)

def get_person(name:str, age:int) -> Person:
    return Person(name=name,age=age)

def get_student(name:str,age:int,chinese=60,english=60,math=60)->Student:
    return Student(name=name,age=age,chinese=chinese,english=english,math=math)                