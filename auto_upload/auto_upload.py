import picture_bed
import json
import os
import shutil
import time


def album_upload(album_config):
    """
    Usage:
        根据输入的album_config内的相册参数进行图片上传
    
    Args:
        album_config (_dict_):{
            "name": _str_ ,  # 相册名称 
            "path": _str_ ,  # 相册文件夹路径
            "permission": _str_ ,  # 图片权限-"public"或"private" 
            "delete_image": _bool_ ,  # 是否在上传后删除图片
            "time_rename": _bool_  # 是否使用时间戳重命名文件
        }
    """
    # 相册参数设置
    album_id = picture_bed.get_album_id(album_config["name"])  
    album_path = album_config["path"]
    album_permission = album_config["permission"]
    album_delete_image = album_config["delete_image"]
    album_time_rename = album_config["time_rename"]
    # 判断是否成功get相册id
    if album_id["get_status"] is True:
        album_id = album_id["album_id"]
        # 遍历相册路径
        for root, dirs, files in os.walk(album_path, topdown=False):  
            for name in files:
                file_path = os.path.join(root, name)  
                # 忽略目录下unsupported_files与uploaded_images文件夹
                if ("unsupported_files" not in file_path) & ("uploaded_images" not in file_path):  
                    # 检测文件格式是否支持
                    if check_image(name) is True:  
                        # 设置项检测：时间戳重命名
                        if album_time_rename is True:  
                            file_path = time_rename(file_path)
                        # 图片上传
                        response = picture_bed.image_upload(file_path, album_permission, album_id)
                        # 设置项检测：删除上传图片
                        if response & album_delete_image is True:  
                            os.remove(file_path)
                        elif response & album_delete_image is False:  
                            uploaded_path = os.path.join(album_path, "uploaded_images")
                            if "uploaded_images" not in os.listdir(album_path):
                                os.mkdir(uploaded_path)
                            if os.path.exists(os.path.join(uploaded_path,os.path.basename(file_path))):
                                file_path = name_add_time(file_path)
                            shutil.move(file_path, uploaded_path)
                    else:  
                        move_path = os.path.join(album_path, "unsupported_files")
                        if "unsupported_files" not in os.listdir(album_path):
                            os.mkdir(move_path)
                        if os.path.exists(os.path.join(move_path,os.path.basename(file_path))):
                            file_path = name_add_time(file_path)
                        shutil.move(file_path, move_path)


def check_image(file_name):
    """
    Usage:
        检查文件格式是否支持

    Args:
        file_name (_str_): 文件名称

    Returns:
        _bool_: 文件格式是否支持
    """
    file_suffix = os.path.splitext(file_name)[1].lower()
    allow_suffix = {".jpeg", ".jpg", ".png", ".gif",
                    ".tif", ".bmp", ".ico", ".psd", ".webp"}
    if file_suffix in allow_suffix:
        return True
    else:
        return False


def get_current_time():  
    """
    Usage:
        返回格式为"Y-M-D-H-M-S-MS"的时间戳

    Returns:
        _str_: 当前时间时间戳 
    """
    current_time = time.time()
    local_time = time.localtime(current_time)
    data_head = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
    data_secs = (current_time - int(current_time)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs)
    return time_stamp


def time_rename(file_path):  
    """
    Usage:
        使用时间戳重命名文件

    Args:
        file_path (_str_): 文件路径 

    Returns:
        _str_ : 重命名后的文件路径 
    """
    time_stamp = get_current_time()
    file_spilt = os.path.splitext(file_path)
    file_suffix = file_spilt[1].lower()
    file_root = os.path.dirname(file_path)
    rename_path = os.path.join(file_root, time_stamp+file_suffix)
    os.rename(file_path, rename_path)
    return rename_path


def name_add_time(file_path):
    """
    Usage:
        在文件名称结尾添加时间戳

    Args:
        file_path (_str_): 文件路径 

    Returns:
        _str_ : 重命名后的文件路径 
    """
    time_stamp = get_current_time()
    file_spilt = os.path.splitext(os.path.basename(file_path))
    file_name = file_spilt[0]
    file_suffix = file_spilt[1].lower()
    file_root = os.path.dirname(file_path)
    rename_path = os.path.join(file_root,file_name+"_"+time_stamp+file_suffix)
    os.rename(file_path, rename_path)
    return rename_path


if __name__ == "__main__":
    # 加载相册参数
    config = json.load(open("auto_upload.config"))
    albums = config["albums"]
    # 对不同相册进行上传
    for album_config in albums:
        album_upload(album_config)
