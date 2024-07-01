from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings
# from topic.models import Annex


class FDFSStorage(Storage):
    '''fastdfs文件存储类'''

    def __init__(self, client_conf=None, base_url=None):
        '''初始化'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_config = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        '''打开文件'''
        pass

    def _save(self, name, content):
        '''保存文件时使用'''
        # name: 选择上传文件的名字
        # content: 包含上传文件内容的File类对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_config)

        # 上传文件到fastdfs
        # print("------name-------")
        # print(name)
        # print("------content-------")
        # print(content)
        ret = client.upload_by_buffer(content.read())
        # ret = client.upload_by_file()
        '''
        @return dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : '',
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        } if success else None
        '''
        if ret.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到FastDFS失败')

        # print("------ret-------")
        # print(ret)
        # print("-----filename------")
        # 获取返回的文件ID
        filename = ret.get('Remote file_id')
        # print(filename)
        # name = name.replace("fdfs/", "")
        return filename

    def exists(self, name):
        '''判断文件名是否可用'''
        return False

    def url(self, name):
        '''返回url路径'''
        return self.base_url + name

    def upload(self, local_path):
        """
        将文件上传到fastdfs分布式文件系统中
        :param local_path: 上传文件的本地路径
        :return:
        """
        client = Fdfs_client(self.client_config)
        ret = client.upload_by_file(local_path)
        print(ret)
        if ret.get("Status") != "Upload successed.":
            raise Exception("upload file failed")
        remote_file_id = ret.get("Remote file_id")

        print("存储在fastdfs上的文件路径：", remote_file_id)

        return True, remote_file_id
