FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf 
#Oli yllä aiemmin: COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]