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
        self.current_relation_hash = self.get_hash_by_ash(ash)

    def add_item(self, name, value, SNDB_type='value'):
        name_hash = self.generate_hash()
        value_hash = self.generate_hash()
        self.data['relation'][self.current_relation_hash][
            name_hash] = value_hash
        self.data['hash'][name_hash] = (name, 'item')
        self.data['hash'][value_hash] = (value, SNDB_type)

    # tool
    def add_hash(self, hash, value, SNDB_type):
        self.data['hash'][hash] = (value, SNDB_type)

    def generate_hash(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode("utf-8"))
        m.update(str(random.random()).encode("utf-8"))
        return m.hexdigest()

    def search_hash(self, name, SNDB_type):
        answer = []
        for each in self.data['hash'].keys():
            if self.data['hash'][each][0] == name and self.data['hash'][each][1] == SNDB_type:
                answer.append(each)
        return answer

    def get_hash_by_name(self, name):
        answer = []
        for each in self.data['hash'].keys():
            if self.data['hash'][each][0] == name:
                answer.append(each)
        return answer

    def get_hash_by_ash(self, ash):  # 获得含有ash的hash列表
        answer = []
        for each in self.data['hash'].keys():
            if re.match(ash, each):
                answer.append(each)
        return answer

    def get_ash_by_hash(self, hash):  # 获得唯一的ash字符串
        order = 1
        for each in self.data['hash'].keys():
            while re.match(hash[0:order], each):
                if each == hash:
                    break
                else:
                    order += 1
        return hash[0:order]

    def check_broken(self):
        pass

    def check_lost(self):
        pass


class InteractiveSNDB(SNDB):
    """docstring for InteractiveSNDB."""
    isRunning = {}

    def __init__(self, debug=False):
        def input_star():
            while self.isRunning['InteractiveSNDB']:
                cmd = input('>')
                if cmd == '':
                    continue
                cmd = cmd.split(' ')
                if cmd[0] == 'exit' or cmd[0] == 'quit':
                    print('即将退出，是否保存？[Y/n]')
                    cmd = input('>')
                    if cmd == 'n' or cmd == 'N':
                        pass
                    else:
                        self.save()
                    self.isRunning['InteractiveSNDB'] = False
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
                        self.add_relation(cmd[2])
                    elif cmd[1] == 'man':
                        self.add_relation(cmd[2])
                        self.add_item('性别', '男')
                    elif cmd[1] == 'woman':
                        self.add_relation(cmd[2])
                        self.add_item('性别', '女')
                    elif cmd[1] == 'item':
                        self.add_item(cmd[2], cmd[3])
                else:
                    pass
        super(InteractiveSNDB, self).__init__(debug)
        self.isRunning['InteractiveSNDB'] = True
        if not os.path.exists('DB'):
            os.mkdir('DB')
        dbs = glob.glob('.\DB\*.db')
        # dbs的转义
        if len(dbs) == 0:
            pass
        elif len(dbs) == 1:
            dbs = dbs[0]
            self.load(dbs)
        else:
            for i, each in enumerate(dbs):
                print('{}:{}'.format(i + 1, each))
            choice = int(input('>'))
            dbs = dbs[choice - 1]
            self.load(dbs)
        t_star = threading.Thread(target=input_star)
        t_star.start()
        t_star.join()

if __name__ == '__main__':
    InteractiveSNDB(True)
