"""
使用sqlalchemy创建数据模型,并连接数据库
"""

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base

# 建立与数据库的连接
engine = create_engine('mysql+pymysql://qmx:123@localhost:3306/exercise')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), unique=True, nullable=False)
    birthday = Column(Date)
    money = Column(Float, default=0.0)

session = Session()

# Base.metadata.create_all(checkfirst=True)

# bob = Student(name='Bob', birthday=datetime.date(1991, 2, 3), money=100)
# tom = Student(name='Tom', birthday=datetime.date(1992, 3, 4), money=10)
# lucy = Student(name='Lucy', birthday=datetime.date(1993, 4, 5), money=1000)
# jimmy = Student(name='Jimmy', birthday=datetime.date(1994, 5, 6), money=200)
# alex = Student(name='Alex', birthday=datetime.date(1995, 6, 7), money=300)
# vae = Student(name='Vae', birthday=datetime.date(1996, 7, 8), money=500)
# rob = Student(name='Rob', birthday=datetime.date(1997, 8, 9), money=12000)
# ella = Student(name='Ella', birthday=datetime.date(1998, 9, 10), money=12300)
# jerry = Student(name='Jerry', birthday=datetime.date(1999, 10, 11), money=5100)

# obj_name_list = [bob, tom, lucy, jimmy, alex, vae, rob, ella, jerry]
# session.add_all(obj_name_list)
# session.commit()

fornow = Student(name='Fornow', birthday=datetime.date(2000, 12, 31), money=2500)
# session.add(fornow)
print('fornow加进去了')
session.commit()

fornow.money = 10.5
print('fornow钱被偷走了')
session.commit()

stu = session.query(Student)
res1 = stu.filter().all()
for i in res1:
    print(i.name)

# session.delete(fornow)
# print('fornow被我删掉了')
# session.commit()

res2=stu.filter_by(name='Jerry').one()
print(res2.name)

res3=stu.get(2)
print(res3.name)

res4=stu.filter(Student.id<5).order_by('birthday').limit(3).offset(2)
for i in res4.all():
    print(i.name,i.birthday,i.money)

num =stu.filter(Student.money>200).count()
print(num)

exists =stu.filter_by(name="Ella").exists()
res10 =session.query(exists).scalar()
print(res10)