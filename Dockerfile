#Dockerfile
FROM index.tenxcloud.com/tenxcloud/centos
MAINTAINER zhou_mfk <zhou_mfk@163.com>
RUN mkdir -p /data/1111111111111111111111111111111111111111
EXPOSE 22
RUN echo 'root:redhat' | chpasswd
RUN yum install tar gzip gcc vim wget -y
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
CMD /usr/sbin/sshd -D
#End
