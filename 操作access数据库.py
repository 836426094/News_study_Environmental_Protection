Python����Access���ݿ�
��������ƪ�����й��������������ϸ������Python����Access���ݿ����ط�����ϣ�����Ը�����Ҫ�������Ǵ���һЩ������

AD��

Python�� �����Եĳ��֣�����������Ա�ǳ���ĺô������ǿ�����������һ���ǿ����������Դ���������ɵ�ʵ������ض��������󡣱���Python���� Access���ݿ�Ĺ���ʵ�ֵȵȡ���Python����Access���ݿ�֮ǰ������,��Ӧ��װ��Python��Python for Windows extensions��

Python����Access���ݿⲽ��֮1���������ݿ�����

import win32com.client
conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
conn.Open(DSN)
Python����Access���ݿⲽ��֮2����һ����¼��

rs = win32com.client.Dispatch(r'ADODB.Recordset')
rs_name = 'MyRecordset'#����
rs.Open('[' + rs_name + ']', conn, 1, 3)
Python����Access���ݿⲽ��֮3���Լ�¼������

rs.AddNew()
rs.Fields.Item(1).Value = 'data'
rs.Update()
Python����Access���ݿⲽ��֮4����SQL��������������

conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
sql_statement = "Insert INTO [Table_Name] ([Field_1],  [Field_2]) VALUES ('data1', 'data2')"
conn.Open(DSN)
conn.Execute(sql_statement)
conn.Close()
Python����Access���ݿⲽ��֮5��������¼

rs.MoveFirst()
count = 0
while 1:
if rs.EOF:
break
else:
countcount = count + 1
rs.MoveNext()
ע�⣺���һ����¼�ǿյģ���ô��ָ���ƶ�����һ����¼������һ��������Ϊ��ʱrecordcount����Ч�ġ�����ķ����ǣ���һ����¼��֮ǰ���Ƚ�Cursorlocation����Ϊ3��Ȼ���ٴ򿪼�¼������ʱrecordcount������Ч�ġ����磺

rs.Cursorlocation = 3 # don't use parenthesis here
rs.Open('Select * FROM [Table_Name]', conn) # be sure conn is open
rs.RecordCount # no parenthesis here either
���Ͼ������Ƕ�Python����Access���ݿⲽ�����ؽ��ܡ�