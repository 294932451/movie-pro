# movie-pro

# day2

项目目录

![img](https://cdn.nlark.com/yuque/0/2023/jpeg/21732846/1693380567478-2e18911c-ac2d-49d9-b63d-9e4c8c232fc1.jpeg)

前后台项目目录分析

![img](https://cdn.nlark.com/yuque/0/2023/png/21732846/1693380661879-43d868a1-fec5-4592-9479-f7e8d2664bb8.png)

蓝图构建项目目录

1. 什么是蓝图

https://dormousehole.readthedocs.io/en/latest/tutorial/views.html

- 定义蓝图
- 注册蓝图
- 调用蓝图

/home/__init__.py    

```python
from flask import Blueprint   #这是从 Flask 框架中导入 Blueprint 类。Blueprint 是 Flask 提供的一个工具，它允许你为你的应用程序组织路由和其他功能

home = Blueprint("home",__name__) #这里创建了一个新的 Blueprint 对象，并将其赋值给变量 home。这个 Blueprint 的名字是 "home"，通常用于区分不同的 Blueprints。__name__ 参数则是告诉 Flask，模板和静态文件应该从哪里被加载。在这里，它们会被加载从包含当前 Blueprint 的模块

import app.home.views # 导入了 app.home.views 模块
```

/admin/__init__.py

```python
from flask import Blueprint

admin = Blueprint("admin",__name__)

import app.admin.views
```

/home/views.py

```python
from . import home
@home.route("/")
def index():
    return "<h1>hello home</h1>"
```

/admin/views.py

```python
from . import admin # 从当前包或模块导入了 home Blueprint
@admin.route("/")
def index():
    return "<h1>hello admin</h1>" # 装饰器，它告诉 Flask：当请求访问应用程序的根路径（即 /）时，应该调用后面的函数 index
```

/app/__init__.py

```python
from flask import Flask

app = Flask(__name__)

app.debug = True

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
```

/movie/manage.py

```python
from app import app
if __name__ == '__main__':
    app.run()
```



/app/models.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

# pymysql.install_as_MySQLdb()
app = Flask(__name__)

# app.config['SQLALCHEMY_BINDS'] = {
#     'default': 'mysql+pymysql://root:123456@127.0.0.1:3306/movie',
# }
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:123456@127.0.0.1:3306/movie'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(255))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    userlogs = db.relationship("Userlog", backref='user')  # 会员日志外键关系关联
    comments = db.relationship("Comment", backref='user')  # 评论外键关联
    moviecols = db.relationship("Moviecol", backref='user')  # 收藏外键关联

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登陆日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship("Movie", backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # url
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    palynum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时长
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref='movie')  # 评论外键关联
    moviecols = db.relationship('Moviecol', backref='movie')  # 收藏外键关联

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.id


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref='role')  # 收藏外键关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员dmin
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 名称
    pwd = db.Column(db.String(255))  # 密码
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('AdminLog', backref='admin')
    oplogs = db.relationship('OpLog', backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 名称
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<AdminLog %r>" % self.id


# 操作日志
class OpLog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 名称
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<OpLog %r>" % self.id

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  #创建表
```

安装mysql 创建数据库

cd app

执行  python models.py