### 必应壁纸API
通过github actions 自动从必应壁纸API中获取壁纸数据,并存储在data目录下.
当前仅支持重定向至必应URL, 不支持返回JSON数据.

#### "/today" 接口
    - 入参: location  可选参数,默认为zh-CN 地区编码 请查看settings.py 中的 LOCATION 字典
    - 出参: 重定向至URL
##### 接口说明: 
     返回当天的壁纸URL. 如果没有location参数,则默认访问zh-CN地区的壁纸.

#### "/random" 接口
    - 入参: location  可选参数 请查看settings.py 中的 LOCATION 字典
    - 出参: 重定向至URL
##### 接口说明: 
     返回随机的壁纸URL. 如果没有location参数,则随机选择一个location. 然后从文件中取出所有数据,从读取的数据中随机取一个url , 并重定向至URL.

#### data 目录
    - 目录下有多个json文件,每个文件对应一个地区的壁纸数据.
    - 以location-today.json 命名的文件为每个地区的今日壁纸数据文件,其中location为地区编码.
    - 每个json文件的文件名格式为 location.json, 其中location为地区编码.
    - 每个json文件的内容为一个列表,列表中每个元素为一个字典,字典包含以下字段:
        - url: 壁纸的URL
        - title: 壁纸的标题
        - copyright: 壁纸的版权信息
        - copyrightlink: 壁纸的版权链接
        - startdate: 壁纸的开始日期
        - enddate: 壁纸的结束日期
