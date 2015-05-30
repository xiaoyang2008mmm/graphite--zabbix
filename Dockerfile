# VERSION 0.0.1
# 默认ubuntu server长期支持版本，当前是12.04
FROM centos
# 签名啦
MAINTAINER yongboy "chen"

# 更新源，安装ssh server
RUN  yum -y  update
RUN yum install -y openssh-server
RUN mkdir -p /var/run/sshd

# 设置root ssh远程登录密码为111111
RUN echo "root:111111" | chpasswd 

# 添加orache java7源，一次性安装vim，wget，curl，java7，tomcat7等必备软件
RUN yum -y  install python-software-properties
RUN yum -y  install -y vim wget curl oracle-java7-installer tomcat7

# 设置JAVA_HOME环境变量
RUN update-alternatives --display java
RUN echo "JAVA_HOME=/usr/lib/jvm/java-7-oracle">> /etc/environment
RUN echo "JAVA_HOME=/usr/lib/jvm/java-7-oracle">> /etc/default/tomcat7

# 容器需要开放SSH 22端口
EXPOSE 22

# 容器需要开放Tomcat 8080端口
EXPOSE 8080

# 设置Tomcat7初始化运行，SSH终端服务器作为后台运行
ENTRYPOINT service tomcat7 start && /usr/sbin/sshd -D
