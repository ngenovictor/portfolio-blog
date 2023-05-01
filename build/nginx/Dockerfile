FROM nginx:1.23.3

RUN rm /etc/nginx/conf.d/default.conf
COPY ./build/nginx/acme-challenge.conf /etc/nginx/acme-challenge.d
COPY ./build/nginx/nginx.conf /etc/nginx/conf.d

RUN apt update
# install cron for setting u[ cert renewal
RUN apt install cron -y
RUN apt install socat -y
RUN curl https://get.acme.sh | sh -s email=ngenovictor321@gmail.com
RUN source /root/.profile
# RUN acme.sh --install-cert -d victorngeno.com --key-file /root/web_cerificates/victorngeno_com_keyfile.pem --fullchain-file /root/web_cerificates/victorngeno_com_fullchain.pem --reloadcmd "service nginx force-reload"
