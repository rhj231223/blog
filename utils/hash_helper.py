import hashlib

class Hash_Pwd(object):

    def __init__(self,salt='qiangsheng'):
        self.salt=salt.encode('utf8')

    def hash_pwd(self,raw_pwd):
        if not raw_pwd:
            return False

        raw_pwd=raw_pwd.encode('utf8')
        return hashlib.sha1(raw_pwd+self.salt).hexdigest()




    def check_pwd(self,raw_pwd,hash_pwd):
        return self.hash_pwd(raw_pwd)==hash_pwd



if __name__=='__main__':
    pwd=Hash_Pwd()
    a=pwd.hash_pwd('jw231223')
    print(pwd.check_pwd('jw231223',a))