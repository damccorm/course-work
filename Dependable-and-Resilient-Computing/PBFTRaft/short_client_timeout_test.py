from network_ctrl import *
from socket import *
import time
from threading import *
import signal
import sys
import copy
from optparse import OptionParser
import random

TIME_OUT = 15
class Node():
    ID = 0
    IPAddr = "localhost"
    ctrlPort = 7228
    relayPort = 7229

    def __eq__(self, other):
        if (self.ID == other.ID and self.IPAddr == other.IPAddr and self.ctrlPort
            == other.ctrlPort and self.relayPort == other.relayPort):
            return True
        return False

seconds = TIME_OUT
request_sent = 0

def client_request_timeout(knownNode):
    global seconds
    global request_sent
    while 1:
        if(request_sent==1):
            if (seconds > -1):
                print("\nSeconds: "+str(seconds))
                time.sleep(1);
                seconds -= 1;
            else:
                # PBFT Raft timed out, start leader election by client intervention
                seconds = TIME_OUT
                print("Client timed out")

                while 1:
                    if request_sent==1:
                        request_sent = 0
                        print("Sending new leader election message")
                        message = send_ctrl_message_with_ACK("blah", ControlMessageTypes.CLIENT_INTERVENTION, 0, knownNode,DEFAULT_TIMEOUT * 4)
                        if message.messageType == MessageTypes.NEW_LEADER_ELECTED:
                            print("New leader elected: "+ message.data.IPAddr)
                        break
                request_sent = 0


def main():
    global seconds
    global request_sent
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-e", "--existingnode",
                      action="store",
                      type="string",
                      dest="existingnode",
                      help="Use an existing node to join an existing network.")
    parser.add_option("-p", "--myIP",
                      action="store",
                      type="string",
                      dest="myIP",
                      help="IP of service.")

    (options, args) = parser.parse_args()

    if options.myIP is None:
        print "Please specify the IP with the -p option."
        exit(0)

    thisNode = Node()
    thisNode.IPAddr = options.myIP

    if options.existingnode is not None:
        tmpNode = Node()
        tmpNode.IPAddr = options.existingnode

    #client_timeout = Thread(target=client_request_timeout,args=(tmpNode,))
    #client_timeout.daemon = True
    #client_timeout.start()



    while 1:
        j = raw_input("")
        if j == "1":
            request_sent = 1
            print("Sending....")
            message = send_ctrl_message_with_ACK("blah", ControlMessageTypes.ACCEPT_REQUEST_FROM_CLIENTS, 0 ,tmpNode ,15)

            '''if message != None:
                if message.messageType == MessageTypes.REPLY_TO_CLIENT:
                    if request_sent==0:
                        print("Response late. Discarding the response from server.")
                        request_sent=1
                    else:
                        print("Your command got executed in time.")
                        print("Commit Index is: ",message.data)
                        request_sent = 0
                        seconds = TIME_OUT
                else:
                    print("Timed out")'''
            if message != None:
                if message.messageType == MessageTypes.REPLY_TO_CLIENT:
                    print("Your command got executed in time.")
                    print("Commit Index is: ", message.data)
                else:
                    print("Timed out. Asking for client Intervention....")
                    message = send_ctrl_message_with_ACK("blah", ControlMessageTypes.CLIENT_INTERVENTION, 0, tmpNode,
                                                     DEFAULT_TIMEOUT * 4)
                    if message.messageType == MessageTypes.NEW_LEADER_ELECTED:
                        print("New leader elected: " + message.data.IPAddr)
            else:
                print("Timed out. Asking for client Intervention....")
                message = send_ctrl_message_with_ACK("blah", ControlMessageTypes.CLIENT_INTERVENTION, 0, tmpNode,
                                                     DEFAULT_TIMEOUT * 4)
                if message.messageType == MessageTypes.NEW_LEADER_ELECTED:
                    print("New leader elected: " + message.data.IPAddr)


if __name__ == "__main__":
    main()
