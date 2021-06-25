import sqlite3

conn = sqlite3.connect('C:/Users/Spectastation/Downloads/farmer-mgmt/flask-gen-template/database.db')
c = conn.cursor()

#c.execute('''
#create table users(username varchar(20) primary key,
# password varcahr(40) not null, name varchar(40) not null,
#income int not null, dob date not null, 
#aadharno varchar(12) not null unique, phno varchar(12) unique)''')

#c.execute('''create table machinery(machineid varchar(20) primary key,
#cost int not null, name varchar(30) not null, 
# description varchar(500) not null )''')

#c.execute('''create table govtschemes(name varchar(200) primary key, 
#benefits varchar(500) not null, criteria varchar(500) not null )''')

#c.execute('''create table seed_fert_det(itemid varchar(20) primary key,
#cost int not null, 
#itemname varchar(30) not null, 
# type varchar(20) not null, 
# description varchar(500) not null )''')

#c.execute('''create table rents(rentid varchar(20) primary key, 
#username varchar(20) not null, machineid varchar(20) not null, 
#cost int not null,rentfrom date not null, renttill date not null)''')

#c.execute('''create table enrolls(enrollmentid varchar(30) primary key,
#scheme varchar(200) not null, username varchar(20) not null)''')

#c.execute('''create table purchases(billid varchar(20) primary key,
#username varchar(20) not null, itemid varchar(20) not null, 
# dop date not null, amount int not null)''')

#c.execute("""insert into users values('kural','kural'
# ,'kural',10,'1928-03-23','123455678909','9999999999')""")

#c.execute("""insert into machinery values
#('M1001',2000,'Harvestor 1230','This is a harvestor which will be very
#  useful in many things')""")

# c.execute("""insert into machinery values
# ('M1001',2000,'Harvestor 1230',
# 'This is a harvestor which will be very useful in many things')""")

# c.execute("""insert into seed_fert_det values
# ('F1002',5600,'Fennec','Fertilizer',
# 'Best for Rice crop. Improves plant natural nitrogen')""")

# c.execute('delete from rents')
# conn.commit()


# c.execute("insert into govtschemes values('PMKY','Very beneficial','medium criteria')")
# c.execute("insert into govtschemes values('PMKYPE','Very beneficial indeed','medium criteria indeed')")
# conn.commit()
c.execute('select * from enrolls')
x=c.fetchall()

for i in x:
    print(i)
#c.execute("insert into machinery values('M1005',25000,'Tafe2 Tractor','Very nice tractor, very good company.')")
c.execute('delete from enrolls')
conn.commit()
# c.execute('select * from rents')
# x=c.fetchall()

# for i in x:
#     print(i)
print('hiii')
c.close()