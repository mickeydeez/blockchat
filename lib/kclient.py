from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from lib.blockchain import Blockchain
from threading import Thread
from pprint import pprint
import socket
import select
import string
import sys
import base64
import binascii

Builder.load_string("""
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
""")

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class ClientApp(App):

    def __init__(self, alias='guest', server='127.0.0.1', port=5000, **kwargs):
        super(ClientApp, self).__init__(**kwargs)
        self.alias = alias
        self.server = server
        self.port = int(port)
        self.blockchain = Blockchain(alias)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.textbox = None
        self.label = None

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        Config.set('graphics', 'width', '200')
        Config.set('graphics', 'height', '200')
        Window.size = (500, 300)
        layout = BoxLayout(orientation='vertical')
        layout.bind(minimum_height=layout.setter('height'))
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = ScrollableLabel(text='connecting...')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    def connect_to_server(self):
        try:
            self.s.connect((self.server, self.port))
            self.label.text = "Connected to %s:%s\n" % (self.server, self.port)
            listener = Thread(target=self.receive_messages).start()
        except Exception as e:
            self.label.text = "Failed to connect to %s:%s\n%s\n" % (self.server, self.port, e)

    def send_message(self, *args):
        msg = self.textbox.text
        if msg:
            if "?chain" in msg:
                self.label.text += "Dumping chain to ./blockchain.json\n"
                with open('blockchain.json', 'wt') as out:
                    pprint(self.blockchain.chain, stream=out)
                self.textbox.text = ""
            else:
                block = self.blockchain.send_block(msg)
                payload = base64.b64encode(block.encode('utf-8'))
                try:
                    self.s.send(payload)
                    self.label.text += "<{}> {}\n".format(self.alias, msg)
                except BrokenPipeError:
                    self.label.text += "You aren't connected!\n"
                self.textbox.text = ""

    def receive_messages(self):
        while True:
            socket_list = [sys.stdin, self.s]
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
            for sock in read_sockets:
                if sock == self.s:
                    data = sock.recv(4096).decode('utf-8')
                    if not data:
                        sys.exit()
                    elif 'entered room' in data:
                        self.label.text += "{}".format(data)
                    else:
                        split = data.split('>')
                        ldata = "%s>" % split[0]
                        rdata = ''.join(split[1:]).encode('utf-8')
                        decoded = base64.b64decode(rdata)
                        block = self.blockchain.recv_block(decoded.decode('utf-8'))
                        txn = block['contents']['txns']
                        lident = list(txn.keys())[0]
                        rident = list(txn.values())[0]
                        display = "<%s> %s" % (lident, rident)
                        self.label.text += "{}".format(display)
                        self.label.scroll_to(display)
