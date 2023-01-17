import requests
import json

config = json.load(open("./auto_upload.config"))
server = config["server"]
token = config["token"]

if config["disable_ssl"] is True:  # 判断是否开启忽略SSL 
    requests.urllib3.disable_warnings()
    server_verify = False
else:
    server_verify = True

def image_upload(image_path,permission,album_id):  # 上传一张图片，返回上传是否成功
    if permission == "public":  # 格式化permission参数为api所定义的值
        format_permission = 1
    else:
        format_permission = 0
    
    upload_header = {
        "Accept":"application/json",
        "Authorization":token,
    }
    upload_file = {
            "file":open(image_path,"rb"),
    }
    upload_data = {
            "permission":format_permission,
            "album_id":album_id
    }
    
    response = requests.post(url=server+"/api/v1/upload",files=upload_file,data=upload_data,headers=upload_header,verify=server_verify)
    if "status" in response.json():  # 判断是否上传成功
        if response.json()["status"] is True:
            return True
        else:
            return False
    else:
        return False

def get_album_id(album_name):  # 获取相册名对应的相册id
    get_header = {
        "Accept":"application/json",
        "Authorization":token,
    }
    get_params = {
        "q":album_name
    }
    
    response = requests.get(url=server+"/api/v1/albums",params=get_params,headers=get_header,verify=server_verify)
    if "status" in response.json():
        if response.json()["status"] is True:
            for album in response.json()["data"]["data"]:  # 遍历返回的结果，寻找完全匹配项
                if album["name"] == album_name:
                    return album["id"]
        else:
            return None
    else:
        return None