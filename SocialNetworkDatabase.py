# coding=utf-8
import os
import re
import glob
import json
import time
import random
import hashlib
import threading


class SNDB(object):
    """docstring for SNDB."""
    data = {
        'hash': {},  # 解释(group,person,item,value,gender,date,time,)
        'relation': {},  # 关系
        'config': {
            'item_order': []
        }  # 设置
    }
    path = '.\\DB\\tmp.db'
    current_relation_hash = ''

    def __init__(self, debug=False):
        super(SNDB, self).__init__()
        self.debug = debug

    # file
    def load(self, path):
        self.path = path
        with open(path, 'r') as dbfile:
            self.data = json.loads(dbfile.read())

    def save(self):
        with open(self.path, 'w') as dbfile:
            dbfile.write(json.dumps(self.data))

    # public
    def add_relation(self, name, SNDB_type='person'):
        self.current_relation_hash = self.generate_hash()
        self.data['relation'][self.current_relation_hash] = {}
        self.data['hash'][self.current_relation_hash] = (name, SNDB_type)
        return self.current_relation_hash

    def choose_relation(self, ash):
        if len(self.get_hash_by_ash(ash)) == 1:
            self.current_relation_hash = self.get_hash_by_ash(ash)[0]

    def add_item(self, name, value, SNDB_type='value'):
        name_hash = self.generate_hash()
        value_hash = self.generate_hash()
        self.data['relation'][self.current_relation_hash][
            name_hash] = value_hash
        self.data['hash'][name_hash] = (name, 'item')
        self.data['hash'][value_hash] = (value, SNDB_type)

    def change_value(self, item_hash, value_hash, SNDB_type):
        self.data['relation'][item_hash] = value_hash

    def del_relation(self, hash):
        del self.data['relation'][hash]

    def del_item(self, hash):
        del self.data['relation'][hash]

    def del_value(self, hash):
        del self.data['relation'][hash]

    def del_hash(self, hash):
        del self.data['hash'][hash]

    # tool
    def get_all_reference(self):
        tmp = set()
        for a in self.data['relation'].keys():
            tmp.add(a)
            for b in self.data['relation'][a].keys():
                tmp.add(b)
                if isinstance(self.data['relation'][a][b], str):
                    tmp.add(isinstance(self.data['relation'][a][b])
                elif isinstance(self.data['relation'][a][b], list):
                    for c in isinstance(self.data['relation'][a][b]:
                        tmp.add(c)
        return tmp

    def add_hash(self, hash, value, SNDB_type):
        self.data['hash'][hash]=(value, SNDB_type)

    def generate_hash(self):
        m=hashlib.md5()
        m.update(str(time.time()).encode("utf-8"))
        m.update(str(random.random()).encode("utf-8"))
        return m.hexdigest()

    def search_hash(self, name, SNDB_type):
        answer=[]
        for each in self.data['hash'].keys():
            if self.data['hash'][each][0] == name and self.data['hash'][each][1] == SNDB_type:
                answer.append(each)
        return answer

    def get_hash_by_name(self, name):
        answer=[]
        for each in self.data['hash'].keys():
            if self.data['hash'][each][0] == name:
                answer.append(each)
        return answer

    def get_hash_by_ash(self, ash):  # 获得含有ash的hash列表
        answer=[]
        for each in self.data['hash'].keys():
            if re.match(ash, each):
                answer.append(each)
        return answer

    def get_ash_by_hash(self, hash):  # 获得唯一的ash字符串
        if isinstance(hash, str):
            order=1
            for each in self.data['hash'].keys():
                while re.match(hash[0:order], each):
                    if each == hash:
                        break
                    else:
                        order += 1
            return hash[0:order]
        elif isinstance(hash, list):
            new_list=[]
            for every in hash:
                order=1
                for each in self.data['hash'].keys():
                    while re.match(every[0:order], each):
                        if each == every:
                            break
                        else:
                            order += 1
                new_list.append(each[0:order])
            return new_list

    def check_broken(self):
        pass

    def check_lost(self):
        pass


class InteractiveSNDB(SNDB):
    """docstring for InteractiveSNDB."""
    isRunning={}

    def __init__(self, debug=False):
        def input_star():
            while self.isRunning['InteractiveSNDB']:
                cmd=input('>')
                if cmd == '':
                    continue
                cmd=cmd.split(' ')
                if cmd[0] == 'exit' or cmd[0] == 'quit':
                    print('即将退出，是否保存？[Y/n]')
                    cmd=input('>')
                    if cmd == 'n' or cmd == 'N':
                        pass
                    else:
                        self.save()
                    self.isRunning['InteractiveSNDB']=False
                elif cmd[0] == 'save':
                    self.save()
                elif cmd[0] == 'show':
                    if cmd[1] == 'all':
                        print('Realtions' + '-' * 30)
                        for each in self.data['relation'].keys():
                            print(' ' + self.get_ash_by_hash(each) + ':')
                            for every in self.data['relation'][each].keys():
                                print('  ' + self.get_ash_by_hash(every) + ':',
                                      self.get_ash_by_hash(self.data['relation'][each][every]))
                        print('Hashes' + '-' * 30)
                        for each in self.data['hash'].keys():
                            print(' ' + self.data['hash'][each][0],
                                  self.data['hash'][each][1], self.get_ash_by_hash(each))
                    elif cmd[1] == 'hash':
                        for each in self.data['hash'].keys():
                            print(self.data['hash'][each][0],
                                  self.data['hash'][each][1], each)
                    elif cmd[1] == 'json':
                        print(self.data)
                    elif cmd[1] == 'current':
                        print(self.data['hash'][self.current_person_hash][0])
                    elif cmd[1] == 'person':
                        for each in self.data['relation'].keys():
                            if self.data['hash'][each][1] == 'person':
                                print(self.data['hash'][each][0])
                elif cmd[0] == 'add':
                    if cmd[1] == 'person':
                        self.addRelation(cmd[2])
                    elif cmd[1] == 'man':
                        self.addRelation(cmd[2])
                        self.addItem('性别', '男')
                    elif cmd[1] == 'woman':
                        self.addRelation(cmd[2])
                        self.addItem('性别', '女')
                    elif cmd[1] == 'item':
                        self.addItem(cmd[2], cmd[3])
                elif cmd[0] == 'delete':
                    if cmd[1] == 'person':
                        self.deleteRelation(cmd[2])
                    elif cmd[1] == 'item':
                        self.deleteItem(cmd[2])
        super(InteractiveSNDB, self).__init__(debug)
        self.isRunning['InteractiveSNDB']=True
        if not os.path.exists('Import'):
            os.mkdir('Import')
        if not os.path.exists('DB'):
            os.mkdir('DB')
        dbs=glob.glob('.\DB\*.db')
        # dbs的转义
        if len(dbs) == 0:
            pass
        elif len(dbs) == 1:
            dbs=dbs[0]
            self.load(dbs)
        else:
            for i, each in enumerate(dbs):
                print('{}:{}'.format(i + 1, each))
            choice=int(input('>'))
            dbs=dbs[choice - 1]
            self.load(dbs)
        t_star=threading.Thread(target=input_star)
        t_star.start()
        t_star.join()

    def addRelation(self, name):
        hash_list=self.get_hash_by_name(name)
        if len(hash_list) == 0:
            self.add_relation(name)
        else:
            print('查到了{}个。'.format(len(hash_list)))
            print('0:新建')
            for i, each in enumerate(hash_list):
                print('{}:{}:{}:{}'.format(
                    i + 1, self.data['hash'][each][0], self.data['hash'][each][1], self.get_ash_by_hash(each)))
            cmd=input('>')
            if cmd.isdigit():
                cmd=int(cmd)
                if cmd == 0:
                    self.add_relation(name)
                else:
                    self.choose_relation(hash_list[cmd - 1])

    def addItem(self, item, value):
        # 对Item查重
            # 确定Item的hash
        # 是否已存在Item
            # 询问合并
        # 对value查重
            # 确定value的hash
        # 是否已存在value
            # 询问合并
        hash_list=self.get_hash_by_name(item)
        item_hash=self.generate_hash()
        if len(hash_list) > 0:
            print('查到了Item {}个。'.format(len(hash_list)))
            print('0:新建')
            for i, each in enumerate(hash_list):
                print('{}:{}:{}:{}'.format(
                    i + 1, self.data['hash'][each][0], self.data['hash'][each][1], self.get_ash_by_hash(each)))
            cmd=input('>')
            if cmd.isdigit():
                cmd=int(cmd)
                if cmd > 0:
                    item_hash=hash_list[cmd - 1]
            else:
                print('!')
        hash_list=self.get_hash_by_name(value)
        value_hash=self.generate_hash()
        if len(hash_list) > 0:
            print('查到了Value {}个。'.format(len(hash_list)))
            print('0:新建')
            for i, each in enumerate(hash_list):
                print('{}:{}:{}:{}'.format(
                    i + 1, self.data['hash'][each][0], self.data['hash'][each][1], self.get_ash_by_hash(each)))
            cmd=input('>')
            if cmd.isdigit():
                cmd=int(cmd)
                if cmd > 0:
                    value_hash=hash_list[cmd - 1]
            else:
                print('!')
        if item_hash in self.data['relation'][self.current_relation_hash].keys():
            item_name=self.data['hash'][item_hash][0]
            if isinstance(self.data['relation'][self.current_relation_hash][item_hash], str):
                value_name=self.data['hash'][self.data['relation'][
                    self.current_relation_hash][item_hash]][0]
                value_type='str'
            elif isinstance(self.data['relation'][self.current_relation_hash][item_hash], list):
                new_list=[]
                for each in self.data['relation'][self.current_relation_hash][item_hash]:
                    new_list.append(self.data['hash'][each])
                value_name=new_list
                value_type='list'
            print('该关系已存在一个“{}:{}”，是合并还是替换？'.format(item_name, value_name))
            print('1:合并')
            print('2:替换')
            cmd=input('>')
            if cmd == '1':
                if value_type == 'str':
                    self.data['relation'][self.current_relation_hash][item_hash]=[
                        self.data['relation'][self.current_relation_hash][item_hash], value_hash]
                elif value_type == 'list':
                    self.data['relation'][self.current_relation_hash][
                        item_hash].append(value_hash)
            elif cmd == '2':
                self.data['relation'][self.current_relation_hash][
                    item_hash]=value_hash
            return
        self.data['relation'][self.current_relation_hash][
            item_hash]=value_hash
        self.add_hash(item_hash, item, 'item')
        self.add_hash(value_hash, value, 'value')
if __name__ == '__main__':
    InteractiveSNDB(True)
