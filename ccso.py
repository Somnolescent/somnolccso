## Read-only CCSO server for Python 3.7+ by dotcomboom for somnol
## Originally worked on ~5/29/2019, finished 7/6/2020
## What is implemented:
##   - "status" command
##   - "fields" command
##      - Title-cases fields for the frontend's description
##   - query command
##   - reload when any command passed has "reload" in it (with cooldown)
##   - reading entries from json

## If using OverbiteFF, queries must be like name="bob" at this time

## Sample entries.json

# [
#     {
#         "alias": "b-smith",
#         "name": "smith bob c.",
#         "discord": "bsmith#0000",
#         "email": "b-smith@example.edu"
#     },
#     {
#         "alias": "j-smith",
#         "name": "smith john z.",
#         "slack": "\"delete this\"",
#         "email": "j-smith@example.edu"
#     }
# ]

## Add as many fields as necessary

### Config

port = 105  # Typical CCSO port is 105 (as for S/Gopher, no thank you)
reload_cooldown = 60   # how frequently "reload" can be used in a command to reload the database
                       # (in seconds)

always_fields = ["name"] # These are fields that always get returned regardless of query

search_fields = ["name", "species", "affiliation", "universe"]  # Fields that are labeled as indexable

filterable_fields = ["name", "sex", "species", "affiliation", "universe", "site", "email", "discord"]  # When doing returned data option "selected" only these and the indexable fields can be chosen to view

###
from urllib.parse import unquote
import asyncio
import traceback
import json
import time
import re

encoding = "ascii"  # or utf-8?
newline = "\r\n"
x = ['quit', 'stop', 'exit']  # exit commands

last_reload = 0

database = []

def reload_db():
    global database
    with open('entries.json', 'r') as f:
        database = json.load(f)
        print('Database read from entries.json')

reload_db()

def nl(x=''):
    return str(x) + newline

def to_bytes(x):
    if isinstance(x, list):
        return bytes(newline.join(x), encoding)
    else:
        return bytes(str(x), encoding)

class PhProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('Connected by', transport.get_extra_info('peername'))
    
    def data_received(self, data):
        global last_reload
        # self.transport.write(data)
        request = data.decode('utf-8')
        # Scrub command specifically for NSCA Mosaic, the asshole client from hell
        request = unquote(request)
        request = request.replace('/', '')
        print("Client: " + request)
        commands = request.split('\r\n')
        print(commands)
        for cmd in commands:
            args = cmd.split(' ')
            print('', args)
            try:
                if args[0] == 'status':
                    self.transport.write(to_bytes(nl('201:Database ready, read-only.')))
                elif args[0] == 'reload':
                    if (last_reload + 60) <= time.time():
                        reload_db()
                        last_reload = time.time()
                    else:
                        print('-- Please wait', (last_reload + reload_cooldown) - time.time(), 'seconds to reload --')
                elif args[0] == 'fields':
                    unique_fields = []

                    for entry in database:
                        for field in entry:
                            if not field in unique_fields:
                                unique_fields.append(field)

                    results = []
                    keywords = ''

                    _id = 0
                    for field in filterable_fields:
                        _id += 1
                        if field in search_fields:
                            keywords += 'Indexed Lookup '
                        if field in always_fields:
                            keywords += 'Always '
                        if field in filterable_fields:
                            keywords += 'Default'
                        results.append('-200:' + str(_id) + ':' + field + ' max 64 ' + keywords)
                        results.append('-200:' + str(_id) + ':' + field + ': ' + field.title())
                        keywords = ''

                    results.append(nl('200:Ok.'))
                    resp = to_bytes(results)
                    self.transport.write(resp)
                elif args[0] == 'query':
                    if not 'return' in cmd:
                        cmd += " return all"

                    criteria = {}

                    matches = re.finditer(r'(\S*)="([^"]*)"', cmd)

                    for match in matches:
                        criteria[match.group(1)] = match.group(2)

                    return_fields = re.match(r'.* return (.*)', cmd).group(1).split(' ')

                    _all = False

                    if 'all' in return_fields:
                        _all = True

                    results = []
                    entry = 0
                    for item in database:
                        entry += 1
                        meets_criteria = True
                        for key in criteria:
                            if key in item:
                                if not criteria[key].lower() in item[key].lower():
                                    meets_criteria = False
                                    break
                            else:
                                meets_criteria = False
                                break
                        if meets_criteria:
                            for field in database[entry - 1]:
                                if field in return_fields or _all:
                                    results.append('-200:' + str(entry) + ': ' + field + ': ' + database[entry - 1][field])
                    results.append(nl('200:Ok.'))

                    for r in results:
                        print(r)

                    resp = to_bytes(results)
                    self.transport.write(resp)
                elif args[0] in x:
                    print('Client wants to exit')
                    self.transport.write(to_bytes(nl('200:Bye!')))
                    self.transport.close()
                    break
                elif args[0] != "":
                    self.transport.write(to_bytes(nl('514:Unknown command.')))
            except Exception as e:
                traceback.print_exc()
                resp = to_bytes(nl("400:Server error occurred. That gets a yikes from me."))
                self.transport.write(resp)


async def main(h, p):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(PhProtocol, h, p)
    await server.serve_forever()

print('Server is now running')
asyncio.run(main('0.0.0.0', port))