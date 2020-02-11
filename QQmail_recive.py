#!/usr/bin/env python3.7

import poplib
import os, sys, base64
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import signal

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()[:-1]
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def grep(Str,List):
    for i in List:
        if Str in str(i):
            break
    return i

def get_attach_name(byte_lines):
    str_lines = []
    for x in byte_lines:
        str_lines.append(x.decode())
    # 拼接邮件内容
    msg_content = '\n'.join(str_lines)
    # 把邮件内容解析为Message对象
    message = Parser().parsestr(msg_content)
    attachments = []
    for part in message.walk():
        filename = part.get_filename()
        #附件名字
        if filename:
            if "=?UTF-8?" in filename:
                filename = base64.b64decode(filename[9:-2]).decode("utf8")
            attachments.append(filename)
    return attachments

def M_read(index):
    resp, lines, octets = server.retr(index)
    try:
        Attachment = get_attach_name(lines)
        Date= str(grep("b'Date:",lines)).replace("b'",'')
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        print_info(msg)
        print('\n\n'+Date)
        print("Attachment:",Attachment)
#    try:
    except:
        Date= str(grep("b'Date:",lines)).replace("b'",'')
        From= Decode(str(grep("b'From:",lines)).replace("b'",''))
        To= Decode(str(grep("b'To:",lines)).replace("b'",''))
        Subject= Decode(str(grep("b'Subject:",lines)).replace("b'",''))
        print("",From,To,"\n",Subject,'\n\n',"this mail are purely composed by img or html",sep='\n')
        print('\n\n'+Date)
    return lines

def Action(Press,server):
    attach =""
    global index
    global Num_mail
    if Press == "q":
        server.quit()
    elif Press == "7":
        server.dele(index)
        index -=1
        Num_mail -=1
    elif Press == "9":
        attach = get_email_content(M_read(index), '.')
    elif Press == "8":
        index -=1
    elif Press == "5":
        index +=1
    if index < 0:
        index =0
    elif index > Num_mail:
        index -= 1
    if index == 0:
        print("No more new e-mails")
    else:
        M_read(index)
    return attach

def Decode(STR):
    head = "=?gb2312?b?"
    tail = "?="
    if head in STR:
        H = STR.find(head) + len(head)
        T = STR.find(tail)
        Result = base64.b64decode(STR[H:T]).decode("GBK")
        STR = STR[:H- len(head)] + Result + STR[T+ len(tail):]
    return STR

def get_email_content(byte_lines, savepath):
    str_lines = []
    for x in byte_lines:
        str_lines.append(x.decode())
    # 拼接邮件内容
    msg_content = '\n'.join(str_lines)
    # 把邮件内容解析为Message对象
    message = Parser().parsestr(msg_content)
    attachments = []
    for part in message.walk():
        filename = part.get_filename()
        if filename:
            print(filename)
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            abs_filename = os.path.join(savepath, filename)
            attach = open(abs_filename, 'wb')
            attachments.append(filename)
            attach.write(data)
            attach.close()
    return attachments

def Refresh():
    server = poplib.POP3_SSL(pop3_server, port)
    server.user(email)
    server.pass_(password)
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    Num_mail = len(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    return server, resp, mails, octets, Num_mail

def INPUT_delay():
  class InputTimeoutError(Exception):
    pass
  def interrupted(signum, frame):
    raise InputTimeoutError
  signal.signal(signal.SIGALRM, interrupted)
  signal.alarm(60)
  try:
    BB = input()
    signal.alarm(0)  # 读到输入的话重置信号
  except InputTimeoutError:
    BB = 'Fresh'
  return BB

# 输入邮件地址, 口令和POP3服务器地址:
email = '591465908@qq.com'
password = ''
pop3_server = 'pop.qq.com'
port = 995

# 连接到POP3服务器:
server = poplib.POP3_SSL(pop3_server, port)
server.user(email)
server.pass_(password)

print('Messages: %s. Size: %s' % server.stat())
resp, mails, octets = server.list()
Num_mail = len(mails)
# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)

#M_read(index)
while True:
    Press = INPUT_delay()
    if Press == "q":
        break
    if Press == "Fresh" or Press == "f":
        print("ReFreshing...")
        server, resp, mails, octets, Num_mail = Refresh()
    if Press == "s":
        print("Save & ReFreshing...")
        server.quit()
        server, resp, mails, octets, Num_mail = Refresh()
    if Num_mail == 0:
        os.system('clear')
        print("No New E-mails")
    else:
        os.system('clear')
        Action(Press,server)
        print("index=",index,"; all=",Num_mail)

# 关闭连接:
server.quit()
