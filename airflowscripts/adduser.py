#!/usr/bin/python
# -*- coding: UTF-8 -*-
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'johuo@yunify.com'
#user.authenticate= 'admin'
#user._password = 'admin'
user.password = 'admin'
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
