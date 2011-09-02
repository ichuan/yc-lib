#!/bin/sh
# 穷举3位字母的.me域名，输出到屏幕及out.txt

for i in {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}; do
	curl -d whois_name=$i http://www.domain.me/domain-search -a 'MSIE' -s | grep "$i.me is available" > /dev/null && echo $i | tee -a out.txt
done
