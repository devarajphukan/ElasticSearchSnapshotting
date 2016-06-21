import requests, json, os, re, datetime , time,sys
from time import strftime
from email.mime.text import MIMEText
import oauth2.clients.smtp as smtplib

def takeSnapshot() :

	#Take Snapshot
	take_snapshot_cmd='http://'+ip+':9200/_snapshot/'+repo+'/'+snapshot_name
	requests.put(take_snapshot_cmd)


def deleteOldSnapshots(num_snapshots_to_keep) :
	
	# Delete old snapshots	
	snapshot_list_cmd = "http://"+ip+":9200/_snapshot/"+repo+"/_all"
	res = requests.get(snapshot_list_cmd)
	response = json.loads(res.text)
	old_snapshots = response['snapshots'][:-num_snapshots_to_keep]
	
	for i in old_snapshots :
		if i['state'] == 'SUCCESS' :
			# print "deleting " + i['snapshot']
			snapshot_del_cmd = "http://"+ip+":9200/_snapshot/"+repo+"/"+i['snapshot']
			requests.delete(snapshot_del_cmd)

def checkSnapshotStatus() :

	#Check for current running snapshot processes
	check_status_cmd = 'http://'+ip+':9200/_snapshot/'+repo+'/_all'
	res = requests.get(check_status_cmd)
	response = json.loads(res.text)

	countOK = 0
	for snp in range(len(response['snapshots'])) :
		if response['snapshots'][snp]['state'] == 'SUCCESS' :
			countOK += 1

	if countOK == len(response['snapshots']) :
		return True
	else :
		return False

def sendMail(sender,sender_passwd,msg,receivers,subject):

    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.set_debuglevel(True)
    server.ehlo('Test')
    server.starttls()

    server.login(sender,sender_passwd)
    server.sendmail(sender, receivers, msg.as_string())
    
try :

	#name of elastic search snapshot repo
	repo = "my_backup"
	snapshot_name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')

	r = requests.get('http://localhost:9200/_cat/master?v').text
	text = re.sub(" +"," ", r)
	ip = str(text.split(" ")[-3].strip())
	
	takeSnapshot()

	while True:
		if checkSnapshotStatus() :
			deleteOldSnapshots(1) #Pass Number of snapshots to keep.
			break

except :

	#Email sender credentials
	sender = 'test@gmail.com'
	sender_passwd = 'testPasswd'

	#List of recievers to send mail
	li_recievers = ["testReciever1@gmail.com","testReciever2@gmail.com"]
	
	sendMail(sender,sender_passwd,"ES Snapshot " + snapshot_name + " failed", li_recievers,"ES Snapshot Failure")