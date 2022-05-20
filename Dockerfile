FROM python:3
USER root


copy . /root/

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# 環境変数にDiscordのトークンの追加
ARG token
ENV Token=${token}

# 環境変数にTimeTreeのトークンの追加
ARG apiKey
ENV ApiKey=${apiKey}

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install discord.py
RUN pip install dislash.py
RUN pip install datetime
RUN pip install bs4

CMD ./root/startup.sh
