create table news_data (
ID					int(20),
url	                varchar(250),
title	            varchar(250),
datatate	        varchar(100),
keyword	            varchar(100),
org_name	        varchar(100),
two_h_product	    varchar(100),
keywords	        varchar(250),
involving_org	    varchar(100),
two_h_products	    varchar(250),
content	            longtext,
content2	        longtext,
get_date	        varchar(100),
get_keyword_date	varchar(100),
status	            varchar(10),
hege	            varchar(10),
guid	            varchar(100),
source_site	        varchar(200),
wuran	            varchar(100),
fengxian	        varchar(100),
shengtai	        varchar(100),
ziyuan	            varchar(100),
xuanjiao	        varchar(100),
guanli	            varchar(100),
shuihj_2	        int(11) DEFAULT 0,
kongqi_2	        int(11) DEFAULT 0,
shenghj_2	        int(11) DEFAULT 0,
turang_2	        int(11) DEFAULT 0,
feiwu_2	            int(11) DEFAULT 0,
shengwu_2	        int(11) DEFAULT 0,
other_2             int(11) DEFAULT 0,
score				int(11) DEFAULT 0

);
create table news_result (
ID					int(20),
url	                varchar(250),
title	            varchar(250),
datatate	        varchar(100),
keyword	            varchar(100),
org_name	        varchar(100),
two_h_product	    varchar(100),
keywords	        varchar(250),
involving_org	    varchar(100),
two_h_products	    varchar(250),
content	            longtext,
content2	        longtext,
get_date	        varchar(100),
get_keyword_date	varchar(100),
status	            varchar(10),
hege	            varchar(10),
guid	            varchar(100),
source_site	        varchar(200),
wuran	            varchar(100),
fengxian	        varchar(100),
shengtai	        varchar(100),
ziyuan	            varchar(100),
xuanjiao	        varchar(100),
guanli	            varchar(100),
shuihj_2	        int(11) DEFAULT 0,
kongqi_2	        int(11) DEFAULT 0,
shenghj_2	        int(11) DEFAULT 0,
turang_2	        int(11) DEFAULT 0,
feiwu_2	            int(11) DEFAULT 0,
shengwu_2	        int(11) DEFAULT 0,
other_2             int(11) DEFAULT 0,
score				int(11) DEFAULT 0

);

create table news_select_middle (
oid					varchar(20),
ID					int(20),
url	                varchar(250),
title	            varchar(250),
datatate	        varchar(100),
keyword	            varchar(100),
org_name	        varchar(100),
two_h_product	    varchar(100),
keywords	        varchar(250),
involving_org	    varchar(100),
two_h_products	    varchar(250),
content	            longtext,
content2	        longtext,
get_date	        varchar(100),
get_keyword_date	varchar(100),
status	            varchar(10),
hege	            varchar(10),
guid	            varchar(100),
source_site	        varchar(200),
wuran	            varchar(100),
fengxian	        varchar(100),
shengtai	        varchar(100),
ziyuan	            varchar(100),
xuanjiao	        varchar(100),
guanli	            varchar(100),
shuihj_2	        int(11) DEFAULT 0,
kongqi_2	        int(11) DEFAULT 0,
shenghj_2	        int(11) DEFAULT 0,
turang_2	        int(11) DEFAULT 0,
feiwu_2	            int(11) DEFAULT 0,
shengwu_2	        int(11) DEFAULT 0,
other_2             int(11) DEFAULT 0,
score				int(11) DEFAULT 0
);



class news_result_d(db.Model):
    __tablename__='news_result'
    ID=db.Column(db.String(20))
    # content	=db.Column(db.LongText)
    status=db.Column(db.String(100))
    hege=db.Column(db.String(100))
    source_site	=db.Column(db.String(100))
    wuran=db.Column(db.String(100))
    fengxian=db.Column(db.String(100))
    shengtai=db.Column(db.String(100))
    ziyuan=db.Column(db.String(100))
    xuanjiao=db.Column(db.String(100))
    guanli=db.Column(db.String(100))
    shuihj_2=db.Column(db.String(10))
    kongqi_2=db.Column(db.String(10))
    shenghj_2=db.Column(db.String(10))
    turang_2=db.Column(db.String(10))
    feiwu_2=db.Column(db.String(10))
    shengwu_2=db.Column(db.String(10))
    other_2=db.Column(db.String(10))
    score=db.Column(db.String(10))

class news_data_d(db.Model):
    __tablename__='news_data'
    ID=db.Column(db.String(20))
    url=db.Column(db.String(250))
    title=db.Column(db.String(250))
    datatate=db.Column(db.String(100))
    keyword=db.Column(db.String(100))
    org_name=db.Column(db.String(100))
    two_h_product=db.Column(db.String(100))
    keywords=db.Column(db.String(250))
    involving_org=db.Column(db.String(100))
    two_h_products=db.Column(db.String(250))
    # content=db.Column(db.TEXT)
    get_date=db.Column(db.String(100))
    get_keyword_date=db.Column(db.String(100))
    status=db.Column(db.String(100))
    hege=db.Column(db.String(100))
    guid=db.Column(db.String(100))
    source_site=db.Column(db.String(100))
    wuran=db.Column(db.String(100))
    fengxian=db.Column(db.String(100))
    shengtai=db.Column(db.String(100))
    ziyuan=db.Column(db.String(100))
    xuanjiao=db.Column(db.String(100))
    guanli=db.Column(db.String(100))
    shuihj_2=db.Column(db.String(100))
    kongqi_2=db.Column(db.String(100))
    shenghj_2=db.Column(db.String(100))
    turang_2=db.Column(db.String(100))
    feiwu_2=db.Column(db.String(100))
    shengwu_2=db.Column(db.String(100))
    other_2=db.Column(db.String(100))
    score=db.Column(db.String(10))



#½ÇÉ«
CREATE TABLE roles (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(64) DEFAULT NULL,
  default tinyint(1) DEFAULT NULL,
  permissions int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY name (name),
  KEY ix_roles_default (default)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


#ÓÃ»§
CREATE TABLE users (
  startnum int(20) DEFAULT NULL,
  endnum int(20) DEFAULT NULL,
  id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(80) DEFAULT NULL,
  email varchar(320) DEFAULT NULL,
  password_hash varchar(1000) DEFAULT NULL,
  name varchar(64) DEFAULT NULL,
  location varchar(64) DEFAULT NULL,
  about_me text,
  member_since datetime DEFAULT NULL,
  last_seen datetime DEFAULT NULL,
  confirmed tinyint(1) DEFAULT NULL,
  role_id int(11) DEFAULT NULL,
  passwd varchar(32) DEFAULT NULL,
  avatar_hash varchar(32) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=214 DEFAULT CHARSET=utf8;

,
  UNIQUE KEY email (email),
  UNIQUE KEY ix_users_username (username),
  KEY role_id (role_id),
  CONSTRAINT users_ibfk_1 FOREIGN KEY (role_id) REFERENCES roles (id)

        <div class="pagination">
            {{ macros.pagination_widget(pagination, 'crawlers.news') }}
        </div>
		
		
		
		ID				,
        url	            , 
        title	        , 
        datatate	    , 
        keyword	        , 
        org_name	    , 
        two_h_product	, 
        keywords	    , 
        involving_org	, 
        two_h_products	, 
        content	        , 
        content2	    , 
        get_date	    , 
        get_keyword_date,
        status	        , 
        hege	        , 
        guid	        , 
        source_site	    