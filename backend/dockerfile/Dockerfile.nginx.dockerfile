FROM nginx:1.23-alpine

RUN echo 'server {\
listen 80;\
access_log /dev/null;\
error_log  /dev/null;\
location /switch {\
proxy_pass http://spider:8080/switch;\
}\
location /spider/ {\
proxy_pass http://spider:8080/spider/;\
}\
location /api/ {\
proxy_pass http://core:8080/api/;\
}\
location /explore/ {\
proxy_pass http://explore:8080/explore/;\
}\
location /notice/ {\
proxy_pass http://explore:8080/notice/;\
}\
}\
server {\
listen 443;\
access_log /dev/null;\
error_log  /dev/null;\
return 200 "ok\n";\
}' > /etc/nginx/conf.d/default.conf
