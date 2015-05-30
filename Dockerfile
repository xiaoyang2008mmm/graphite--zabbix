#Dockerfile
FROM centos
MAINTAINER zhou_mfk <0fsdfsdfds@163.com>
EXPOSE 22
RUN echo 'root:redhat' | chpasswd
RUN mkdir -p /data11111111111111111111111111111
RUN yum install -y yum-priorities && rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
RUN yum install tar gzip gcc vim wget -y
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
CMD /usr/sbin/sshd -D
#End
