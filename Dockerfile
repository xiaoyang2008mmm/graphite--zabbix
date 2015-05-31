FROM centos:centos6
MAINTAINER The CentOS Project <cloud-ops@centos.org>

RUN yum -y update
RUN yum -y install openssh-server passwd httpd
ADD ./start.sh /start.sh
RUN mkdir /var/run/sshd
RUN echo "root:111111" | chpasswd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' 
RUN chmod 755 /start.sh
RUN /etc/init.d/httpd start
EXPOSE 22
RUN ./start.sh
RUN yum -y install epel-release
RUN yum -y install nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN echo "nginx on CentOS 6 inside Docker" > /usr/share/nginx/html/index.html
EXPOSE 80
ENTRYPOINT ["/usr/sbin/sshd", "-D"]
CMD [ "/usr/sbin/nginx" ]

