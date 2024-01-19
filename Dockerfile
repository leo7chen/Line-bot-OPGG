# 使用 Python 官方映像作為基礎映像
FROM python:3.8

# 設置工作目錄
WORKDIR /app

# 安裝 chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -qqy && \
    apt-get -qqy install google-chrome-stable fonts-wqy-zenhei && \
    rm /etc/apt/sources.list.d/google-chrome.list && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# 设置环境变量以支持中文字符
ENV LANG zh_TW.UTF-8
ENV LANGUAGE zh_TW:zh
ENV LC_ALL zh_TW.UTF-8

# 複製依賴文件並安裝依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼到容器中
COPY . .
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/able-goods-407102-e4f8edd319ad.json

# 指定容器啟動時執行的命令
CMD ["python", "./opggapp.py"]