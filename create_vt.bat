cd C:\docker\vt
git pull origin master
docker-compose up
git add .
git commit -m "update vectortiles"
git push origin master
