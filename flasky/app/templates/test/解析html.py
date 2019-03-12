#coding=utf-8
# from html.parser import HTMLParser
# class MyHTMLParser(HTMLParser):
#     def __init__(self):
#         HTMLParser.__init__(self)
#         self.links = []
#     def handle_starttag(self, tag, attrs):
#         #print "Encountered the beginning of a %s tag" % tag
#         if tag == "a":
#             if len(attrs) == 0:
#                 pass
#             else:
#                 for (variable, value) in attrs:
#                     if variable == "href":
#                         self.links.append(value)
#
# if __name__ == "__main__":
#     html_code = """ <a href="www.google.com"> google.com</a> <A Href="www.pythonclub.org"> PythonClub </a> <A HREF = "www.sina.com.cn"> Sina </a> """
#     hp = MyHTMLParser()
#     hp.feed(html_code)
#     hp.close()
#     print(hp.links)


# from html.parser import HTMLParser
#
# page =u'''<sada>啊啊啊</sada><a href="http://click.union.360buy.com/JdClick /?unionId=75" class="f1"  style="padding-left:13px; padding-right:14px">京东商城</a></td><td><a href="http://www.letao.com /?source=hao123" class="f1">乐淘网上鞋城</a></td><td><a href="http://www.lashou.com/cl_today/w_3001" class="f2">拉手团购</a></td><td><a href="http://www.amazon.cn/?tag=2009hao123famousdaohang" class="f2">亚马逊</a></td><td><a href="http://www.vancl.com/?source=hao123mp"  class="f1">凡客诚品</a></td><td><a href="http://reg.jiayuan.com/st/?id=3237&url=/st /main.php" class="f1">世纪佳缘'''
# class hp(HTMLParser):
#     a_text = False
#
#     def handle_starttag(self,tag,attr):
#         if tag == 'a':
#             self.a_text = True
#             #print (dict(attr))
#
#     def handle_endtag(self,tag):
#         if tag == 'a':
#             self.a_text = False
#
#     def handle_data(self,data):
#         if self.a_text:
#             print (data)
#
# yk = hp()
# yk.feed(page)
# yk.close()
#

#coding=utf8
import HTMLParser
parser = HTMLParser.HTMLParser()
s1 = parser.unescape('&#27979;&#35797;')
print s1            # output: 测试

s2 = parser.unescape('&#x6D4B;&#x8BD5;')
print s2             # output: 测试


