import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getContent(data,mailType):
    if mailType == 0:
        mail_content = f"Hello {data['Username']},\nYour Order has been received. Order number is {data['OrderNumber']}. Thank you for shopping at eKirana.\nOrder details are:\n"
        
        for i in range(data["TotalItems"]):
            mail_content = mail_content + f'Order Item {data["OrderDetails"][i][0]}'+ f' x{data["OrderDetails"][i][1]}\n'
        

        mail_content = mail_content + f'Total Amount is {data["TotalPrice"]}'+ "\n\nRegards\neKirana Team"
    else:
        mail_content = f"Hello {data['Username']},\nYour Order #{data['OrderNumber']} has been successfully completed. Thank you for shopping at eKirana.\nOrder details are:\n"
        
        for i in range(data["TotalItems"]):
            mail_content = mail_content + f'Order Item {data["OrderDetails"][i][0]}'+ f' x{data["OrderDetails"][i][1]}\n'
        

        mail_content = mail_content + f'Total Amount is {data["TotalPrice"]}'+ "\n\nRegards\neKirana Team"
    return mail_content

def sendMail(email,data,mailType):
    mail_content = getContent(data,mailType)
    #The mail addresses and password
    sender_address = "ekiranateam@outlook.com"
    sender_pass = "adibhs123#"
    receiver_address = email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    if mailType==0:
        message['Subject'] = f'Your eKiarana Order #{data["OrderNumber"]} placed'   #The subject line
    else:
        message['Subject'] = f'Your eKiarana Order #{data["OrderNumber"]} Completed' #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.outlook.com', 587) 
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


# data format : {'Username','OrderNumber','OrderDetails'}
# s = {"username":"aditya","asdasd":554,"orderItems":[('adsasd',3),('assdf',4),('sdfsdf',23)]}
# data = {'Username':"Aditya",'OrderNumber':256}
# emailadd = 'bhosleaditya7@gmail.com'
# sendMail(emailadd,data)
