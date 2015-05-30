#Dockerfile
FROM index.tenxcloud.com/tenxcloud/centos
RUN mkdir -p /data/1111111111111111111111111111111111111111
RUN echo 'root:111111' | chpasswd
RUN yum install tar gzip gcc vim wget -y
#End
