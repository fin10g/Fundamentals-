Steps to start application.

Start EC2 instance.
find public ip

Start CT5169_VM04
ssh: sudo docker start mysqlcontainerwiki
ssh: sudo docker exec -it mysqlcontainerwiki /bin/sh
sh-4.4# mysql -u root -p (mypassword)
mysql> USE wiki

Start CT5169_VM02
ssh: cd ~/flaskProjects/paramiko6
ssh: nano app.py
    CHANGE INSTANCE IP
    ^X y ENTER
ssh: python3 app.py

Browser
Search: Paul Thomas Anderson

Added connection= none and cursor = None, but it's not a good solution. revert back as well as finally
Real issue is port forwarding from 3306:7888 on the mysql VM - Almost there.
