Preparation steps


1) create a ec2 intstance server on Aws platform 
2) install Docker on the server
3) Run nginx container 


wrote a python program that checks the endpoint, the application endpoint where the nginx is running and checks the status of that application.makes an http request to it and checks that we have  a successful reply from the application has some problems or the application is'nt accessible at all. maybe server is down , maybe the container is crashed if that happens the python program will alert us or notify us through email , when the website is down

configure the python program to send email to our email address and once we get notified per email we will extend the python logic to restart the docker container on the server or server is not accessible , restart the server 

1) create a ec2 instance in the AWS to locally connect from the computer , ssh into the server using pem file and execute the ssh 


install Docker on the server and run nginx container 

steps required to install docker
```
sudo yum install docker
```

Add group membership for the default ec2-user so you can run all docker commands without using the sudo command
```
sudo usermod -a -G docker ec2-user
id ec2-user
# Reload a Linux user's group assignments to docker w/o logout
newgrp docker
```

Enable docker service at AMI boot time:
```
sudo systemctl enable docker.service
```

Start the Docker service:

```
sudo systemctl start docker.service
```


run a nginx container

```
docker run -d -p 8080:8080 nginx

```


access the nginx server using the public ip and port 8080


Python script that monitors the website by accessing it and validating the
HTTP response


1. HTTP Request:

* The script uses the requests ```library``` to send an HTTP GET request to the URL ```http://ec2-18-143-73-242.ap-southeast-1.compute.amazonaws.com:8080/```.

2. Response Handling:

* It checks the status code of the response received from the server.
* If the status code is 200, it prints "Application is running successfully!"
* If the status code is not 200, it prints "Application down fix it!"


* This script is used for monitoring the availability and health of the application hosted at the specified URL. If the application is reachable and returns a successful response (status code 200), it indicates that the application is running correctly. Otherwise, it suggests that application is down.












