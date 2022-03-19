import socket, os, glob, re, datetime, shutil

c = datetime.datetime.now()


VERSIONS = ["http/1.0", "http/1.1"]
STATUSES = {200: "OK",
            302: "Moved Temporarily",
            400: "Bad Request",
            404: "Page Not Found",
            501: "Not Implemented",
            505: "HTTP Version Not Supported"}


CONTENT_ADD = {"html": "text/html; charset=utf-8",
               "txt":  "text/html; charset=utf-8",
               "jpg": "image/jpeg",
               "ico": "image/ico",
               "gif": "image/gif",
               "js": "text/javascript; charset=UTF-8",
               "png": "image/png",
               "rtf": "text/rtf",
               "css": "text/css"}

RESPONSE_BODY = {
    "type": "Content-Type: ",
    "lenght": "Content-Length: "}
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + "webroot"

def send_response(client_socket, code, response_body, url_type):
    print("sent")


def validate_http_request(request):
    data_by_line = request.split("\r\n")
    data_by_ward = data_by_line[0].split(" ")
    print("\nGET" == data_by_ward[0])
    print("HTTP/1.1" == data_by_ward[2])
    return not "\nGET" == data_by_ward[0] and "HTTP/1.1" == data_by_ward[2]





txt = "calculate-area?height=3&width=4"

txt2 = "calculate-next?num=34"
def define():

    if re.search(WEB_FUN["calculate_area"], url) != None:
        print("calculate-area:")
        base = str(re.findall('t=.+&', url))[4:-3]
        hight = str(re.findall('h=.+', url))[4:-2] 
        print(int(base)*int(hight)/2)
    if re.search(WEB_FUN['calculate-next'], url) != None:
        print("calculate_next")





def calculate_area(url):
    print("calculate-area:")
    base = str(re.findall('t=.+&', url))[4:-3]
    hight = str(re.findall('h=.+', url))[4:-2] 
    print(int(base)*int(hight)/2)

          

def calculate_next(url):
    net = int(str(re.findall('=.+', url))[3:-2]) +  1
    return net








WEB_FUN = {
    "^calculate-area.height=.+&width=.+": calculate_area, 
    "calculate-next.num=.+": calculate_next
}
 
def find_url_defin(url):
    for FUN in WEB_FUN:
        if re.search(FUN, url) != None:
            return(WEB_FUN[FUN](url))


















def handle_client_request(resource):

    if resource == '':
        url = "DEFAULT_URL"
    else:
        url = resource

    file_name = url.split("/")[-1]
    print("file_name = ")
    print(file_name)
    if url == "uploads/resricted":
        return 403, "None", "None"
    if file_name == "index1.html":
        return 302, "None", "None"
    urlA = CURRENT_DIR + url
    urlA = urlb
    if os.path.isfile(urlA):
        url_type = urlA.split('.')[-1].lower()
        f = open(urlA, "rb")
        body = f.read()
        f.close()
        return 200, body, url_type
    else:
        return 404, "None", "None"


def handle_client_request_byRan(resource):
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource[1:]
    full_url = CURRENT_DIR + url
    full_url = urlb
    if not os.path.exists(full_url):
        return 404, "None", "None"

    file_type = url.split(".")[-1]
    f = open(full_url, "rb")
    data = f.read()
    f.close()
    return 200, data, file_type



def send_response(client_socket, code, response_body, url_type):
    if code == 200:
        response = VERSIONS[1] + " " + str(code) + " " + STATUSES[code] + "\r\n"
        response = response + RESPONSE_BODY["lenght"] + str(len(response_body)) + "\r\n"
        response = response + RESPONSE_BODY["type"] + str(CONTENT_ADD[url_type]) + "\r\n"
        response = response + "\r\n"
        print(response)
        return((response).encode() + response_body)
    else:
        response = VERSIONS[1] + " " + str(code) + " " + STATUSES[code] + "\r\n"
        response = response + RESPONSE_BODY["lenght"] + "0" + "\r\n"
        response = response + RESPONSE_BODY["type"] + str(CONTENT_ADD["html"]) + "\r\n"
        response = response + "\r\n"
        return((response).encode())


request = '''
GET /index.html HTTP/1.1
Host: 127.0.0.1
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
'''

request2 = '''
POST /upload?file-name=LOGO.png HTTP/1.1
Host: 127.0.0.1
Connection: keep-alive
Content-Length: 20341
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"
Accept: */*
Content-Type: text/plain
X-Requested-With: XMLHttpRequest
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
sec-ch-ua-platform: "macOS"
Origin: http://127.0.0.1
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://127.0.0.1/index.html
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
'''



REQUEST_TYPES = {
    "GET": r'(GET /.+ HTTP/1.1)',
    "POST": r'(POST /.+ HTTP/1.1)'
}



def validate_http_request(request):
    for T in REQUEST_TYPES:
        request_ln = re.findall(REQUEST_TYPES[T], request)
        if request_ln != []:
            if T == "GET":
                request_ln = list(request_ln[0])
            if T == "POST":
                request_ln = request_ln[0].split(" ")
            if len(list(request_ln)) != 3:
                return False, 400
            if request_ln[0] != T or not request_ln[2].lower() in VERSIONS:
                return False, 505
            resource = request_ln[1]
            return True, resource
    return False, 404
    
    

def recive_post(url, client_socket):  #/upload?file-name=LOGO.png
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
        print("file alredy exsist") 
    if re.findall('image',CONTENT_ADD[file_type]):
        f = open(filename, 'bw')
    else:
        f = open(filename, 'w')
        f.write("HELLO MY NAME IS RAN")
    f.close()
    f = open(filename, 'r')
    (f.read())
    f.close()
    shutil.move(filename, new_file_path)
    funel_path = new_file_path + '/' + filename
    f2 = open(funel_path, 'r')
    print(f2.read())
    print("gg")
    send_response(client_socket, 200, f2, "txt")



s = 'image.image-name='


#recive_post('/upload?file-name=LOGO.rtf', 'client_socket')

url_img = "/image?image-name=MB_LOGO"


def get_img_by_name(url, client_socket):
    pic_name = url[18:]
    print(pic_name)
    pic_dir = CURRENT_DIR + '/summened_imgs/' + pic_name + ".jpeg"
    print(pic_dir)
    print(os.path.exists(pic_dir))
    if os.path.exists(pic_dir):
        pic_f = open(pic_dir, 'br')





#get_img_by_name(url_img, "")


url_logo = "/Users/ranbrachel/Desktop/Syber_Shit/project4.4/webroot/summened_imgs/MB_LOGO.jpeg"

def shat_up():
    f = open(url_logo,"rb")
    con = f.read()
    print(type(con))
    print(con)
    
    print("rip")









shat_up( )



