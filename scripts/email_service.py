import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("sender", "pass")
server.sendmail("reseiver",
                 "sender",
                 "Test Envyard")

server.quit()