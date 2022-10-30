FROM nginx:1.23-alpine

RUN echo 'server {\n\
  listen 80;\n\
  access_log /dev/null;\n\
  error_log  /dev/null;\n\n\
  location /switch {\n\
    proxy_pass http://spider:8080/switch;\n\
  }\n\
  location /spider/ {\n\
    proxy_pass http://spider:8080/spider/;\n\
  }\n\
  location /api/ {\n\
    proxy_pass http://core:8080/api/;\n\
  }\n\
  location /explore/ {\n\
    proxy_pass http://explore:8080/explore/;\n\
  }\n\
  location /notice/ {\n\
    proxy_pass http://explore:8080/notice/;\n\
  }\n\
}\n\n\
server {\n\
  listen 443;\n\
  access_log /dev/null;\n\
  error_log  /dev/null;\n\
  return 200 "ok\\n";\n\
}\n' > /etc/nginx/conf.d/default.conf
