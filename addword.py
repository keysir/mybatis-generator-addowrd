#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mybatis-generator 添加字段脚本
import  xml.dom.minidom

# 项目基本路径
basepath='E:/python/sxh/';

# 配置参数
rclassname='AttributeInfo';#类名称 OO原则
keytype='String';#添加字段的类型
Keyname='tesekey';#字段名称


#相对路径
dtopath='dto/';
modelpath='model/';
daoImplpath='dao/impl/';

# get/set模版数据拼接

getfun='public '+keytype+' get'+Keyname.capitalize()+'(){\r\t\treturn '+Keyname+';\r\t}'; 
setfun='public void set'+Keyname.capitalize()+'(){\r\t\tthis.'+Keyname+' = '+Keyname+';\r\t}';

# model文件路径 
allmodelpath=basepath+modelpath+rclassname+'.java';

#修改model 读取、数据准备
f = open(allmodelpath, 'r', encoding='utf-8');
s=f.read();

content="""""";

#将字段添加到第一个 public 方法之前

contentli= s.split("public", 2);

#数据拼接
content=contentli[0]+'public'+contentli[1]+'\tprivate '+keytype+' '+Keyname+';\r\r';
content=content+"\t"+getfun+"\r\n";
content=content+"\t"+setfun+"\r\n";
content=content+'\tpublic'+contentli[2];

#修改model 写入
fw= open(allmodelpath, 'w', encoding='utf-8');

fw.write(content);

fw.close();

# 
# 修改dto
# 
alldtopath=basepath+dtopath+rclassname+'DTO.java';

#修改model 读取、数据准备
fdto = open(alldtopath, 'r', encoding='utf-8');
sdto=fdto.read();

contentdto="""""";

#将字段添加到第一个 public 方法之前

contentdtoli= sdto.split("public", 2);

#数据拼接
contentdto=contentdtoli[0]+'public'+contentdtoli[1]+'\tprivate '+keytype+' '+Keyname+';\r\r';
contentdto=contentdto+"\t"+getfun+"\r\n";
contentdto=contentdto+"\t"+setfun+"\r\n";
contentdto=contentdto+'\tpublic'+contentdtoli[2];

#修改model 写入
fwdto= open(alldtopath, 'w', encoding='utf-8');

fwdto.write(contentdto);

fwdto.close();

# 
# 修改Mapper
# 
allmapperpath=basepath+daoImplpath+rclassname+'Mapper.xml';

# 数据类型转换

jdbcType="";

if keytype=="String"
  jdbcType="VARCHAR";
else if keytype=="Integer"
  jdbcType="INTEGER";
else if keytype=="Boolean"
  jdbcType="INTEGER";
else if keytype=="Date"
  jdbcType="TIMESTAMP";
else if keytype=="Double"
  jdbcType="DECIMAL";
else
  jdbcType="DECIMAL";

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse(allmapperpath);

#得到文档元素对象
root = DOMTree.documentElement;

# 修改 resultMap
resultMaps =root.getElementsByTagName("resultMap");
resultMap0=resultMaps[0];

resultnew= DOMTree.createElement('result');

resultnew.setAttribute('column',Keyname);
resultnew.setAttribute('jdbcType',jdbcType);
resultnew.setAttribute('property',Keyname);
resultMap0.appendChild(resultnew);

# 修改Base_Column_List
sqls = root.getElementsByTagName("sql");
sql0=sqls[0];
sql0_con=sql0.firstChild.data;

sql0_con_new=sql0_con+", "+Keyname;

sql0.firstChild.data=sql0_con_new;

inserts = root.getElementsByTagName("insert");

#修改 insert 
insert0=inserts[0];
insert0_id=insert0.getAttribute("id");

if insert0_id=="insert":
 insert0_con=insert0.firstChild.data
 # print(insert0_con)

 map_con_result_li= insert0_con.split("(", 2);

 insert0_connew=map_con_result_li[0]+"("+Keyname+", "+map_con_result_li[1]+"( {"+Keyname+",jdbcType="+jdbcType+"}, "+map_con_result_li[2];

 insert0.firstChild.data=insert0_connew;


 # 修改insertSelective
 # 
trims=root.getElementsByTagName("trim");

trim0=trims[0];
trim0_prefix=trim0.getAttribute("prefix");

if trim0_prefix=="(":

 trim0if = DOMTree.createElement('if')
 trim0if.setAttribute('test' ,Keyname+'  != null')
 trim0ifT=DOMTree.createTextNode('\n\t\t\t\t'+Keyname+',\n\t\t')
 trim0if.appendChild(trim0ifT)
 trim0.appendChild(trim0if);

trim1=trims[1];
trim1_prefix=trim1.getAttribute("prefix");

if trim1_prefix=="values (":
 trim1if = DOMTree.createElement('if')
 trim1if.setAttribute('test' ,Keyname+'  != null')
 trim1ifT=DOMTree.createTextNode('\n\t\t\t\t#{'+Keyname+',jdbcType='+jdbcType+'},\n\t\t')
 trim1if.appendChild(trim1ifT)
 trim1.appendChild(trim1if);

 
 # 修改updateByPrimaryKeySelective
 
sets=root.getElementsByTagName("set");

set0=sets[0];
set0if = DOMTree.createElement('if');
set0if.setAttribute('test' ,Keyname+'  != null');
set0ifT=DOMTree.createTextNode('\n\t\t\t\t'+Keyname+' = #{'+Keyname+',jdbcType='+jdbcType+'},\n\t\t');
set0if.appendChild(set0ifT);
set0.appendChild(set0if);


 # 修改updateByAttributeType
doupdates=root.getElementsByTagName("update");
for update in doupdates:
 	if update.getAttribute("id")=="updateByPrimaryKey":
 	 updateByAttributeType_con=update.firstChild.data
 	 updateByAttributeType_con_li=updateByAttributeType_con.split("where", 1);
 	 updateByAttributeType_con_new=updateByAttributeType_con_li[0]+","+Keyname+" = #{"+Keyname+",jdbcType="+jdbcType+"} where "+updateByAttributeType_con_li[1]
 	 update.firstChild.data=updateByAttributeType_con_new;

# 保存XML
f2= open(allmapperpath, 'w', encoding='utf-8');
DOMTree.writexml(f2, addindent='  ', newl='\n',encoding='utf-8');
f2.close();