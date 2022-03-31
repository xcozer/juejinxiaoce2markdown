# juejinxiaoce2markdown
Python3 将掘金小册保存为本地 PDF （会处理图片）

## 使用指南
1. 安装依赖
    ```shell
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    ```
2. 安装wkhtmltopdf
    
   Debian/Ubuntu
    ```shell
    $ sudo apt-get install wkhtmltopdf
    ```
   
   macOS
   ```shell
   $ brew install homebrew/cask/wkhtmltopdf
   ```
4. 根据实际情况修改 config.yml
    ```yaml
    sessionid: "{这里填写自己的sessionid}" # 填写 cookie 里的 sessionid
    book_ids: # 要爬取的小册id(在url里可以找到)，必须是上面账号已购的小册
    #  - 6844733722936377351 # 深入理解 RPC : 基于 Python 自建分布式高并发 RPC 服务
    #  - 6844733712102326279 # 大厂 H5 开发实战手册
    #  - 6844733730678898702 # 基于 Go 语言构建企业级的 RESTful API 服务
    #  - 6844733718335062030 # 基于 Python 轻松自建 App 服务器
      - 6844733813021491207 # 深入浅出TypeScript：从基础知识到类型编程
      - 6844733800300150797 # 前端算法与数据结构面试：底层逻辑解读与大厂真题训练
      - 6897616008173846543 # 从 0 到 1 实现一套 CI/CD 流程
    save_dir: "book" # 保存小册的目录，默认会在当前目录下新建一个 book 目录
    ```
5. 运行主程序：`python3 main.py`
6. 爬取结果预览：
```
├── book
│   └── 深入浅出TypeScript：从基础知识到类型编程.pdf
├── config.yml
├── main.py
└── requirements.txt
```

## 后续问题
**20210120**
发现输入账号密码+拖动验证码无法登录，建议采用微信扫码登录