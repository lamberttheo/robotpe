import socket, fcntl, struct, smtplib, threading
import globalConfig

def get_ip_address(ifname):
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(socket.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def sendEmail():
  try:
    server = smtplib.SMTP(globalConfig.mailSMTPserver, globalConfig.mailSMTPport)
    if globalConfig.mailStartTLS:
      server.starttls()
    server.login(globalConfig.mailUsername, globalConfig.mailPassword)
    header = "To:" + globalConfig.mailTo + "\n" + "From: " + globalConfig.mailFrom + "\n" + "Subject:Now at " + get_ip_address("wlan0") + "\n\n"
    content = "Take control of the robot at http://" + get_ip_address("wlan0") + ":" + str(globalConfig.webserverPort) + "\n\n"
    server.sendmail(globalConfig.mailFrom, globalConfig.mailTo, header+content)
    server.quit()
    print("Mail sent to " + globalConfig.mailTo)
  except:
    print("The mail can't be sent")

mailThread = threading.Thread(None, sendEmail)
mailThread.start()
mailThread._Thread__stop()
