'''Module to operate with HTTP-Requests.'''
from json.decoder import JSONDecodeError
import csv
import json
import socket
import os.path

from film_utils import search_title

ARTIST = 0
ALBUM = 1
TRACK = 2
FILE_PATH = 'musik.csv'
RESPONSE_HEADER = {
    'Server': 'Socket_Based(Linux)',
    'Content-Type': 'application/json',
    'Connection': 'close'
}
HTTP = 'HTTP/1.1 {}'
STATUS_CODE = {
    'OK' : '200 ',
    'Not Found' : '404 ',
    'Method Not Allowed' : '405 ',
    'Not Acceptable' : '406',
    'Bad Request' : '400 '
}
DATA_SIZE = 4096
CSV_HEADER = ['Artist', 'Album', 'Track']


def create_status_code(status, body=False):
    '''Function to create the statuscode.'''
    if not body:
        return HTTP.format(
            [value + key for (key, value) in STATUS_CODE.items() if key == status][0]
        )
    return '{}'.format(
        [value + key for (key, value) in STATUS_CODE.items() if key == status][0]
    )


def _create_csv_header(path, header=CSV_HEADER):
    '''Function to create the initial CSV header.'''
    with open(path, 'w', newline='', encoding='ISO-8859-1') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)


def _get_csv_data(path):
    '''Open given CSV-file, create a list of reader-object and skip first line.'''
    with open(path, 'r', encoding='ISO-8859-1') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        return list(reader)


def _create_csv_data(path, music):
    '''Writes into a CSV-file.'''
    with open(path, 'a', newline='', encoding='ISO-8859-1') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(music)


def _find_music(title, search_type):
    '''Function to search for artists in a CSV.'''
    if search_type == ARTIST:
        try:
            music = title[search_type].lower()
        except IndexError:
            return None
        found_music = set()
        for line in _get_csv_data(FILE_PATH):
            if music not in line[search_type].lower():
                continue
            found_music.add(line[search_type])
        return sorted(list(found_music))
    elif search_type == ALBUM:
        music = title[ARTIST].lower()
        found_music = set()
        for line in _get_csv_data(FILE_PATH):
            if music not in line[ARTIST].lower():
                continue
            found_music.add(line[search_type])
        return sorted(list(found_music))
    else:
        music = title[ALBUM].lower()
        found_music = set()
        for line in _get_csv_data(FILE_PATH):
            if (music != line[ALBUM].lower()) or (title[ARTIST].lower() != line[ARTIST].lower()):
                continue
            found_music.add(line[search_type])
        return sorted(list(found_music))
    return 'no music found..'


class HTTPServer:
    '''Class to take and work with socket objects.'''
    # pylint: disable=too-few-public-methods
    # pylint: disable=superfluous-parens,no-self-use,too-many-return-statements
    def __init__(self, ip_address, port):
        '''Initializing a local network with socket module.'''
        super().__init__()
        self.port = int(port)
        self.ip_address = str(ip_address)
        self.connection = None

    def __call__(self):
        '''Method to start the server_socket.'''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.ip_address, self.port))
            server_socket.listen(5)
            while True:
                (self.connection, _) = server_socket.accept()
                all_data = []
                bytes_rec = 0
                try:
                    data = self.connection.recv(DATA_SIZE)
                    if not data:
                        self.connection.close()
                        continue
                    all_data.append(data)
                    bytes_rec += len(data)
                    total_data = b''.join(all_data)
                    request = self._get_request(total_data)
                    created_response = self._handle_request(request)
                    self._send_response(created_response)
                finally:
                    self.connection.close()

    @staticmethod
    def _get_request(data):
        '''Function to create a request object of the clients request.'''
        data = data.decode()
        return Request(data)

    def _handle_request(self, request):
        '''Method to handle the request of client.'''
        reply_header = ''
        if not os.path.isfile(FILE_PATH):
            _create_csv_header(FILE_PATH)
        for (key, value) in RESPONSE_HEADER.items():
            reply_header += '{}: {}\r\n'.format(key, value)
        if request.resource.split('/')[1] == 'Musik':
            if request.method == 'GET':
                music = request.resource.lower().split('/')[2:5]
                try:
                    music[0]
                except IndexError:
                    all_artists = set()
                    for line in _get_csv_data(FILE_PATH):
                        all_artists.add(line[0])
                    return Response(
                        create_status_code('OK'),
                        reply_header,
                        json.dumps(list(all_artists))
                    )
                if not _find_music(music, ARTIST):
                    return Response(
                        create_status_code('Not Found'),
                        reply_header,
                        create_status_code('Not Found', True)
                    )
                if (len(music) == 1) and (music[0] != ''):
                    if not _find_music(music, ARTIST):
                        return Response(
                            create_status_code('Not Found'),
                            reply_header,
                            create_status_code('Not Found', True)
                        )
                    return Response(
                        create_status_code('OK'),
                        reply_header,
                        json.dumps(_find_music(music, ALBUM))
                    )
                if (len(music) == 2) and (music[0] != '') and (music[1] != ''):
                    if not _find_music(music, ALBUM):
                        return Response(
                            create_status_code('Not Found'),
                            reply_header,
                            create_status_code('Not Found', True)
                        )
                    return Response(
                        create_status_code('OK'),
                        reply_header,
                        json.dumps(_find_music(music, TRACK))
                    )
                return Response(
                    create_status_code('Not Found'),
                    reply_header,
                    create_status_code('Not Found', True)
                )
            if request.method == 'POST':
                music = request.resource.lower().split('/')[2:5]
                if len(music) != 3:
                    return Response(
                        create_status_code('Bad Request'),
                        reply_header,
                        create_status_code('Bad Request', True)
                    )
                _create_csv_data(FILE_PATH, music)
                return Response(
                    create_status_code('OK'),
                    reply_header,
                    create_status_code('OK', True)
                )
            return Response(
                create_status_code('Method Not Allowed'),
                reply_header,
                create_status_code('Method Not Allowed', True)
            )
        return Response(
            create_status_code('Not Found'),
            reply_header,
            create_status_code('Not Found', True)
        )

    def _send_response(self, response):
        '''Method to build the response of server_socket.'''
        self.connection.sendall('\r\n'.join([
            response.status_code,
            response.header,
            '\r\n' + response.body
        ]).encode(encoding='UTF-8'))


class Request:
    '''Class to take the request of client.'''
    # pylint: disable=too-few-public-methods
    def __init__(self, data):
        '''Initialize the request of client.'''
        self.method = None
        self.body = None
        self.headers = {}
        self.resource = None
        self._data_splitter(data)

    def _data_splitter(self, data):
        '''Method to split client request.'''
        data = data.splitlines()
        (self.method, self.resource) = data[0].split(' ')[0:2]
        for (elem, next_elem) in zip(data[1:], data[2:]):
            if not elem:
                self.body = next_elem
                break
            header_split = elem.split(':', 1)
            self.headers[header_split[0]] = header_split[1]


class Response():
    '''Class to response with requested data.'''
    # pylint: disable=too-few-public-methods
    def __init__(self, status_code, header, body):
        '''Initialize a server_socket response.'''
        self.header = header
        self.status_code = status_code
        self.body = body


# pylint: disable=invalid-name
if __name__ == '__main__':
    start_server = HTTPServer('127.0.0.1', 8080)
    print('serving on 127.0.0.1:8080')
    start_server()

