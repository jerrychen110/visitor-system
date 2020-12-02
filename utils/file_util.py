# coding: utf-8
import os
import shutil
import json


def _scan_dir(dir_path, prefix=None, postfix=None):
    files_list = []

    for root, sub_dirs, files in os.walk(dir_path):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list


def _copy_file(from_path, to_path):
    if os.path.exists(from_path):
        shutil.copy(from_path, to_path)


def _delete_all(file_path):
    filelist = os.listdir(file_path)
    for f in filelist:
        filepath = os.path.join(file_path, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(str(filepath)+ " removed")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
            print("dir "+str(filepath)+" removed")
    shutil.rmtree(file_path,True)
    print("removed all")


def _check_file(file_path, file_name):
    file_list = []
    for f in os.listdir(file_path):
        filepath = os.path.join(file_path, f)
        if os.path.isdir(filepath):
            _check_file(filepath, file_name)
        if os.path.isfile(filepath):
            if file_name in f:
                file_list.append(filepath)
    return file_list


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def replace_china(_input_str):
    result = ''

    for item in _input_str:
        if '\u4e00' <= item <= '\u9fff':
            result += str(hex(ord(item)))
        else:
            result += item

    return result


def is_json(myjsonstr):
    try:
        json.loads(myjsonstr)
    except ValueError:
        return False
    return True
