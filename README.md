Steps to start application.

Start EC2 instance.
find public ip

Start CT5169_VM04
ssh: sudo docker start mysqlwiki
ssh: sudo docker exec -it mysqlwiki /bin/sh
sh-4.4# mysql -u root -p (mypassword)
mysql> USE wiki

Start CT5169_VM02
scp -r -P 2222 FundamentalsAssignment student@127.0.0.1:~/flaskProjects/wikidb1
OR
ssh: cd ~/flaskProjects/wikidb1
ssh: nano app.py
    CHANGE INSTANCE IP
    ^X y ENTER
ssh: python3 app.py

Browser
http://127.0.0.1:3000/search
Search: Paul Thomas Anderson

Added connection= none and cursor = None, but it's not a good solution. revert back as well as finally
Real issue is port forwarding from 3306:7888 on the mysql VM - Almost there.
