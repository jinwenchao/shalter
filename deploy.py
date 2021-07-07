#!/user/bin/python
# -*- coding=utf-8 -*-
#
# Copyright : Copyright 2021 Inc
# File      : deploy.py
# Introduce : 本文件为升级部署脚本程序,通过指定的后缀进行判断部署操作
#             1 前端程序 默认zip结尾
#             2 后端程序 默认tar结尾
#             1 配置文件 默认yml结尾
# Version   : V1.0.1
# Author    : wenchao jin
# Time      : 2021-06-08

import os
import sys
import time
def oper_file():
  path = os.getcwd()
  #print(path)
  for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
      if name[-3:] == "tar":
        '''
        stup 1 拷贝现有文件    - ansible jgxt3 -m copy -a "src=user-service-center.tar dest=/data/images/ backup=yes"
             2 删除当前镜像    - docker rmi -f IMAGE ID -  IMAGE ID
             3 加载新的镜像文件 - docker load < isgs-camunda-rest.tar - 此步骤执行报错
             4 重新打标签 -docker tag 10.18.101.162:9081/isgs/user-center-manger:1.0 192.168.1.15:5000/gajg/user-center-manger:1.0 
             5 推送镜像到服务器 - docker push 192.168.1.15:5000/gajg/isgs-camunda-rest:1.0
             6 重新加载部署    - docker stack deploy --with-registry-auth -c isgs-camunda-rest.yml isgs-app
        '''
        print("===================后端部署文件:" + name[:-4] + " 已开始升级部署===================")
        cmd_copy = 'ansible jgxt3 -m copy -a ' + '\"src=' + name + ' dest=/data/images/ backup=yes\"'
        os.system(cmd_copy)
        code_image = 'ansible jgxt3 -m shell -a ' + '\"docker images | awk '+'\''+ '/'+  name[:-4]  + '/'+ '\'' + '| awk '+ '\''+'{print $3}'+'\'' +'| awk '+ '\'' + 'NR==1'+'\'' +'\"'
        os.system(code_image)
        output = os.popen(code_image)
        info = output.readlines()
        image_id = " "
        for line in info:
          print(line.strip('\r\n'))
          img_id = line.split(" ")

          for i in range(len(img_id)):
            if len(img_id[i]) == 12 and str.isalnum(img_id[i]):
              image_id = img_id[i]

        delete_image = 'ansible jgxt3 -m shell -a' + ' \"docker rmi -f ' + image_id +'\"'
        os.system(dele_image)
        load_image = 'ansible jgxt3 -m shell -a' + ' \"chdir=/data/images docker load < ' + name + '\"'
        os.system(load_image)
        tag_image = 'ansible jgxt3 -m shell -a' + ' \"docker tag 10.18.101.162:9081/isgs/' + name[:-4] + ':1.0 192.168.1.15:5000/gajg/' + name[:-4] + ':1.0\"'
        os.system(tag_image)
        push_image = 'ansible jgxt3 -m shell -a' + ' \"docker push 192.168.1.15:5000/gajg/' + name[:-4] + ':1.0\"'
        os.system(push_image)
        redeploy = 'ansible jgxt1 -m shell -a' + ' \"docker stack deploy --with-registry-auth -c ' + name[:-4] + '.yml isgs-app\"'
        os.system(redeploy)
        print(name + "===================后端部署文件:" + name[:-4] + " 已升级部署完毕===================")

      elif name[-3:] == "zip":
        '''
        stup: 1 将文件拷贝至目录
              2 将原文件重命名备份
              3 解压缩包文件
        '''
        print("===================前端配置文件:" + name[:-4] + " 已开始升级部署===================")
        cmd_copy = 'ansible jgxt1 -m copy -a ' + '\"src=' + name + ' dest=/data/docker/volumes/isgs-app_nginx-www/_data/ backup=yes\"'
        os.system(cmd_copy)
        cmd_mv= 'ansible jgxt1 -m shell -a' + ' \"chdir=/data/docker/volumes/isgs-app_nginx-www/_data/ mv '  + name[:-4] + ' ' +name[:-4] + '-backup-' + time.strftime("%Y-%m-%d@%H:%M:%S~", time.localtime()) + '\"'
        os.system(cmd_mv)
        cmd_unzip = 'ansible jgxt1 -m shell -a' + ' \"chdir=/data/docker/volumes/isgs-app_nginx-www/_data/ unzip ' + name + '\"'
        os.system(cmd_unzip)
        print("===================前端配置文件:" + name[:-4] + " 已升级部署完毕===================")

      elif name[-3:] == "yml":
        '''
        stup: 1 将文件拷贝至目录(如存在文件重命名文件)
        '''
        print("===================配置文件:" + name[:-4] + " 已开始升级部署===================")
        cmd_copy = 'ansible jgxt1 -m copy -a ' + '\"src=' + name + ' dest=/data/file/ backup=yes\"'
        os.system(cmd_copy)
        print("====================配置文件:" + name[:-4] + " 已升级部署完毕===================")
      else:
        #exit(1)
        print("===================升级部署已经开始===================")
        #print(name + " is not a deploy file")

def main():
  oper_file()

if __name__ == "__main__":
  main()
