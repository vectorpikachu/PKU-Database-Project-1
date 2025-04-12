# Flask 使用说明

## 最简单的程序

当前的目录为:
```
flask_app/
   app.py
```

app.py 的内容为:
```python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'
if __name__ == '__main__':
    app.run()
```

通过运行:
```
python app.py
```

或者运行:
```
flask run
```

就可以开始运行这个app了.


## View Function (视图函数)

所谓的“注册”，就是给这个函数戴上一个装饰器帽子。我们使用 `app.route()` 装饰器来为这个函数绑定对应的 URL，当用户在浏览器访问这个 URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：
```python
@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'
```

### 添加 HTML 元素

返回值作为响应的主体，默认会被浏览器作为 HTML 格式解析，所以我们可以添加一个 HTML 元素标记：
```python
@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
```

### 修改 URL 规则

另外，你也可以自由修改传入 `app.route` 装饰器里的 `URL` 规则字符串，但要注意以斜线 `/` 作为开头。比如：
```python
@app.route('/hello')
def hello():
    return 'Hello, World!'
```

一个视图函数也可以绑定多个 URL，这通过附加多个装饰器实现，比如：
```python
@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return 'Welcome to My Watchlist!'
```

前面，我们之所以把传入 `app.route` 装饰器的参数称为 URL 规则，是因为我们也可以在 URL 里定义变量部分。比如下面这个视图函数会处理所有类似 `/user/<name>` 的请求：
```python
@app.route('/user/<name>')
def user(name):
    return 'Hello'
```

不论你访问 `/user/greyli`，还是 `/user/peter`，抑或是 `/user/甲`，都会触发这个函数。通过下面的方式，我们也可以在视图函数里获取到这个变量值：
```python
from markupsafe import escape

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'
```

> 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用 `MarkupSafe`（Flask 的依赖之一）提供的 `escape()` 函数对 `name` 变量进行转义处理，比如把 `<` 转换成 `&lt;`。这样在返回响应时浏览器就不会把它们当做代码执行。

## 发现程序

如果你把上面的程序保存成其他的名字，比如 `hello.py`，接着执行 `flask run` 命令会返回一个错误提示。这是因为 Flask 默认会假设你把程序存储在名为 `app.py` 或 `wsgi.py` 的文件中。如果你使用了其他名称，就要设置系统环境变量 `FLASK_APP` 来告诉 Flask 你要启动哪个程序：
```bash
export FLASK_APP=hello.py
flask run
```

或者在 Windows CMD 上:
```bash
set FLASK_APP=hello.py
flask run
```
或者在 PowerShell 上:
```bash
$env:FLASK_APP = "hello.py"
flask run
```




