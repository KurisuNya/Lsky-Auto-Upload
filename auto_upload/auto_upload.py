import picture_bed
import json
import os
import shutil
import time


def album_upload(album_config):
    album_id = picture_bed.get_album_id(album_config["name"])  # 无法找到相册id时上传至默认目录
    album_path = album_config["path"]
    album_permision = album_config["permision"]
    album_delete_image = album_config["delete_image"]
    album_time_rename = album_config["time_rename"]
    for root, dirs, files in os.walk(album_path, topdown=False):  # 遍历整个目录及其子目录的文件
        for name in files:
            file_path = os.path.join(root, name)  # 合成文件路径
            if ("unsupported_files" not in file_path) & ("uploaded_images" not in file_path):  # 忽略unsupported_files与uploaded_images文件夹
                if check_image(name) is True:  # 检查文件后缀名
                    if album_time_rename is True:  # 若album_time_rename为true，重命名图片
                        file_path = time_rename(file_path)
                    response = picture_bed.image_upload(file_path, album_permision, album_id)
                    if response & album_delete_image is True:  # 若delete_image为true,删除图片
                        os.remove(file_path)
                    elif response & album_delete_image is False:  # delete_image为false,移动图片至uploaded_images文件夹
                        file_path = time_rename(file_path)  # 强制时间戳重命名，避免名称重复
                        uploaded_path = os.path.join(album_path, "uploaded_images")
                        if "uploaded_images" not in os.listdir(album_path):
                            os.mkdir(uploaded_path)
                        shutil.move(file_path, uploaded_path)
                else:  # 后缀名不满足要求，移动至unsupported_files文件夹
                    file_path = time_rename(file_path)  # 强制时间戳重命名，避免名称重复
                    move_path = os.path.join(album_path, "unsupported_files")
                    if "unsupported_files" not in os.listdir(album_path):
                        os.mkdir(move_path)
                    shutil.move(file_path, move_path)


def check_image(file_name):  # 检查文件后缀名
    file_suffix = os.path.splitext(file_name)[1].lower()
    allow_suffix = {".jpeg", ".jpg", ".png", ".gif",
                    ".tif", ".bmp", ".ico", ".psd", ".webp"}
    if file_suffix in allow_suffix:
        return True
    else:
        return False


def get_current_time():  # 时间格式化为时间戳
    current_time = time.time()
    local_time = time.localtime(current_time)
    data_head = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
    data_secs = (current_time - int(current_time)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs)
    return time_stamp


def time_rename(file_path):  # 时间戳重命名
    time_stamp = get_current_time()
    file_spilt = os.path.splitext(file_path)
    file_suffix = file_spilt[1].lower()
    file_root = os.path.dirname(file_path)
    rename_path = os.path.join(file_root, time_stamp+file_suffix)
    os.rename(file_path, rename_path)
    return rename_path


if __name__ == "__main__":
    config = json.load(open("./auto_upload.config"))
    albums = config["albums"]
    for album_config in albums:
        album_upload(album_config)
