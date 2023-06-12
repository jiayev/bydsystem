# bydsystem
## 充电桩管理系统

### 接口文档

### To Do List
1. 时间系统，可以设定开始时间、时间单位，可设置步进或自动进行，每个时间单位开始时进行检查和操作，正在充电的车每次时间单位结束时计算费用，结束时加到详单中
2. 重写申请系统，首先将申请推至等待表中，然后检查对应充电桩的充电位和等待位是否有空，有空则将等待表中申请推至位置，直到没有空位或者等待表为空
3. 以上的检查需要在每个时间单位开始时进行
4. 退出充电桩功能，分为以下几个情况：
    1. 充电桩关闭，需要把充电位和等待位中的用户全部退出并返回等待表
    2. 用户主动退出或充电完成，如果用户在充电位，则将等待位中的用户推至充电位，如果用户在等待位，则直接移除；之后，重新检查
5. 账单与详单功能：
    1. 详单在每次退出充电桩时生成，记录进数据库，同时每次生成详单时更新账单，将详单中的金额加入账单中，并记载详单id
    2. 账单和详单可通过id、车id查询

## Flask框架

![Flask Logo](https://flask.palletsprojects.com/en/2.0.x/_static/flask-icon.png)

Flask是一个轻量级的Python Web框架，用于快速构建Web应用程序。它简单易用，但功能强大，可以帮助开发者快速搭建起一个稳定可靠的Web应用。

本文档将介绍如何在Flask框架下进行开发，包括安装、基本用法和常见特性。

### 安装

首先，确保你的开发环境中已经安装了Python。然后，可以通过以下命令安装Flask：

```
pip install flask
```

### 快速开始

下面是一个简单的Flask应用程序的示例：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

这个应用程序创建了一个Flask实例，定义了一个路由（route）和对应的处理函数。当访问根URL（/）时，会调用`hello()`函数并返回"Hello, World!"。最后通过`app.run()`启动应用。

保存代码为`app.py`，在终端中执行以下命令运行应用程序：

```
python app.py
```

你将在终端中看到应用程序运行的输出，并可以通过浏览器访问`http://localhost:5000`查看"Hello, World!"。

### 路由和视图函数

Flask使用装饰器（decorators）来定义路由和对应的视图函数。路由决定了用户请求的URL路径应该调用哪个视图函数来处理。

```python
@app.route('/')
def index():
    return 'This is the homepage'

@app.route('/about')
def about():
    return 'About page'
```

在上面的示例中，`@app.route('/')`定义了根URL的路由，对应的视图函数是`index()`。同理，`@app.route('/about')`定义了`/about`路径的路由，对应的视图函数是`about()`。当用户访问根URL或`/about`时，Flask将调用相应的视图函数并返回其返回值。

### 模板

在复杂的应用程序中，通常需要动态生成HTML页面。Flask使用模板来实现这一功能。模板是包含动态内容的HTML文件，可以通过在模板中插入变量或执行控制流来生成动态内容。

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = 'John Doe'
    return render_template('index.html', name=name)
```

上面的示例中，`render_template()`函数用于渲染模板`index.html`并传递变量`name`给模板。在模板中可以通过`{{ name }}`来使用这个变量。

### 数据库集成

Flask可以与各种数据库进行

集成，如SQLite、MySQL、PostgreSQL等。通过使用数据库适配器（Database Adapter）和对象关系映射（Object Relational Mapping，ORM）库，可以在Flask应用中轻松地进行数据库操作。

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
```

上面的示例中，我们使用了SQLAlchemy来进行数据库操作。`User`类定义了一个数据库表，包含了`id`和`username`两个字段。通过`User.query.all()`可以获取所有用户对象，然后传递给模板进行展示。

### 扩展

Flask框架提供了丰富的扩展（Extensions），用于简化开发过程和增加功能。这些扩展包括：

- **Flask-WTF**：用于处理Web表单的扩展。
- **Flask-Login**：提供用户认证和会话管理的扩展。
- **Flask-RESTful**：用于构建RESTful API的扩展。
- **Flask-SQLAlchemy**：用于与SQL数据库集成的扩展。

你可以通过Flask官方网站或第三方扩展库的文档了解更多有用的扩展。

### 总结

Flask是一个简单而强大的Web框架，适用于构建各种类型的Web应用程序。本文档提供了Flask的基本用法和常见特性的简要介绍，希望能帮助你入门Flask开发。如需更详细的信息，请参阅Flask官方文档。

祝你在Flask的世界中编写出优秀的Web应用程序！


## 版本管理策略

### 主要分支

主要分支为`master`与`dev`分支，默认分支为`master`分支。

- `master`分支
  描述：产品的发布分支，用于进行稳定版本的迭代
  是否受保护：是
  管理员：jiayev
- `dev`分支
  描述：产品最新的开发版本，用于进行新功能的测试
  是否受保护：是
  管理员：jiayev

### 分支的分类

为了便于分支管理，将不同功能的分支以特定的格式命名，分支分类如下：

- feature 分支：用于进行新功能的开发，命名规则为`dev-feat-{feat_name}`，`feat_name`应该由数字、字母、以及**下划线**组成
- fix 分支：用于 issue 的修复，命名方式为`dev-fix-{fix_name}`，`fix_name`的命名规则同上
- refactor 分支：用于代码的重构，大概率不需要使用，命名方式为`dev-refactor-{refactor_name}`，`refactor_name`的命名规则同上

> 注：使用下划线的目的是将分支的名称与前缀区分开，方便阅读

### 开发流程

1. 确认需要执行的任务类别
2. 基于`dev`分支或者自己的子分支按照命名规范创建新分支
3. 进行开发
4. (可选) 使用`merge`或`rebase`指令（建议用`merge`）将`dev`分支的提交更新到自己的分支上
5. 使用`push`推送全部提交
6. 在*创建合并请求*页面发起`PR`

### 创建合并请求的方法

1. 在代码仓库菜单中点击合并请求，点击右上角的创建合并请求，在打开的页面中选择源分支为你自己的分支，目标分支选择`dev`分支。若提示无法合并，则说明`dev`分支有新的提交，并且这些提交中修改的代码与你的分支修改的代码**有冲突**，这时需要执行**开发流程**中的步骤 4。步骤 4 执行完成后，再回到*创建合并请求*页面，选择分支后，已可以进行合并。
2. 输入合并请求标题，格式为`{merge_type}. {title}`，例如“feat. 添加登录注册支持”。确保`title`在 20 字以内
3. (可选) 输入描述，如果改动较小，则可以不输入描述。若改动较大或认为又需要特别说明的内容，则可以写在描述中
4. 如果分支为`fix`类型，则需要在下方的关联资源中关联对应的 issue

### 提交消息的规范

提交(commit)需要按照规范进行。此项目参考谷歌的 AngularJS 提交规范，具体规范内容可以使用搜索引擎查询。这里推荐使用 Visual Studio Code 进行开发，在拓展中搜索并安装`git-commit-plugin`，在版本管理页面点击“版本管理”标题右侧的 Github 章鱼按钮，按照提示信息填写提交信息。本项目只需要填写前三条信息，前两条（影响范围和提交标题）必须填写，第三条（提交描述）可选，当涉及到复杂变动时可以填写。

## 附录教程

### Git 的基本使用方法

这里提供一些本项目开发的 git 使用 tips。

推荐使用 Visual Studio Code 提供的 GUI 版本管理功能，可以大幅减小 Git 的学习成本。

**commit**

提交，一次提交会创建一个提交记录，可以在版本管理页的下方查看。

**fetch**

本地的版本信息不一定是最新的，例如选择分支时不一定会出现他人刚在代码仓库发布的分支，这时需要使用`fetch`指令更新仓库信息。建议在 Visual Studio Code 中开启自动定期`fetch`。

**push**

将本地的修改（本地的所有新提交）同步到远程代码仓库中，如果左下角的*版本状态*显示你的版本领先于远程版本，则可以直接推送，否则需要先进行`pull`操作。

**pull**

将远程代码仓库的修改同步到本地，如果远程与本地提交有冲突，会触发`merge`流程，这时需要手工将代码中的冲突消除。

如果在`pull`本地存在未提交的修改并且不想提交，则需要使用`stash`暂存功能将代码暂时保存，在`pull`后`apply latest stash`将暂存内容应用到现在的代码中，如果存在冲突，解决冲突的流程会在这时候进行。

**checkout**

切换分支，直接点击 Visual Studio Code 左下角的分支名称，即可选择需要切换到的分支。

> 注意：切换分支前需要将本地未提交的修改提交，或者`stash`暂存当前分支的修改

**merge**

在 Visual Studio Code 版本管理页面中选择*分支/合并分支*，选择*合并自*的分支，可以将*合并自*分支的提交合并到本分支，这样就可以在网页上创建合并请求了。
