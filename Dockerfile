FROM centos6.6
RUN mkdir -p /data/1111111111111111111111111111111111111111
RUN echo 'root:111111' | chpasswd
RUN yum install passwd openssl openssh-server -y
RUN ssh-keygen -q -t rsa -b 2048 -f /etc/ssh/ssh_host_rsa_key -N ''
RUN ssh-keygen -q -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
RUN sed -i '/^session\s\+required\s\+pam_loginuid.so/s/^/#/' /etc/pam.d/sshd
RUN mkdir -p /root/.ssh && chown root.root /root && chmod 700 /root/.ssh
# 暴露ssh端口22
EXPOSE 22
# 设定运行镜像时的默认命令：输出ip，并以daemon方式启动sshd
CMD ip addr ls eth0 | awk '{print $2}' | egrep -o '([0-9]+\.){3}[0-9]+';/usr/sbin/sshd -D
