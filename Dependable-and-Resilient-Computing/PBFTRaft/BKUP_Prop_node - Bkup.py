from network_ctrl import *
from socket import *
import time
from threading import *
import signal
import sys
import copy
from optparse import OptionParser
import random


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

thisNode = Node()
thisNode.ID = 0
thisNode.IPAddr = "localhost"
thisNode.ctrlPort = 7228
thisNode.relayPort = 7229

acc_Table = []
drop_table = []
ProposalID = 0
LastProposalID = 0
SendProposalValue = ''
ProposalValue = {}
ProposalValueLock = Lock()
Acks_Cnt = set()
Acks_CntLock = Lock()
Accept_Cnt = set()
Accept_CntLock = Lock()
Anti_Dict = {}
Anti_DictLock = Lock()
Quo_Cnt = 0

ProposeFlag = 0
ProposeFlagLock = Lock()

SendFlag = 0
SendFlagLock = Lock()

PaxosFlag = 0
PaxosFlagLock = Lock()


def handle_ctrl_connection(conn, addr):
    global thisNode
    global acc_Table
    global drop_table
    global ProposalID
    global LastProposalID
    global ProposalValue
    global Acks_Cnt
    global Anti_Dict
    global SendFlag
    global SendFlagLock
    global ProposeFlagLock
    global Anti_DictLock
    global ProposalValueLock
    global SendProposalValue
    global Accept_Cnt
    global Accept_CntLock
    global PaxosFlag
    global PaxosFlagLock


    data = conn.recv(MAX_REC_SIZE)
    conn.settimeout(DEFAULT_TIMEOUT)

    if data:
        message = unserialize_message(data)

        if message.messageType == ControlMessageTypes.JOIN_NETWORK:
            retCode = 0
            inNode = copy.deepcopy(message.data)
            acc_Table.append(inNode)
            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, retCode)
            conn.send(serialize_message(retMsg))
        elif message.messageType == ControlMessageTypes.SYNC_NETWORK:
            retCode = 0
            a = set()
            b = set()
            for i in acc_Table:
                a.add(i.IPAddr)
            for i in drop_table:
                b.add(i.IPAddr)
            for i in message.data:
                if (i.IPAddr not in a) and (i.IPAddr <> thisNode.IPAddr) and (i.IPAddr not in b):
                    acc_Table.append(i)

            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, retCode)
            conn.send(serialize_message(retMsg))
        elif message.messageType == ControlMessageTypes.LEADER_PROPOSE:
            print("Incoming Proposal Number ", message.data)
            inPID = int(message.data)
            if LastProposalID < inPID: #ProposalID == 0 and
                print("1..................1")
                send_Leader_Response(message.extra, ControlMessageTypes.LEADER_GO)
                print("2..................2")
                retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, 0)
                conn.send(serialize_message(retMsg))
            else:
                print("4..................4")
                send_Leader_Response(message.extra,ControlMessageTypes.LEADER_NO)
                retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, 0)
                print("6..................6")
                conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.LEADER_GO:
            print("7.....................7")
            Acks_CntLock.acquire()
            Acks_Cnt.add(message.data.IPAddr)
            print("+++++++++++++++++++++++++++++++++++++++++")
            print(Acks_Cnt)
            print("+++++++++++++++++++++++++++++++++++++++++")
            if(len(Acks_Cnt) >= Quo_Cnt):
                SendFlagLock.acquire()
                SendFlag = 1
                SendFlagLock.release()
            Acks_CntLock.release()
            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, 0)
            conn.send(serialize_message(retMsg))
        elif message.messageType == ControlMessageTypes.LEADER_NO:
            #Currently only if ur proposal id is old
            print("8.....................8")
            Anti_DictLock.acquire()
            x,y = message.data
            Anti_Dict[x] = y
            Anti_DictLock.release()
            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, 0)
            conn.send(serialize_message(retMsg))
        elif message.messageType == ControlMessageTypes.SEND_VAL:
            ProposalValueLock.acquire()
            x,y = message.data
            if x in ProposalValue.keys():
                print("Old Value Returned")
            else:
                ProposalValue[x] = y
                LastProposalID = x
            ProposalValueLock.release()
            send_Leader_Response(message.extra,ControlMessageTypes.VAL_ACCEPTED)
            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, 0)
            print("$$$$$$---VAL ACCEPTED---$$$$$$$")
            conn.send(serialize_message(retMsg))
        elif message.messageType == ControlMessageTypes.VAL_ACCEPTED:
            #Learnt a new Value
            Accept_CntLock.acquire()
            Accept_Cnt.add(message.data.IPAddr)
            if (len(Accept_Cnt) >= Quo_Cnt):
                ProposalValueLock.acquire()
                ProposalValue[ProposalID] = SendProposalValue
                #ProposalValueLock.release()
                Accept_Cnt = set()
                Acks_CntLock.acquire()
                Acks_Cnt = set()
                Acks_CntLock.release()
                PaxosFlagLock.acquire()
                PaxosFlag = 0
                PaxosFlagLock.release()
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("---------PAXOS ROUND COMPLETED------------")
                print(ProposalValue)
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                ProposalValueLock.release()
            Accept_CntLock.release()




def send_Leader_Response(someNode, msgType):
    global thisNode
    #time.sleep(random.randint(4,10))
    if msgType == ControlMessageTypes.LEADER_NO:
        send_ctrl_message_with_ACK1((LastProposalID,ProposalValue[LastProposalID]), msgType, 3, someNode, DEFAULT_TIMEOUT * 4)
    elif msgType == ControlMessageTypes.LEADER_GO:
        send_ctrl_message_with_ACK1(thisNode, msgType, 3, someNode, DEFAULT_TIMEOUT * 4)
    elif msgType == ControlMessageTypes.VAL_ACCEPTED:
        send_ctrl_message_with_ACK1(thisNode, msgType, 4, someNode, DEFAULT_TIMEOUT * 4)





def join_network(someNode):
    global thisNode
    global acc_Table
    message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.JOIN_NETWORK, 0, someNode,
                                         DEFAULT_TIMEOUT * 4)
    if message is None:
        print("Timeout or Error")
        return 0
        # TODO: handle this
        #pass
    print ("return IP", message.data.IPAddr)
    acc_Table.append(message.data)
    return message.data

def paxos_Test():
    return 0

def stabilization_routine():
    global thisNode
    global acc_Table
    global drop_table

    time.sleep(random.randint(1,10))
    while 1:
        for i in acc_Table:
            message = send_ctrl_message_with_ACK(acc_Table, ControlMessageTypes.SYNC_NETWORK, 1,i,
                                       DEFAULT_TIMEOUT * 4)
            if message.messageType == ControlMessageTypes.NODE_DROP:
                print("Bu hu")
                drop_table.append(message.data)
                print("Length of drop table: ",len(drop_table))
                acc_Table.remove(i)
                time.sleep(40)
                drop_table.remove(message.data)
                print("Length of drop table: ", len(drop_table))
                print("Removed: ", i.IPAddr)
            else:
                print(message.data)
            time.sleep(random.randint(4,7))


'''
def Run_Paxos():
    global thisNode
    global acc_Table
    global drop_table
    global ProposalID
    global LastProposalID
    global Anti_Dict
    global Acks_Cnt
    global Quo_Cnt
    global ProposalValue

    if (len(acc_Table) < 3):
        print("Not enough acceptors")
        return "Cannot Start a Paxos Round"

    if len(drop_table)> 0 and ProposalID == 0:
        print("===================================")
        print("SYSTEM STILL STABILIZING...PLZ WAIT")
        print("===================================")
        return "Cannot Start a Paxos Round"

    Quo_Cnt = len(acc_Table) / 2 + 1
    print("Quorum Requirement: ", Quo_Cnt)
    #Propose_Paxos()
    #wait_for_ctrl_connections(thisNode,Propose_Paxos())
    Propose_Paxos()
    Ctrr = 0
    time.sleep(2)
    while Ctrr ==0:
        if len(Acks_Cnt) > Quo_Cnt:
            print("*******************READY FOR PHASE 2*****************************")
            Ctrr = 1
        else:
            print("-----------------Time TO SLEEP----------------")
            time.sleep(2)


    #time.sleep(10)
    #print("*******************BACK FROM SLEEP*************************")

    while len(Acks_Cnt) <= Quo_Cnt:
        print("+++++++++++++++++++++++++++++++++++++++++")
        print(Acks_Cnt)
        print("+++++++++++++++++++++++++++++++++++++++++")
        print("Waiting for all Acks")


    #if len(Acks_Cnt) > Quo_Cnt:
    #    print("*******************READY FOR PHASE 2*****************************")


    return "Completed a PAXOS Round"


def Propose_Paxos():
    global thisNode
    global acc_Table
    global ProposalID
    global LastProposalID
    #global drop_table

    if len(drop_table)> 0:
        print("===================================")
        print("SYSTEM STILL STABILIZING...PLZ WAIT")
        print("===================================")
        return ControlMessageTypes(ControlMessageTypes.NO_GO,thisNode,0)
    else:

    ProposalID = LastProposalID + 1
    for i in acc_Table:
        message = send_ctrl_message_with_ACK1(ProposalID, ControlMessageTypes.LEADER_PROPOSE, thisNode, i,
                                             DEFAULT_TIMEOUT * 4)
        print(message.data)

    print("PROPOSING COMPLETE.................---->>>>>>>")

'''

def Propose_Paxos():
    global thisNode
    global acc_Table
    global drop_table
    global ProposalID
    global LastProposalID
    global Anti_Dict
    global Acks_Cnt
    global Quo_Cnt
    global ProposalValue
    global ProposeFlag

    time.sleep(1)

    while 1:
        ProposeFlagLock.acquire()
        i = ProposeFlag
        ProposeFlag = 0
        ProposeFlagLock.release()
        if i == 1:
            print("----------------------------In deamon--------------------------------")
            ProposalID = LastProposalID + 1
            for i in acc_Table:
                message = send_ctrl_message_with_ACK1(ProposalID, ControlMessageTypes.LEADER_PROPOSE, thisNode, i,
                                                      DEFAULT_TIMEOUT * 4)
        else:
            time.sleep(5)



def Send_Paxos():
    global SendFlag
    global SendFlagLock
    global Anti_DictLock
    global Anti_Dict
    global ProposalID
    global LastProposalID
    global ProposalValue
    global SendProposalValue

    time.sleep(1)
    while 1:
        SendFlagLock.acquire()
        k = SendFlag
        SendFlag = 0
        SendFlagLock.release()
        if k == 1:
            print("!!!!!!!!@@@@@Proposal Complete@@@@@!!!!!!!!!!!")
            Anti_DictLock.acquire()
            local_Dict = copy.deepcopy(Anti_Dict)
            Anti_DictLock.release()
            ADLen = len(local_Dict.keys())
            if ADLen >0:
                ProposalID = max(local_Dict.keys())
                LastProposalID = ProposalID
                SendProposalValue = local_Dict[ProposalID]
            else:
                ranVal = 'A' + str(random.randint(100,999))
                SendProposalValue = copy.deepcopy(ranVal)
            for i in acc_Table:
                message = send_ctrl_message_with_ACK1((ProposalID,SendProposalValue), ControlMessageTypes.SEND_VAL, thisNode, i,
                                                      DEFAULT_TIMEOUT * 4)

        else:
            time.sleep(5)



def main():
    global thisNode
    global acc_Table
    global drop_table
    global ProposalID
    global LastProposalID
    global Anti_Dict
    global Acks_Cnt
    global Quo_Cnt
    global ProposalValue
    global ProposeFlag
    global Acks_CntLock
    global Accept_Cnt
    global Accept_CntLock
    global SendProposalValue
    global PaxosFlag
    global PaxosFlagLock


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

    thisNode.IPAddr = options.myIP

    if options.existingnode is not None:
        tmpNode = Node()
        tmpNode.IPAddr = options.existingnode
        join_network(tmpNode)

    print("MY IP ADDRESS IS ", thisNode.IPAddr)

    listenCtrlThread = Thread(target=wait_for_ctrl_connections, args=(thisNode, handle_ctrl_connection))
    listenCtrlThread.daemon = True
    listenCtrlThread.start()
    print "Sleeping for 1 seconds while listening threads are created."
    time.sleep(1)

    stabilizer = Thread(target=stabilization_routine)
    stabilizer.daemon = True
    stabilizer.start()

    Propose_Routine = Thread(target=Propose_Paxos)
    Propose_Routine.daemon = True
    Propose_Routine.start()

    Send_Routine = Thread(target=Send_Paxos)
    Send_Routine.daemon = True
    Send_Routine.start()


    # Wait forever
    while 1:
        # The threads should never die
        listenCtrlThread.join(1)
        # listenThread.join(1)
        print("\nOptions:\n")
        print("1: Press 1 to print expored node list\n")
        print("2: Press 2 to start a paxos round")
        print("3: Press 3 to print Paxos Information")
        j = raw_input("")
        print("You selected: ", j)
        if (j == "1"):
            try:
                for i in acc_Table:
                    print(i.IPAddr)
                    print("\n")
            except:
                print(acc_Table)
        elif j == "2" :
            print("Chappa Chappa Charkha Chale")
            if (len(acc_Table) < 3):
                print("Not enough acceptors")
                #return "Cannot Start a Paxos Round"
            elif len(drop_table) > 0 and ProposalID == 0:
                print("===================================")
                print("SYSTEM STILL STABILIZING...PLZ WAIT")
                print("===================================")
                return "Cannot Start a Paxos Round"
            elif PaxosFlag == 0:
                PaxosFlagLock.acquire()
                PaxosFlag = 1
                PaxosFlagLock.release()
                Accept_CntLock.acquire()
                Accept_Cnt = set()
                Accept_CntLock.release()
                Acks_CntLock.acquire()
                Acks_Cnt = set()
                Acks_CntLock.release()
                Quo_Cnt = len(acc_Table) / 2 + 1
                print("Quorum Requirement: ", Quo_Cnt)
                ProposeFlagLock.acquire()
                ProposeFlag = 1
                ProposeFlagLock.release()
                print("Propose Flag SET")
            else:
                print("Can't Start a Paxos Round NOW")
                #print(Run_Paxos())
            #wait_for_ctrl_connections(thisNode,get_leader())
        elif j == 3:
            ProposalValueLock.acquire()
            print(ProposalValue)
            ProposalValueLock.release()
        else:
            print("Incorrect Input")

    return 0

if __name__ == "__main__":
    main()
