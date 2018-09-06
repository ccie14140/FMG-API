import syslog_client

log_level_text = ["WARNING","NOTICE","ERROR"]
log_message = input("Enter the message you want to send to the server: ")
log_level_choice = int(input("Enter the log level you want to test, 0 - warning, 1 - notification, or 2 - error: "))
log_level = log_level_text[log_level_choice]
print(log_level)
log = syslog_client.Syslog('10.2.1.4')
log.send(log_message,syslog_client.Level.log_level)
