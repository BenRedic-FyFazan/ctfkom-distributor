FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-server socat && \
    mkdir /var/run/sshd

# Create user
RUN useradd -m myuser
RUN chsh -s /bin/bash myuser

# Update SSH server configuration for passwordless and keyless login
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "myuser:U6aMy0wojraho" | chpasswd -e

# Expose SSH port
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
