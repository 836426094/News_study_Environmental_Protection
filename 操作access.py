#coding=utf-8

import win32com
#获取Connection对象
conn = win32com.client.Dispatch('ADODB.Connection')
#设置ConnectionString
conn.ConnectionString = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=%s"%(mdb_file) #mdb_file为mdb文件的路径
#打开连接
conn.Open()#这里也可以conn.Open(DSN) DSN内容和ConnectionString一致
# 此时数据库就连接上了。
#
# 成功的平台：win2008 64位系统；office2010 32位；python 32位；ODBC 32位（位于C:/Windows/SysWOW64/odbcad32.exe）打开后有Microsoft Access Driver（*mdb,*accdb)等驱动程序
#
# 失败的平台：win7 64位系统；office2013 64位；python 64,32都试了；试着安装了AccessDatabaseEngine2010的，都未成功，目前未找到原因。

#打开已打开的数据库中的已有表或者视图表
rs = win32com.client.Dispatch('ADODB.Recordset')
rs.Open(tablename,conn,1,3)#Open(sql,conn,1,3)
#rs的Open（Source,ActiveConnection,CursorType,LockType,Options)
#后面的参数3使得表可以被编辑更新。具体详细的参数和意义可以参照ADO程序员参考http://doc.51windows.net/ado/?url=/ado/dir.htm
# 此时获得了一个可以表，其实只是一个游标，游标指向的是对应表中的一条记录，称为当前记录。我们可以通过一系列的操作读取、编辑当前记录，也可以移动游标来改变当前记录。

# 复制代码
#这里对几个重要的函数和属性记录一下
rs.MoveFirst()
rs.MoveLast()
rs.MoveNext()
rs.MovePrevious()#跟打开表的游标类型有关系。
#用来改变游标所指向的当前记录。
rs.BOF  #当前记录位于第一个记录的前面时为True
rs.EOF  #当前记录位于最后一个记录之后时为True 判断记录是否遍历完

# rs.BOF和rs.EOF同时为True时说明当前rs中没有记录。也就不能进行上面几个操作。

#添加新记录着重记录：
###利用rs.AddNew()即依据rs新建了一条新纪录，rs会指向该记录。
###rs.Fields.Item(1)  rs.Fields.Item("fieldname") 得到当前记录的对应字段的项
###rs.Fields.Item(1).Value = data为对应项赋值
###rs.Fields.Item(0).AppendChunk(blob)  #对于二进制数据需要用此函数赋值

###设置好各项的值之后
###rs.Update()  保存新纪录，也可以保存对记录的修改。调用该方法，需要在打开rs的时候，设置锁定类型具体都可以在  ADO程序员参考http://doc.51windows.net/ado/?url=/ado/dir.htm找到介绍。
# 复制代码
# 至此对于Access 的mdb文件的简单访问就基本实现了。



# ADO作为访问数据的COM接口，支持多种数据源，多种语言，当然也就支持Python对于Access的访问。对于Python访问Access更深入的学习，应该是对于ADO相关接口类的深入了解。
#
# 这里有个对于Python访问数据库的相对清楚的教程：http://www.mayukhbose.com/python/ado/ado-recordset.php
#
#
#
# 最后记录编码问题，Python利用AddNew添加新纪录可以避免编码问题，对于文本可以直接将unicode对象赋值给文本字段。如果利用conn.Execute(insert_sql)或者 rs.Execute(insert_sql)对于insert_sql插入sql字符串，不能插入unicode对象，需要编码为gbk、gb2312、gb18030、utf8等一系列编码，在一些偏僻中文字符上会出现乱码等一系列不可控问题。