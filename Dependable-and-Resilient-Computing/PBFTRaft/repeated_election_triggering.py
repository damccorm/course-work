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

    '''def __eq__(self, other):
        if (self.ID == other.ID and self.IPAddr == other.IPAddr and self.ctrlPort
            == other.ctrlPort and self.relayPort == other.relayPort):
            return True
        return False'''

thisNode = Node()
thisNode.ID = 0
thisNode.IPAddr = "localhost"
thisNode.ctrlPort = 7228
thisNode.relayPort = 7229


#currentleaderNode = Node()
currentleaderNode = None
oldleaderNode = None
log = []
current_index=0
commit_index = -1
commit_tracker = {}
commit_lock = Lock()
acc_Table = []
drop_table = []
state= ServerStates.FOLLOWER
cluster_count=0
term_number = 0
last_term_i_voted_for = 0
voting_lock = Lock()
seconds = 10
#seconds = random.randint(10,20)
quorum = []

def handle_ctrl_connection(conn, addr):
    global thisNode
    global acc_Table
    global drop_table
    global currentleaderNode
    global last_term_i_voted_for
    global term_number
    global current_index
    global state
    global seconds
    global oldleaderNode
    global quorum
    global commit_index
    global commit_tracker
    global cluster_count
    global commit_lock
    global last_node_i_voted_for
    
    try:
        last_node_i_voted_for
    except:
        last_node_i_voted_for = None

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

        elif message.messageType == ControlMessageTypes.STARTING_ELECTION_PHASE:
            retCode = 0
            if(state == ServerStates.CANDIDATE):
                retMsg = CtrlMessage(MessageTypes.ELECTION_ALREADY_RUNNING, thisNode, retCode)
            else:
                state = ServerStates.FOLLOWER
                term_number = term_number + 1
                retMsg = CtrlMessage(MessageTypes.NOTED, thisNode, retCode)
            conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.ASK_FOR_VOTE:
            retCode = 0
            if len(acc_Table)<=2:
                retMsg = CtrlMessage(MessageTypes.NOT_ENOUGH_NODES_IN_THE_SYSTEM, thisNode, retCode)
                conn.send(serialize_message(retMsg))
            else:
                incoming_term_number  = int(message.extra)
                if incoming_term_number < term_number:
                        retMsg = CtrlMessage(MessageTypes.I_DO_NOT_VOTE_FOR_YOU, thisNode, retCode)
                else:
                    print("Voting for term ",message.extra)
                    last_node_i_voted_for = message.data.IPAddr
                    print("Last node I voted for", last_node_i_voted_for)
                    retMsg = CtrlMessage(MessageTypes.I_VOTE_FOR_YOU, thisNode, retCode)
                    last_term_i_voted_for = incoming_term_number

                conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.I_AM_LEADER:
            cluster_count = len(acc_Table) + 1
            retCode = 0
            flag=0
            quorum_temp = message.extra
            #print("Quorum temp is: ", quorum_temp)
            existing_IP_addr_list = []

            for each_node in acc_Table:
                existing_IP_addr_list.append(each_node.IPAddr)

            #->> Connected
            existing_IP_addr_list.append(thisNode.IPAddr)

            #print("Acc_table IP addresses : ", existing_IP_addr_list)

            for each_voter_in_quorum in quorum_temp:
                print(each_voter_in_quorum)
                # ->> Connected
                #if each_voter not in IP_addr_list and each_voter!= thisNode.IPAddr :
                if each_voter_in_quorum not in existing_IP_addr_list:
                    print("Vote Not Valid")
                    flag=1
                    retMsg = CtrlMessage(MessageTypes.REJECT_NEW_LEADER, thisNode, retCode)
                    conn.send(serialize_message(retMsg))
                    break
                elif each_voter_in_quorum != message.data.IPAddr:
                    # Check if quorum is valid.
                    cur_node = None
                    for n in acc_Table:
                        if n.IPAddr == each_voter_in_quorum:
                            cur_node = n
                    if cur_node is not None:
                        # IF it is none, it must be this node.
                        reply = send_ctrl_message_with_ACK(str(message.data.IPAddr), ControlMessageTypes.DID_YOU_VOTE_FOR_LEADER, 0, cur_node, DEFAULT_TIMEOUT * 4)
                        if reply.messageType == MessageTypes.NOT_WHO_I_VOTED_FOR:
                            # TODO: Ensure that the leader doesn't still have enough votes.
                            print("Vote Not Valid")
                            flag=1
                            retMsg = CtrlMessage(MessageTypes.REJECT_NEW_LEADER, thisNode, retCode)
                            conn.send(serialize_message(retMsg))
                            break
                    elif last_node_i_voted_for is None or str(last_node_i_voted_for) != str(message.data.IPAddr):
                        print("Vote Not Valid")
                        flag=1
                        retMsg = CtrlMessage(MessageTypes.REJECT_NEW_LEADER, thisNode, retCode)
                        conn.send(serialize_message(retMsg))
                        break

            if flag ==0:
                # added as experiment
                seconds = 10

                currentleaderNode = message.data
                # term_number = int(message.extra)
                state = ServerStates.FOLLOWER
                print("---------------------The leader for term ",term_number," is:",message.data.IPAddr,"------------------------")
                retMsg = CtrlMessage(MessageTypes.ACCEPT_NEW_LEADER, thisNode, retCode)
                conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.REPLICATE_LOG:
            retCode = 0

            #check quorum first to authenticate the leader

            flag = 0
            quorum_temp = message.extra
            # print("Quorum temp is: ", quorum_temp)
            existing_IP_addr_list = []

            for each_node in acc_Table:
                existing_IP_addr_list.append(each_node.IPAddr)

            # ->> Connected(if you comment or remove below line , uncomment the line with same tag ->> later and comment the next line which follows)
            existing_IP_addr_list.append(thisNode.IPAddr)

            # print("Acc_table IP addresses : ", existing_IP_addr_list)

            for each_voter_in_quorum in quorum_temp:
                # ->> Connected
                # if each_voter not in IP_addr_list and each_voter!= thisNode.IPAddr :
                if each_voter_in_quorum not in existing_IP_addr_list:
                    print("Vote Not Valid")
                    flag = 1
                    retMsg = CtrlMessage(MessageTypes.REJECT_LOG_REPLICATION_LEADER_FAILED_TO_PROVE_QUORUM, thisNode, retCode)
                    conn.send(serialize_message(retMsg))
                    break

            if flag == 0:
                term_and_index_number = message.data
                print("******Term_and_index_number: " ,len(term_and_index_number))
                #log_index = int(term_and_index_number[0])
                #log_value = int(term_and_index_number[1])
                log_index = term_and_index_number[0]
                log_value = term_and_index_number[1]
                print("%%%%%My current index is: ",current_index)
                print("%%%%%Received index from leader is : ", log_index)
                #log_value = message.data
                #print("*****Quorum satisfied*****")
                if(current_index == log_index):
                    #log[current_index] = message.data
                    log.append(log_value)
                    #print("Log replicated: ", log[current_index])

                    print("Log replicated: ", log)
                    current_index = current_index +1

                    #Below commented code is for old Raft where we inform only the leader about the replicated log.
                    #retMsg = CtrlMessage(MessageTypes.LOG_RECORDED, thisNode, retCode)

                    # Now in PBFT raft we send AppendEntryResponse i.e Ack for Log replication to everybody in the system so that everybody
                    # can take their own decision when to commit the entries.

                    # We initialize the commit count for the replicated entry to 1 because the leader has already replicated it.

                    #We sleep for 6 seconds so that all the replicas record the log first.

                    if len(term_and_index_number)==2:  #when term_and_index_numer has 3 entries it means a replica is catching up
                        commit_tracker[current_index - 1] = 1
                        #time.sleep(6)
                        for servers in acc_Table:
                            send_ctrl_message_with_ACK(current_index-1, ControlMessageTypes.APPEND_ENTRY_RESPONSE_FOR_LOG_REPLICATION, thisNode,
                                                       servers, DEFAULT_TIMEOUT * 4)

                        print("Finished sending APPEND_ENTRY_RESPONSE_FOR_LOG_REPLICATION to servers")

                    else:
                        commit_index = current_index

                    retMsg = CtrlMessage(MessageTypes.LOG_RECORDED, thisNode, retCode)


                elif (current_index < log_index):
                    retMsg = CtrlMessage(MessageTypes.I_AM_BEHIND, current_index, retCode)

                else:
                    print("current index: ",current_index)
                    print("log index: ", log_index)
                    retMsg = CtrlMessage(MessageTypes.ERROR_CONDITION, current_index, retCode)

                conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.APPEND_ENTRY_RESPONSE_FOR_LOG_REPLICATION:
            # when number of Appendentry responses received for a particular entry becomes > (NumberOfNodes/2) , that means the entry has been recorded in
            # majority of servers and can be safely committed.

            replicated_entry_index = message.data

            if commit_index == replicated_entry_index:
                print("Already committed")

            else:

                print("Got APPEND_ENTRY_RESPONSE_FOR_LOG_REPLICATION ")

                commit_lock.acquire()

                if replicated_entry_index in commit_tracker.keys():
                    commit_tracker[replicated_entry_index] = commit_tracker[replicated_entry_index] + 1
                else:
                    commit_tracker[replicated_entry_index] = 1

                commit_lock.release()

                print(commit_tracker)

                #flag = 1
                #while flag==1:
                while True:
                    #commit_lock.acquire()
                    cluster_count = len(acc_Table) + 1
                    if commit_tracker[replicated_entry_index] > cluster_count/2 and len(log)>=replicated_entry_index+1:
                        print(commit_tracker)
                        print("commit_tracker[replicated_entry_index]",commit_tracker[replicated_entry_index])
                        print("cluster_count", cluster_count)
                        print("cluster_count/2", cluster_count/2)
                        commit_index = replicated_entry_index
                        print("Entry committed at index : ", commit_index)
                        print("Current log is : ",log)
                        break
                    time.sleep(5)
                        #flag=0
                    #commit_lock.release()


        elif message.messageType == ControlMessageTypes.UPDATE_YOUR_TERM_NUMBER_FROM_CURRENT_LEADER:
            retCode = 0
            term_number = message.data
            retMsg = CtrlMessage(MessageTypes.UPDATED_MY_TERM, current_index, retCode)
            conn.send(serialize_message(retMsg))


        elif message.messageType == ControlMessageTypes.ACCEPT_REQUEST_FROM_CLIENTS:
            if (state == ServerStates.LEADER):
                retCode = 0
                #time.sleep(8)

                if currentleaderNode==None:
                    retMsg = CtrlMessage(MessageTypes.REPLY_TO_CLIENT, current_index, retCode)
                    conn.send(serialize_message(retMsg))
                    return

                #log[current_index]= term_number
                log.append(term_number)
                print("Log recorded: ",log[current_index])
                commit_tracker[current_index] = 1
                current_index = current_index + 1

                for servers in acc_Table:

                    term_and_index_number = []
                    term_and_index_number.append(current_index-1)
                    term_and_index_number.append(term_number)

                    msg = send_ctrl_message_with_ACK(term_and_index_number, ControlMessageTypes.REPLICATE_LOG,quorum,servers,DEFAULT_TIMEOUT * 10)
                    print("Sent replicate request to ", servers)
                    if(msg.messageType == MessageTypes.I_AM_BEHIND ):
                        starting_index_of_log_of_lagging_server = msg.data



                        #for i in range(starting_index_of_log_of_lagging_server,current_index):
                        for i in range(starting_index_of_log_of_lagging_server, commit_index):
                            term_and_index_number = []
                            term_and_index_number.append(i)
                            term_and_index_number.append(log[i])
                            # When a replica is catching up it does not need to send APPEND ENTRY RESPONSES
                            # for replicating that log to other servers. So we are adding -1 to denote that.
                            term_and_index_number.append(-1)
                            send_ctrl_message_with_ACK(term_and_index_number, ControlMessageTypes.REPLICATE_LOG, quorum,servers, DEFAULT_TIMEOUT * 10)

                        for i in range(commit_index, current_index):
                            term_and_index_number = []
                            term_and_index_number.append(i)
                            term_and_index_number.append(log[i])
                            # Now that the replica is caught up,send the latest client request to be replicated the replica

                            send_ctrl_message_with_ACK(term_and_index_number, ControlMessageTypes.REPLICATE_LOG, quorum,servers, DEFAULT_TIMEOUT * 10)

                        send_ctrl_message_with_ACK(term_number, ControlMessageTypes.UPDATE_YOUR_TERM_NUMBER_FROM_CURRENT_LEADER, i,
                                                   servers, DEFAULT_TIMEOUT * 10)


                    elif (msg.messageType == MessageTypes.REJECT_LOG_REPLICATION_LEADER_FAILED_TO_PROVE_QUORUM):
                        print("I am caught impersonating a Leader")
                        commit_tracker[current_index-1] = 0

                        # add code to in for client about faulty leader

                    elif (msg.messageType == MessageTypes.LOG_RECORDED):
                        print("Log that I sent was recorded by the replica")

                    elif (msg.messageType == MessageTypes.ERROR_CONDITION):
                        print("Error condition")



                print("Leader sent replicate request to all replicas")
                retMsg = CtrlMessage(MessageTypes.REPLY_TO_CLIENT, commit_index, retCode)

                conn.send(serialize_message(retMsg))
                print("Sent reply to Client")

            else:
                if currentleaderNode != None:
                    retCode = 0
                    msg = send_ctrl_message_with_ACK(message.data, ControlMessageTypes.ACCEPT_REQUEST_FROM_CLIENTS,0 , currentleaderNode,
                                                     DEFAULT_TIMEOUT *100)

                    if msg.messageType == MessageTypes.REPLY_TO_CLIENT:
                        retMsg = CtrlMessage(MessageTypes.REPLY_TO_CLIENT, current_index, retCode)
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
                if (i.IPAddr not in a) and (i.IPAddr != thisNode.IPAddr) and (i.IPAddr not in b):
                    acc_Table.append(i)

            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, retCode)
            conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.HEARTBEAT:
            retCode = 0
            seconds = 10
            #seconds = random.randint(10, 20)
            currentleaderNode = message.data
            retMsg = CtrlMessage(MessageTypes.MSG_ACK, thisNode, retCode)
            conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.CLIENT_INTERVENTION:
            print("Client Intervention received")
            retCode = 0
            state = ServerStates.FOLLOWER
            seconds = 10
            oldleaderNode = currentleaderNode
            currentleaderNode = None
            for servers in acc_Table:
                msg = send_ctrl_message_with_ACK(term_number, ControlMessageTypes.CLIENT_INTERVENTION_RECEIVED, current_index, servers,
                                                 DEFAULT_TIMEOUT * 10)

            while(1):
                #Wait till new election gives a new leader
                if currentleaderNode == None:
                    time.sleep(2)
                else:
                    print("Old Leader: "+ oldleaderNode.IPAddr)
                    print("New Leader: " + currentleaderNode.IPAddr)
                    if currentleaderNode.IPAddr == oldleaderNode.IPAddr:
                        currentleaderNode = None
                        seconds = 10
                        print("Same leader elected again. Start Election again")
                        for servers in acc_Table:
                            msg = send_ctrl_message_with_ACK(term_number,ControlMessageTypes.CLIENT_INTERVENTION_RECEIVED,current_index, servers,
                                                             DEFAULT_TIMEOUT * 10)

                    else:
                        print("********&&&&&&^%$#$%^&*(*&^%$%^&*(*&^New Leader Elected^&*)(*&^%$$%^&*(*&^%$#$%^&*(*&^%$#$%^&*(")

                        break

            retMsg = CtrlMessage(MessageTypes.NEW_LEADER_ELECTED, currentleaderNode, retCode)
            conn.send(serialize_message(retMsg))
            #start_leader_election()

        elif message.messageType == ControlMessageTypes.CLIENT_INTERVENTION_RECEIVED:
            retCode = 0
            state = ServerStates.FOLLOWER
            currentleaderNode = None
            seconds = 10

            retMsg = CtrlMessage(MessageTypes.NEW_LEADER_ELECTED, thisNode, retCode)
            conn.send(serialize_message(retMsg))

        elif message.messageType == ControlMessageTypes.DID_YOU_VOTE_FOR_LEADER:
            if last_node_i_voted_for is None or str(last_node_i_voted_for) != message.data:
                retMsg = CtrlMessage(MessageTypes.NOT_WHO_I_VOTED_FOR, 0, 0)
                conn.send(serialize_message(retMsg))
            else:
                retMsg = CtrlMessage(MessageTypes.WHO_I_VOTED_FOR, 0, 0)
                conn.send(serialize_message(retMsg))


def join_network(someNode):
    global thisNode
    global acc_Table
    message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.JOIN_NETWORK, 0, someNode,
                                         DEFAULT_TIMEOUT * 10)
    if message is None:
        print("Timeout or Error")
        return 0
        # TODO: handle this
        #pass
    print ("return IP", message.data.IPAddr)
    acc_Table.append(message.data)
    return message.data

def stabilization_routine():
    global thisNode
    global acc_Table
    global drop_table

    #time.sleep(random.randint(1,10))
    while 1:
        for i in acc_Table:
            message = send_ctrl_message_with_ACK(acc_Table, ControlMessageTypes.SYNC_NETWORK, 1,i,
                                       DEFAULT_TIMEOUT * 10)
            if message.messageType == ControlMessageTypes.NODE_DROP:
                print("Bu hu")
                drop_table.append(message.data)
                print("Length of drop table: ",len(drop_table))
                acc_Table.remove(i)
                time.sleep(40)
                drop_table.remove(message.data)
                print("Length of drop table: ", len(drop_table))
                print("Removed: ", i.IPAddr)
            #else:
            #    print(message.data)
            #time.sleep(random.randint(1,2))

def start_leader_election():
    global thisNode
    global term_number
    global currentleaderNode
    global state
    global voting_lock
    global quorum

    #voting_lock.acquire()


    if len(acc_Table)<=2:
        print("Not enough servers yet for PBFT raft.")
        currentleaderNode = None
        #voting_lock.release()
        return

    voting_lock.acquire()

    state = ServerStates.CANDIDATE
    cluster_count = len(acc_Table)+1
    print("--------Total servers in cluster:",cluster_count,"-------")
    print("My state is: Candidate")
    count=1

    for server in acc_Table:
        message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.STARTING_ELECTION_PHASE, term_number, server,
                                         DEFAULT_TIMEOUT * 10)
        if (message.messageType == MessageTypes.ELECTION_ALREADY_RUNNING):
            state = ServerStates.FOLLOWER
            print("Election already running")
            voting_lock.release()
            return

    term_number = term_number + 1

    '''for server in acc_Table:
        message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.ASK_FOR_VOTE, term_number, server,
                                         DEFAULT_TIMEOUT * 10)

        if(message.messageType == MessageTypes.I_VOTE_FOR_YOU):
            count=count+1
            quorum.append(message.data.IPAddr)
            if(count>cluster_count/2):
                state = ServerStates.LEADER
                currentleaderNode=thisNode
                print("------I am the leader for term ",term_number,"------")
                break

    if(state == ServerStates.LEADER):
        for i in acc_Table:
            #message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.I_AM_LEADER, term_number, i,DEFAULT_TIMEOUT * 10)
            message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.I_AM_LEADER, quorum, i,DEFAULT_TIMEOUT * 10)
            if message.messageType == MessageTypes.REJECT_NEW_LEADER :
                state = ServerStates.FOLLOWER
                currentleaderNode = None
                print("------Other nodes rejected my leadership in term ", term_number, "------")
    else:
        print("You cannot become leader")
        state = ServerStates.FOLLOWER'''

    quorum = []
    for server in acc_Table:
        message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.ASK_FOR_VOTE, term_number, server,
                                             DEFAULT_TIMEOUT * 10)

        if (message.messageType == MessageTypes.I_VOTE_FOR_YOU):
            count = count + 1
            quorum.append(message.data.IPAddr)
            if (count > cluster_count / 2):
                #state = ServerStates.LEADER
                #currentleaderNode = thisNode
                #print("------I am the leader for term ", term_number, "------")
                print("Quorum is: ", quorum)
                break

        if (message.messageType == MessageTypes.NOT_ENOUGH_NODES_IN_THE_SYSTEM):
            print("Not enough servers yet for PBFT raft.")
            state = ServerStates.FOLLOWER
            currentleaderNode = None
            voting_lock.release()
            return

    flag= 0
    #if (state == ServerStates.LEADER):
    if (count > cluster_count / 2):
        for i in acc_Table:
            # message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.I_AM_LEADER, term_number, i,DEFAULT_TIMEOUT * 10)
            message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.I_AM_LEADER, quorum, i,
                                                 DEFAULT_TIMEOUT * 10)
            if message.messageType == MessageTypes.REJECT_NEW_LEADER:
                state = ServerStates.FOLLOWER
                currentleaderNode = None
                print("------Other nodes rejected my leadership in term ", term_number, "------")
                flag = 1
                break

        if flag ==0:
            state = ServerStates.LEADER
            currentleaderNode = thisNode
            print("------I am the leader for term ", term_number, "------")

    else:
        print("You cannot become leader")
        state = ServerStates.FOLLOWER

    voting_lock.release()

def heartbeat_routine():
    global state

    while 1:
        if (state == ServerStates.LEADER):
            for server in acc_Table:
                message = send_ctrl_message_with_ACK(thisNode, ControlMessageTypes.HEARTBEAT, term_number, server,
                                                 DEFAULT_TIMEOUT * 10)
        #good value
        time.sleep(5)

        #bad value
        #time.sleep(13)


def display_state_of_server():
    global state
    global currentleaderNode
    while 1:
        if(state == ServerStates.FOLLOWER):
            print("My state is : Follower")
        elif(state == ServerStates.LEADER):
            print("My state is : Leader")
        else:
            print("My state is : Candidate")

        if state==ServerStates.FOLLOWER:
            if currentleaderNode != None:
                print("My Leader is :"+ currentleaderNode.IPAddr)

        if len(acc_Table)<=2:
            state = ServerStates.FOLLOWER
            currentleaderNode = None

        print("Number of nodes in the system:",len(acc_Table))

        time.sleep(30)

def leader_timeout_routine():
    global seconds
    while 1:
        #if (state == ServerStates.FOLLOWER and currentleaderNode!=None) or (state == ServerStates.CANDIDATE and currentleaderNode!=None):
        if state == ServerStates.FOLLOWER or state == ServerStates.CANDIDATE:
            print("STARTING ELECTION")
            start_leader_election()



def main():
    global thisNode
    global acc_Table
    global drop_table
    global log
    global state


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
        print ("Please specify the IP with the -p option.")
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
    print ("Sleeping for 1 seconds while listening threads are created.")
    time.sleep(1)

    stabilizer = Thread(target=stabilization_routine)
    stabilizer.daemon = True
    stabilizer.start()

    stabilizer = Thread(target=heartbeat_routine)
    stabilizer.daemon = True
    stabilizer.start()

    display_State_Routine = Thread(target=display_state_of_server)
    display_State_Routine.daemon = True
    display_State_Routine.start()

    leader_timeout = Thread(target=leader_timeout_routine)
    leader_timeout.daemon = True
    leader_timeout.start()

    # Wait forever
    while 1:
        # The threads should never die
        listenCtrlThread.join(1)
        '''print("\nOptions:\n")
        print("Press 1 to start leader election\n")
        print("Press 2 to print log status\n")'''

        j = input("")

        #if (j == "1"):
        #    start_leader_election()


        if j=="2" :
            for i in log:
                print(i)

        else:
            print("Incorrect Input")

    return 0

if __name__ == "__main__":
    main()
