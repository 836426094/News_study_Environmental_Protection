Python操作Access数据库
我们在这篇文章中公分了五个步骤详细分析了Python操作Access数据库的相关方法，希望可以给又需要的朋友们带来一些帮助。

AD：

Python编 程语言的出现，带给开发人员非常大的好处。我们可以利用这样一款功能强大的面向对象开源语言来轻松的实现许多特定功能需求。比如Python操作 Access数据库的功能实现等等。在Python操作Access数据库之前，首先,你应安装了Python和Python for Windows extensions。

Python操作Access数据库步骤之1、建立数据库连接

import win32com.client
conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
conn.Open(DSN)
Python操作Access数据库步骤之2、打开一个记录集

rs = win32com.client.Dispatch(r'ADODB.Recordset')
rs_name = 'MyRecordset'#表名
rs.Open('[' + rs_name + ']', conn, 1, 3)
Python操作Access数据库步骤之3、对记录集操作

rs.AddNew()
rs.Fields.Item(1).Value = 'data'
rs.Update()
Python操作Access数据库步骤之4、用SQL来插入或更新数据

conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
sql_statement = "Insert INTO [Table_Name] ([Field_1],  [Field_2]) VALUES ('data1', 'data2')"
conn.Open(DSN)
conn.Execute(sql_statement)
conn.Close()
Python操作Access数据库步骤之5、遍历记录

rs.MoveFirst()
count = 0
while 1:
if rs.EOF:
break
else:
countcount = count + 1
rs.MoveNext()
注意：如果一个记录是空的，那么将指针移动到第一个记录将导致一个错误，因为此时recordcount是无效的。解决的方法是：打开一个记录集之前，先将Cursorlocation设置为3，然后再打开记录集，此时recordcount将是有效的。例如：

rs.Cursorlocation = 3 # don't use parenthesis here
rs.Open('Select * FROM [Table_Name]', conn) # be sure conn is open
rs.RecordCount # no parenthesis here either
以上就是我们对Python操作Access数据库步骤的相关介绍。