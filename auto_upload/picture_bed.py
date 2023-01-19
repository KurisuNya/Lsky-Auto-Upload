import requests
import json


# 加载全局参数
config = json.load(open("auto_upload.config"))
server = config["server"]
token = config["token"]
# 判断是否开启忽略SSL 
if config["disable_ssl"] is True:  
    requests.urllib3.disable_warnings()
    server_verify = False
else:
    server_verify = True


def image_upload(image_path,permission,album_id):  
    """
    image_upload 根据传输参数调用api上传图片

    Args:
        image_path (_string_): 图片路径
        permission (_string_): 图片权限，public/private 
        album_id (_int_): 相册id

    Returns:
        _bool_: 上传是否成功
    """
    # 格式化permission参数为api所定义的值
    if permission == "public":  
        format_permission = 1
    else:
        format_permission = 0
    # 设置POST参数
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
    # POST上传图片   
    response = requests.post(url=server+"/api/v1/upload",files=upload_file,data=upload_data,headers=upload_header,verify=server_verify)
    # 判断是否上传成功
    if "status" in response.json():  
        if response.json()["status"] is True:
            return True
        else:
            return False
    else:
        return False


def get_album_id(album_name):  
    """
    get_album_id 获取相册id

    Args:
        album_name (_string_): 相册名称

    Returns:
        _int_ or None: 对应的相册id，找不到时返回None 
        
    TODO:
        修改返回参量以改善代码逻辑，避免在获取相册id时无法连接服务器导致相册内的图片全部传入默认位置
    """
    # 设置GET参数
    get_header = {
        "Accept":"application/json",
        "Authorization":token,
    }
    get_params = {
        "q":album_name
    }
    # GET获取相册id
    response = requests.get(url=server+"/api/v1/albums",params=get_params,headers=get_header,verify=server_verify)
    # 判断是否找到相册id
    if "status" in response.json():
        if response.json()["status"] is True:
            for album in response.json()["data"]["data"]:  
                if album["name"] == album_name:
                    return album["id"]
        else:
            return None
    else:
        return None