FROM centos:7
RUN yum -y install epel-release && yum clean all
RUN yum -y install ansible python36 python36-pip

ADD ansible/ /tmp/ansible/
ADD ansible/hosts /etc/ansible/
RUN ansible-playbook /tmp/ansible/site.yml

EXPOSE 5000

CMD ["/bin/python3","/opt/motd/motd_api.py"]
