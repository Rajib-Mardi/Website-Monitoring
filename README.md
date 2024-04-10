### Demo Project:
* Website Monitoring and Recovery
### Technologiesused:
Python, AWS , Docker, Linux


###  Project Description:

* wrote a Python program that checks the endpoint, the application endpoint where the nginx is running, and checks the status of that application. makes an HTTP request to it and checks that we have a successful reply from the application, which has some problems or isn't accessible at all. Maybe the server is down or maybe the container is crashed. If that happens, the Python program will alert us or notify us through email when the website is down.

* configure the Python program to send email to our email address, and once we get notified per email, we will extend the Python logic to restart the Docker container on the server. If the server is not accessible, restart the server. 


### Create a server on a cloud platform
1) create a ec2 instance in the AWS to locally connect from the computer , ssh into the server using pem file and execute the ssh 


#### install Docker on the server and run nginx container 

steps required to install docker

 1. Install docker, run
   ```
   sudo yum install docker
  ```

  2. Add group membership for the default ec2-user so you can run all docker commands without using the sudo command
   ```
   sudo usermod -a -G docker ec2-user
   id ec2-user
   newgrp docker
   ```

  3. Enable docker service at AMI boot time:
    ```
    sudo systemctl enable docker.service
    ```

  4. Start the Docker service:

    ```
    sudo systemctl start docker.service
    ```


  5. run a nginx container

   ```
    docker run -d -p 8080:8080 nginx
   ```


#### access the nginx server using the public ip and port 8080


![Welcome to nginx! - Brave 25-03-2024 19_19_57](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/d94e3559-05bb-47f8-8fa9-bc68e136ad50)


![MINGW64__c_Users_Rajib_Downloads 25-03-2024 11_17_50](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/8e6648c5-90ee-44d2-bc1e-e1223690a5b3)




### Python script that monitors the website by accessing it and validating the HTTP response


1. HTTP Request:

* The script uses the requests ```library``` to send an HTTP GET request to the URL ```http://ec2-18-143-73-242.ap-southeast-1.compute.amazonaws.com:8080/```.

2. Response Handling:

* It checks the status code of the response received from the server.
* If the status code is 200, it prints "Application is running successfully!"
* If the status code is not 200, it prints "Application down fix it!"


* This script is used for monitoring the availability and health of the application hosted at the specified URL. If the application is reachable and returns a successful response (status code 200), it indicates that the application is running correctly. Otherwise, it suggests that application is down.


![website-monitoring – website-monitoring py 23-03-2024 18_59_53](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/38c286bd-f2db-41ea-8ca6-e4cdd0563c65)


 -----------------------------------------------------------------------------
 
### Python script that sends an email notification when website is down


* Python script utilizes the ```smtplib module``` to send an email notification if a site is down. 

1. SMTP Connection:

* The script connects to the Gmail SMTP server (```smtp.gmail.com```) on port 587 using ```smtplib.SMTP```.

2.Start TLS Encryption:

* It initiates a TLS (Transport Layer Security) encrypted connection with the SMTP server using ```starttls()```.

3.SMTP Extended Hello (EHLO):

* The script sends an EHLO command to the SMTP server using ```ehlo()``` to identify itself.

4. SMTP Authentication:

* It logs in to the SMTP server using the provided email address (```EMAIL_ADDRESS```) and password (```EMAIL_PASSWORD```) for authentication with smtp.login().

5. Compose Email Message:

* The email message is composed with a subject line "SITE DOWN" and a custom message (```email_msg```).

6.Send Email:

* It sends the email notification to the same email address (```EMAIL_ADDRESS```) from which it is logged in using smtp.sendmail().

7. Environment Variables:

* The script fetches the email address and password from environment variables ```EMAIL_ADDRESS``` and ```EMAIL_PASSWORD``` using ```os.environ.get()```.

* This script is used to monitor the status of a website and receive email notifications if the site goes down. It relies on Gmail's SMTP server for sending emails securely, and it uses environment variables to store sensitive information such as email credentials.


![website-monitoring – website-monitoring py 23-03-2024 19_45_50](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/bd553717-5019-46e3-9333-9d66679a9ee6)



![SITE DOWN - rajeevmardi111@gmail com - Gmail and 39 more pages - Profile 1 - Microsoft​ Edge 10-04-2024 23_47_37](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/1319217a-238b-4851-be3c-522ea08c8689)


###   Python script that automatically restarts the application & server when the application is down




1. restart_container() Function:

  * Establishes an SSH connection to the specified host (18.143.73.242) using the ```paramiko``` library.
  * Executes a Docker start command (```docker start deed03b844af```) to restart the Docker container with the specified container ID (deed03b844af).
  * Prints the output of the Docker start command.

![website-monitoring – website-monitoring py 24-03-2024 11_20_30](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/60813ee9-d8e2-4ee6-99ff-8a1890e1eba6)

2. restart_server_and_container() Function:

 * Initiates a reboot of the specified EC2 instance using the ```reboot_instances()``` method from the ```boto3``` library.
 * Checks the status of the EC2 instance in a loop until it is in the 'running' state.
 * Upon reaching the 'running' state, it waits for 100 seconds and then calls the ```restart_container()``` function.
 







###  Python script continuously monitors the availability of an application by periodically sending an HTTP GET request to a specific URL.

1. monitor_application() Function:

* Tries to send an HTTP GET request to the specified URL  (```http://ec2-18-143-73-242.apsoutheast-1.compute.amazonaws.com:8080/```).
* If the response status code is '200', it prints "Application is running successfully!".
* If the response status code is not '200', it prints "Application down fix it!" and sends a notification email using the ```send_notification()``` function.
* If an exception occurs during the request (e.g., connection error), it prints the error message and sends a notification email.
* If the application is not accessible at all, it sends a notification email and restarts both the server and the container using the ```restart_server_and_container()``` function.

![website-monitoring – website-monitoring py 25-03-2024 11_17_34](https://github.com/Rajib-Mardi/Website-Monitoring/assets/96679708/ed4beb28-7232-4fa8-8693-c7a7ee2c969d)

  

2. Scheduler:

* The script schedules the ```monitor_application()``` function to run every 5 seconds using the ```schedule``` module.
* Inside the ```while True``` loop, it continuously checks for pending scheduled tasks and executes them.









