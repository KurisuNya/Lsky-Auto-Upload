# Lsky-Auto-Upload

基于兰空图床V2企业版api编写的自动上传脚本

## 使用注意

发现配置在服务器上时无法找到`auto_upload.config`文件时，可以参考以下解决方法。

解决方法：

* 方法一：将`auto_upload.py`与`picture_bed.py`内`auto_upload.config`文件的路径修改为绝对路径。
* 方法二：在运行脚本前通过`cd`命令将目录移至脚本所在目录。
* 方法三：使用systemd管理服务，设置WorkingDirectory为脚本所在目录。

## 配置文件格式

```json
{
    "server":"https://127.0.0.1",  // 填入你的服务器url,末尾不能带'/'
    "disable_ssl":false,  // 用于局域网内上传，若通信协议为https，则此字段有效
    "token":"your_token",  // 例如："Bearer 1|xxxxxxxxxxx"
    "albums":
    [
        {
            "name":"",  // 填入相册名称,若为空或找不到对应相册则自动上传至默认路径
            "path":"",  // 填入备份文件夹路径,支持绝对路径与相对路径
            "permission":"private",  // 图片是否公开,可选择"private"或"public"
            "time_rename":true,  // 仅控制上传前是否按时间戳重命,反映在图床内图片名称
            					 // 文件移动时为避免文件名称重复强制重命名 
            "delete_image":false  // 上传后是否删除本地图片
        },
        {  // 你可以配置多备份文件夹路径
            "name":"test",
            "path":".\test",
            "permission":"private",
            "time_rename":true,
            "delete_image":false
        }
    ]
}
```

## 兰空图床官网

[兰空图床](https://www.lsky.pro/)
