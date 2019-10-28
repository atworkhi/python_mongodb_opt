# _*_coding:utf-8_*_
# ==========================================
#   FileName:Hello.py
#   User: hanxx
#   Date: 2019/9/12
#   Desc: 数据库操作
# ===========================================
from pymongo import MongoClient


class DataBaseOpt(object):
    # 数据增删改查操作
    def __init__(self):
        # 数据库的初始化连接
        client = MongoClient()
        database = client.Hello
        self.handler = database.data_03  # 被其他函数调用

    def query_all(self):
        # 查询所有字段 去掉删除(标记为0)，隐藏_id
        info_list = list(self.handler.find({'deleted': 0}, {'_id': 0}))
        return info_list

    def query_last_id(self):
        # 查询最大ID 用于新添加数据，在原始ID+1
        last = self.handler.find({}, {'_id': 0, 'id': 1}).sort('id', -1).limit(1)
        return last[0]['id'] if last else 0

    def add_info(self, para_dict):
        # 添加
        id = self.query_last_id() + 1
        para_dict['id'] = id
        try:
            self.handler.insert_one(para_dict)
        except Exception as e:
            print("插入数据失败：{}".format(e))
            return False
        return True

    def update_info(self, people_id, para_dict):
        # 更新数据
        try:
            p = self.handler.update({'id': people_id}, {'$set': para_dict})
            print(p)
        except Exception as e:
            print("更新错误:{}".format(e))
            return False
        return True

    def del_info(self, people_id):
        # 删除数据 增加deleted字段并设置为1
        return self.handler.update({'id': people_id}, {'$set': {'deleted': 1}})
