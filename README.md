# 钓鱼邮件测试演练平台

Django+celery+rabbitmq

## 安装部署
下载项目 安装依赖包
```
pip -r requirements.txt
```
安装mysql
进入mysql创建数据库

安装rabbitmq
```
sudo apt-get install erlang-nox
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install rabbitmq-server
```

### 修改settings.py
数据库配置
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phishing_test',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '2smilemysql',
    }
}
```
域名配置
```
WEB_URL = 'http://phishing.shishike.com/'
```

### 运行
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## 基本功能模块
- 目标管理
- 任务管理
- 邮件模板
- 钓鱼页面
- 发信配置
- 用户管理


## TODO
- [x] task增加报错处理
- [x] 钓鱼页面设定切换跳转
- [x] 分组详情列表
- [x] 添加目标处批量导入邮件发送目标
- [x] 丰富dashboard页面
- [x] 邮件池轮询发送
- [x] 列表搜索功能
- [x] 列表排序功能
- [x] 分组添加功能优化
- [ ] 日志功能
- [ ] 任务邮件通知
- [ ] 附件功能
