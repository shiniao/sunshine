# Pre-work - Todo List

使用django + Django Rest Framework + Vue + Ant Design构建。

### 已实现功能
- 列出所有待办事项
![todo_list](http://blog.shiniao.fun/todo_list.png)
- 添加待办事项(可添加优先级、截止时间)
- 删除待办事项
- 编辑待办事项(可设置优先级、截止时间) 
![todo_edit](http://blog.shiniao.fun/todo_edit.png)
- 标记已完成
- 登录功能(不用用户不同内容)
![todo_login](http://blog.shiniao.fun/todo_login.png)
- 翻页功能
- 按照优先级、截止时间排序
![todo_sort](http://blog.shiniao.fun/todo_sort_p.png)

### 待实现功能
- 用户注册

### api接口
- /todos/a/  获取所有todos, create todo
- /todos/a/<id>/ 单个todo操作(get/put/delete)
- /todos/f/ 获取已完成todo
- /todos/d/ 分页获取todo(按创建时间排序)
- /todos/e/ 分页获取todo(按截止时间排序)
- /todos/p/ 分页获取todo(按优先级排序)

### how to run
```shell script
# server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

# client
npm install
npm run serve
```

### License
此项目为九章算法实习Pre work: Todo List，请遵守License.

[MIT License](https://opensource.org/licenses/mit-license.php)
