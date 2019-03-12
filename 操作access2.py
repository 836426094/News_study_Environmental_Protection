# -*-coding:utf-8-*-
import pyodbc

# �������ݿ⣨����Ҫ��������Դ��,connect()��������������һ�� Connection ����
# cnxn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=.\data\goods.mdb')
cnxn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\���󻷾�����\�ؼ�������20181223-20181230\data.mdb')
# cursor()ʹ�ø����Ӵ����������أ�һ���α�����α�Ķ���
crsr = cnxn.cursor()

# ��ӡ���ݿ�goods.mdb�е����б�ı���
print('`````````````` goods ``````````````')
for table_info in crsr.tables(tableType='TABLE'):
    print(table_info.table_name)


l = crsr.execute("SELECT * from goods WHERE goodsId='0001'")# [('0001', '��Ҷ', 20, 'A��˾', 'B��˾', 2000, 2009)]

rows = crsr.execute("SELECT currentStock from goods")  # ���ص���һ��Ԫ��
for item in rows:
    print(item)

l = crsr.execute("UPDATE users SET username='lind' WHERE password='123456'")
print(crsr.rowcount)  # ��֪�������޸ĺ�ɾ��ʱ������Ӱ���˶�������¼�����ʱ�������ʹ��cursor.rowcount�ķ���ֵ��

# �޸����ݿ���int���͵�ֵ
value = 10
SQL = "UPDATE goods " \
      "SET lowestStock=" + str(value) + " " \
      "WHERE goodsId='0005'"

# ɾ����users
crsr.execute("DROP TABLE users")
# �����±� users
crsr.execute('CREATE TABLE users (login VARCHAR(8),userid INT, projid INT)')
# �����в���������
crsr.execute("INSERT INTO users VALUES('Linda',211,151)")

''''''
# ��������
crsr.execute("UPDATE users SET projid=1 WHERE userid=211")

# ɾ��������
crsr.execute("DELETE FROM goods WHERE goodNum='0001'")

# ��ӡ��ѯ�Ľ��
for row in crsr.execute("SELECT * from users"):
    print(row)


# �ύ���ݣ�ֻ���ύ֮�����еĲ����Ż��ʵ�ʵ����������Ӱ�죩
crsr.commit()
crsr.close()
cnxn.close()
