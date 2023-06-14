cd ~
rm -rf project-summer-2023
git clone https://github.com/AlexeykaVas/project-summer-2023
sudo docker stop krok2023
sudo docker rm krok2023
sudo docker rmi krok2023
cd project-summer-2023
sudo docker build -t krok2023 .
sudo docker run -d --name krok2023 -p 23182:23182 krok2023
cd ..