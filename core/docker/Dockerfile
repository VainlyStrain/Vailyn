# Pulling base image
FROM fedora:latest

# Install Vailyn dependencies
RUN dnf install -y --refresh \
    konsole \
    python3 \
    python3-pip \
    tor \
    nmap-ncat \
    git

# Installing Vailyn
RUN git clone https://github.com/VainlyStrain/Vailyn.git && \
    cd Vailyn && \
    pip3 install -r requirements.txt
    
ENTRYPOINT ["python3", "Vailyn"]
