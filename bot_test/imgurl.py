from qiniu import Auth, put_file

def imgurlget(localfile:str,key:str):
    # 获取Access Key 和 Secret Key 后，进行初始化对接：
    q = Auth(access_key='',
         secret_key='')

    # 上传的七牛云空间
    bucket_name = 'bicuisi'

    # 上传后保存的文件名
    #key=

    # 生成上传token
    token = q.upload_token(bucket_name, key)

    # 要上传文件的路径
    #localfile = './126_30003.jpg'

    ret, info = put_file(token, key, localfile)

    # 拼接路径   qj5s0uqce.hb-bkt.clouddn.com这个是创建空间分配的测试域名
    image_file = 'http://rh3nkqn8l.hn-bkt.clouddn.com/' + ret.get('key')
    return image_file

