FROM centos:centos6
MAINTAINER The CentOS Project <cloud-ops@centos.org>

RUN yum -y update; yum clean all
RUN yum -y install openssh-server passwd httpd; yum clean all
ADD ./start.sh /start.sh
RUN mkdir /var/run/sshd
RUN echo "root:111111" | chpasswd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' 
RUN chmod 755 /start.sh
RUN /etc/init.d/httpd start
EXPOSE 22
EXPOSE 80
RUN ./start.sh
ENTRYPOINT ["/usr/sbin/sshd", "-D"]
