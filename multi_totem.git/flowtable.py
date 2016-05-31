from multiprocessing import Process
from entropy_tools import construct_hashes
from entropy_algo import entropy
from entropy_correlation import seek_ddos
import time
import datetime



class sflow_postprocess(Process):
    
    def __init__ (self,flowtable,cycle_count, action, monitoring):
        Process.__init__(self)
        self.action = action
        self.time_started = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_ended = time.time()
        self.flowtable = flowtable
        self.monitoring = monitoring
        self.cycle_count = cycle_count
        
    def run(self):

        if self.action == 'entropy':
            hashes = construct_hashes(self.flowtable)
            entropies = entropy(hashes)
            self.time_ended = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur_monitoring_entry = {'start':self.time_started, \
                                    'end':self.time_ended, \
                                    #'hashes':hashes, \
                                    'entropies':entropies}
            self.monitoring.append(cur_monitoring_entry)
            

            #===================================================================
            # #Standard Output - NEEDS 'hashes' enabled at cur_monitoring_entry
            # print "-------------------------------"
            # print "Total Current Flows:"+str(self.monitoring[-1]['hashes'].sum_flows)
            # if len(self.monitoring) >= 2:
            #  print "Total Previous Flows:"+str(self.monitoring[-2]['hashes'].sum_flows)
            #  print "Flow Difference: "+str(self.monitoring[-1]['hashes'].sum_flows - self.monitoring[-2]['hashes'].sum_flows)
            # print "Total Packets:"+str(self.monitoring[-1]['hashes'].sum_packets)
            # print "-------------------------------"
            # print ""
            #===================================================================
            result = 'OK'
            try:
                check=[]
                check.append(self.monitoring[-2]['entropies'])
                check.append(self.monitoring[-1]['entropies'])
                result = seek_ddos(check)
            except:
                pass


            #Entropies Output - NEEDS 'entropies' enabled at cur_monitoring_entry
            print "-------------------------------"
            print ""
            print "DstIP Flows: "+str(self.monitoring[-1]['entropies']['dstip_flows'])
            if len(self.monitoring) >= 2:
                print "changed by "+str(self.monitoring[-1]['entropies']['dstip_flows'] - self.monitoring[-2]['entropies']['dstip_flows'])
            print ""
            print "DstPORT Flows: "+str(self.monitoring[-1]['entropies']['dstport_flows'])
            if len(self.monitoring) >= 2:
                print "changed by "+str(self.monitoring[-1]['entropies']['dstport_flows'] - self.monitoring[-2]['entropies']['dstport_flows'])
            print "-------------------------------"
            print ""
            print "RESULT: "+result

        else:
            pass #To Use for other methods / A/D aglorithms
        #for item in self.flowtable:     #####
        #    self.total_flows+=1
        #print self.total_flows


    #===========================================================================
    # def no_of_flows(self):
    #    self.time_ended = time.time()
    #    return self.time_started, self.total_flows, self.time_ended     
    #===========================================================================