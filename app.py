from flask import Flask,render_template, request
import logging
import os
import mysql.connector as msql
import pandas as pd
import pymysql
import sshtunnel
from mysql.connector import Error
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder



app = Flask("__name__")
ssh_host = '192.168.56.104'
ssh_username = 'hassan'
ssh_password = '1202'
database_username = 'hassane'
database_password = '1202'
sql_password = os.environ.get('sql_password')
database_name = 'hassandb'
localhost = '127.0.0.1'

def open_ssh_tunnel(verbose=False):
    """Open an SSH tunnel and connect using a username and password.
    
    :param verbose: Set to True to show logging
    :return tunnel: Global SSH tunnel connection
    """
    
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    
    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username = ssh_username,
        ssh_password = ssh_password,
        remote_bind_address = ('127.0.0.1', 3306)
    )
    
    tunnel.start()
    print("connected to tunnel")
    
def mysql_connect():
    """Connect to a MySQL server using the SSH tunnel connection
    
    :return connection: Global MySQL database connection
    """
    
    global connection
    
    connection = pymysql.connect(
        host='127.0.0.1',
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=tunnel.local_bind_port
    )
    print("connected to mysql")



def close_ssh_tunnel():
    """Closes the SSH tunnel connection.
    """
    
    tunnel.close
 


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/attendance')
def attendance():
	open_ssh_tunnel()
	mysql_connect()
	cur = connection.cursor()
	cur.execute("SELECT * FROM attendance")
	data = cur.fetchall()
	return render_template('attendance.html', data=data)




app.run(host='0.0.0.0', port=5000)
