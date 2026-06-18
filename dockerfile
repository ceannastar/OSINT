FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    zstd \
    unzip \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Ollama через официальный скрипт
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN useradd -m -u 1000 ollama && \
    chown -R ollama:ollama /home/ollama

USER ollama

RUN mkdir -p /home/ollama/.ollama/models

RUN curl -L https://github.com/OpenOSINT/OpenOSINT/archive/refs/heads/main.zip -o /tmp/repo.zip && \
    unzip /tmp/repo.zip -d /home/ollama/ && \
    mv /home/ollama/OpenOSINT-main /home/ollama/OpenOSINT && \
    rm /tmp/repo.zip

RUN pip3 install --user requests beautifulsoup4 lxml

EXPOSE 11434

EXPOSE 5000

CMD ["/bin/sh", "-c", "ollama serve & tail -f /dev/null"]