import os
import socket
import re
import datetime
import shutil



IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.1
DEFAULT_URL = "index.html"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + "webroot"
httpRegex = re.compile(r'(GET) /([A-Za-z.?]+)? (HTTP/1.1)')
METHODS = ["get"]
VERSIONS = ["http/1.0", "http/1.1"]
STATUSES = {200: "OK",
            302: "Moved Temporarily",
            400: "Bad Request",
            404: "Page Not Found",
            501: "Not Implemented",
            505: "HTTP Version Not Supported"}
CONTENT_ADD = {"html": "text/html; charset=utf-8",
               "txt": "text/html; charset=utf-8",
               "jpg": "image/jpeg",
               "ico": "image/ico",
               # "gif": "image/gif",
               "js": "text/javascript; charset=UTF-8",
               "css": "text/css",
               "rtf": "text/rtf",
               "png": "image/png"}
RESPONSE_BODY = {
    "type": "Content-Type: ",
    "length": "Content-Length: "}
REQUEST_TYPES = {
    "GET": r'(GET /.+ HTTP/1.1)',
    "POST": r'(POST /.+ HTTP/1.1)'
}
c = datetime.datetime.now()


def calculate_area(url, client_socket, data):
    print("calculate-area was summoned")
    base = str(re.findall('t=.+&', url))[4:-3]
    hight = str(re.findall('h=.+', url))[4:-2]
    res = int(base) * int(hight) / 2
    if res == int(res):
        res = int(res)
    print(res)
    send_response(client_socket, 200, str(res).encode(), 'txt')


def calculate_next(url, client_socket, data):
    print("calculate_next was summend")
    net = str(int(str(re.findall('=.+', url))[3:-2]) + 1)
    print(net)
    send_response(client_socket, 200, net.encode(), 'txt')


def get_img_by_name(url, client_socket, data):
    print("get_img_by_name was summened")
    pic_name = url[18:]
    print(pic_name)
    pic_dir = CURRENT_DIR + '//summened_imgs/' + pic_name + ".jpeg"
    print(pic_dir)
    print(os.path.exists(pic_dir))
    if os.path.exists(pic_dir):
        print("hello")
        pic_f = open(pic_dir, 'br')
        pic_data = pic_f.read()
        print("pic is open")
        send_response(client_socket, 200, pic_data, 'jpg')
        print("hi")
    send_response(client_socket, 404, "", 'txt')

def get_file_body(data):
    print("geting file content")
    print(data)
    line = re.search("\r\n\r\n", data)
    print(line)
    c = line.span()[1]
    print(c)
    content = data[c:]
    print(content)
    return content

def recive_post(url, client_socket, data):  #/upload?file-name=LOGO.png
    new_file_path = CURRENT_DIR + '/uploads'
    print("working with posts:\n")
    s_url = url.split(".")
    print("s_url = ")
    print(s_url)
    print(CONTENT_ADD[(s_url[-1])] != None)
    if CONTENT_ADD[(s_url[-1])] != None:
        send_response(client_socket, 400, ("unknown type file").encode(), "html")
    file_type = s_url[-1]
    print("new_file_path = " + new_file_path)

    d = str(c.strftime("%Y")) + str(c.strftime("%b")) + str(c.strftime("%d"))
    file_n = str(re.findall('e=.+', s_url[-2]))[4:-2]
    filename = file_n + "_" + d + '.' + file_type
    if os.path.exists(new_file_path + '/' + filename):
        print("Error, file already exist. rewriting file")
    f = open(filename, 'w')
    f_body = get_file_body(data)
    f.write(f_body)
    f.close()
    shutil.move(filename, new_file_path)
    send_response(client_socket, 200, f_body.encode(), file_type)


WEB_FUN = {
    "GET": {
        "calculate-area.height=.+&width=.+": calculate_area,
         "calculate-next.num=.+": calculate_next,
        "image.image-name=": get_img_by_name
    },
    "POST": {
        "": recive_post
    }
}


def find_url_defin(url, client_socket, req, data):
    print("serching for " + req + " function")
    print(url)
    for FUN in WEB_FUN[req]:
        if re.search(FUN, url) != None:
            print("FUN = " + FUN)
            return (WEB_FUN[req][FUN](url, client_socket, data))
    return "None"


def handle_client_request(resource, client_socket, req, data):
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource
    url_defin = find_url_defin(url, client_socket, req, data)
    if url_defin == "None":
        full_url = CURRENT_DIR + "/" + url
        if not os.path.exists(full_url):
            return 404, "None", "None"
        file_type = url.split(".")[-1]
        print("full_url = " + full_url)
        f = open(full_url, "rb")
        data = f.read()
        f.close()
        return 200, data, file_type


def response_headline(code):
    return VERSIONS[1] + " " + str(code) + " " + STATUSES[code] + "\r\n"


def send_response(client_socket, code, response_body, url_type): #send_response(client_socket, 200, f2, "txt")
    print("rar")
    if code == 200:
        print("ok")
        response = response_headline(code)
        response = response + RESPONSE_BODY["length"] + str(len(response_body)) + "\r\n"
        response = response + RESPONSE_BODY["type"] + str(CONTENT_ADD[url_type]) + "\r\n"
        response = response + "\r\n"
        print(response)
        client_socket.send(response.encode() + response_body)
    else:
        response = VERSIONS[1] + " " + str(code) + " " + STATUSES[code] + "\r\n"
        response = response + RESPONSE_BODY["length"] + "0" + "\r\n"
        response = response + RESPONSE_BODY["type"] + str(CONTENT_ADD["html"]) + "\r\n"
        response = response + "\r\n"
        client_socket.send(response.encode())


def validate_http_request(request):
    print(request[:4])
    print(request.split("\r\n")[0])
    for T in REQUEST_TYPES:
        request_ln = re.findall(REQUEST_TYPES[T], request)
        if request_ln != []:
            request_ln = request_ln[0].split(" ")
            if len(request_ln) != 3:
                return False, 400
            if request_ln[0] != T or not request_ln[2].lower() in VERSIONS:
                return False, 505
            resource = request_ln[1]
            return True, resource, T
    return False, 404




def handle_client(client_socket):
    print('Client connected\n')

    while True:

        try:
            data = client_socket.recv(1024).decode()
            is_request_valid, resource, req = validate_http_request(data)
            print("received new file")

            if not is_request_valid:
                print('Error: Not a valid HTTP request')
                send_response(client_socket, resource, None)
            print('Got a valid HTTP request')
            code, response, url_type = handle_client_request(resource, client_socket, req, data)
            send_response(client_socket, code, response, url_type)
            break
        except:
            break

    print('Closing connection\n')
    client_socket.close()


def main():
    os.chdir('webroot')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port " + format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received\n')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    main()
