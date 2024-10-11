import tools

print(tools.SUN)
p1 = tools.Person(name="robert",age=30)
print(p1)

s1 = tools.Student(name="徐國堂",age=40,chinese=87,english=75,math=67)
print(s1.name)
print(s1.age)
print(s1.english)
print(s1.math)
print(s1.chinese)
print(s1.total)
print(s1.average())