# ******************************************************************************
# graph_entropy_method.py
#
# Drift Detector, Detect drift point in Graph Stream
#
#
# Date      Name       Description
# ========  =========  ========================================================
# 03/20/2018  Paudel     Initial version,
#
# ******************************************************************************
import os
import math
import statistics
from random import shuffle
from properties import GBAD, GraphEntropy
from graph.dataset import Dataset

class GraphEntropyMethod:
    XP = 1
    flag = "w"
    subgraph_list = {}
    subgraph_id = 0
    is_isomorphic = False
    graphWindow = {}

    def __init__(self):
        # remove graph file if exist
        try:
            os.remove(GBAD.graphFolder + "/win_1G.g")
            os.remove(GBAD.graphFolder + "/win_1G.g")
        except OSError:
            pass

    @staticmethod
    def getTotalSubgraphCount(subgraph):
        '''
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
        # NAME: getTotalSubgraphCount
        #
        # INPUTS: (subgraph) List of subgraph in this window
        #
        # RETURN: (total) count of total subgraph
        #
        # PURPOSE: Get the total count of subgraph in current window  for calculating Entropy
        #
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
        :param subgraph:
        :return:
        '''
        total = 0
        pos = 0
        neg = 0
        for s in subgraph.keys():
            # print("S: ", s)
            total += int(subgraph[s][0])
            pos += int(subgraph[s][1])
            neg += int(subgraph[s][2])
            # print("total: ", total, "Post: ", pos, "NEg :", neg)
        return total, pos, neg

    @staticmethod
    def getSupervisedWindowEntropy(subgraph, p_count, n_count):
        '''
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
        # NAME: getWindowEntropy
        #
        # INPUTS: (subgraph) List of subgraph in current window
        #
        # RETURN: (entropy)
        #
        # PURPOSE: Calculate the entropy of current window by using subgraph from current window
        #
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **

        :param subgraph:
        :param p_count:
        :param n_count:
        :return:
        '''

        #print("Subgraph Lists: ", len(subgraph), subgraph)
        total, pos, neg = GraphEntropyMethod.getTotalSubgraphCount(subgraph)
        #print("Total: ", total, pos, neg)
        #print("Graph Count: ", p_count, n_count)
        PyP = 0
        PyN = 0

        #Fraction of Positive Graph in W
        if p_count > 0:
            PyP = p_count / (p_count + n_count)

        #Fraction of Negative Graph in W
        if n_count > 0:
            PyN = n_count / (p_count + n_count)

        PyY = [PyP, PyN]

        eW = 0
        # y = 0
        temp = 0
        for index, Py in enumerate(PyY):
            for s in subgraph.keys():
                #print("Subgraph: " , subgraph[s])
                if index == 0:
                    if subgraph[s][1] > 0:
                        PSiP = subgraph[s][1]/pos
                        #print("PSiP: ", PSiP, subgraph[s][1])
                        temp += PSiP * math.log2(PSiP)
                else:
                    if subgraph[s][2] > 0:
                        PSiN = subgraph[s][2]/neg
                        #print("PSiN: ",PSiN, subgraph[s][2])
                        temp += PSiN * math.log2(PSiN)
            #print("Temp :", temp, " Py :", Py, " eW :", -1 * Py * temp)
            eW += -1 * Py * temp
            temp = 0
            # y += 1
            #print("Entropy  : ", index, eW)
        #print("Entropy of Window: ", eW)
        return eW

    @staticmethod
    def countSubgraph():
        sg_count = {}

        p_count = 0
        n_count = 0
        iso_graph = {}
        for id in GraphEntropyMethod.graphWindow:
            #print("Graphs: ", id, GraphEntropyMethod.graphWindow[id])
            #print(GraphEntropyMethod.graphWindow[id].edges.keys())
            for e in GraphEntropyMethod.graphWindow[id]['edge']:
                v1 = GraphEntropyMethod.graphWindow[id]['node'][e.split(" ")[0]]
                v2 = GraphEntropyMethod.graphWindow[id]['node'][e.split(" ")[1]]
                #print("Edge label: ", GraphEntropyMethod.graphWindow[id]['edge'][e])
                sg = v1+ " " + v2 + " " + GraphEntropyMethod.graphWindow[id]['edge'][e]
                iso_sg = v2+ " " + v1 + " " + GraphEntropyMethod.graphWindow[id]['edge'][e]
                #print("Subgraph: ", sg)

                if sg in sg_count:
                    if GraphEntropyMethod.graphWindow[id]['label'] == 'pos':
                       sg_count[sg] = [sg_count[sg][0]+1, sg_count[sg][1]+1, sg_count[sg][2]]
                    if GraphEntropyMethod.graphWindow[id]['label'] == 'neg':
                       sg_count[sg] = [sg_count[sg][0]+1, sg_count[sg][1], sg_count[sg][2]+1]
                else:
                    if GraphEntropyMethod.graphWindow[id]['label'] == 'pos':
                        sg_count[sg] = [1,1,0]
                    if GraphEntropyMethod.graphWindow[id]['label'] == 'neg':
                        sg_count[sg] = [1,0,1]

                #if not sg in iso_graph:
                #    iso_graph[sg] = iso_sg

            if GraphEntropyMethod.graphWindow[id]['label'] == 'pos':
                p_count += 1
            if GraphEntropyMethod.graphWindow[id]['label'] == 'neg':
                n_count += 1
        #print("Count (p): ", p_count, "Count (n):", n_count)
        return sg_count, p_count, n_count


    @staticmethod
    def shuffule_graphs(g_id, dataset):
        b_key = []
        a_key = []
        for id in g_id:
            if id <= dataset.drift_points[0]:
                b_key.append(id)
            else:
                a_key.append(id)
        shuffle(b_key)
        shuffle(a_key)
        return (b_key + a_key)

    @staticmethod
    def is_real_drift(i, drift_points):
        for j in drift_points:
            if j <= i < GraphEntropy.W:
                return True

    @staticmethod
    def is_not_duplicate(i, drift_points, DRIFT):
        for j in drift_points:
            if j <= i < GraphEntropy.W:
                return True

    @staticmethod
    def graph_entropy_method(g_list, dataset):
        '''
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
        # NAME: graphEntropyMethod()
        #
        # INPUTS: (message, graphCount) JSON Message stream that have graph, count of number of graph
        #
        # RETURN: ()
        #
        # PURPOSE: Implementation of GEM, that give drift point
        #
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **

        :param message:
        :param graphCount:
        :return:
        '''
        #graphFile = graphEntropyMethod.savetoWindowGBADGraphFile(message)
        #print("Graph: ", message) #, "Real Label: ", message['reallabel'])
        DRIFT = []
        WARN = []
        FA = []
        E = [0]
        D = [0]
        C = [0]
        N = [0]
        i = 1
        start = 1
        h = 5
        k = 0.5
        u = 0
        winCount = 1

        key = GraphEntropyMethod.shuffule_graphs(list(g_list.keys()), dataset)

        graphCount = 1
        for g_count in key:
            GraphEntropyMethod.graphWindow[graphCount] = g_list[g_count]
            if len(GraphEntropyMethod.graphWindow) >= GraphEntropy.W:
                GraphEntropyMethod.graphWindow = {k: v for k, v in GraphEntropyMethod.graphWindow.items() if
                                                  k > (graphCount - GraphEntropy.W)}

                S, p_count, n_count = GraphEntropyMethod.countSubgraph()

                e = GraphEntropyMethod.getSupervisedWindowEntropy(S, p_count, n_count)
                #print("Previous Entropy: ", graphEntropyMethod.E[-1])
                #d = e - GraphEntropyMethod.E[-1]
                if i > 1:
                    d = e - E[-1]
                else:
                    d = 0
                E.append(e)
                D.append(d)

                #from start to i
                #print(" D List from Start: ", graphEntropyMethod.D[graphEntropyMethod.start:], graphEntropyMethod.start)
                if len(D[start:]) > 1 :
                    #print(graphEntropyMethod.D[graphEntropyMethod.start:])
                    sd = statistics.stdev(D[start:])
                else:
                    sd = 0
                #u = statistics.mean(graphEntropyMethod.D)

                K = k * sd
                #print(" C: ", GraphEntropyMethod.C)

                #print("Mean: ", graphEntropyMethod.u, " SD: ", sd, " Difference : ", d, " K: ", K)
                c = max(0, d - (u + K) + C[-1])
                #print("Ci : ", c)
                if c > 0:
                    n = N[-1] + 1
                else:
                    n = 0

                H = h * sd
                if c > H:
                    drift = i + GraphEntropy.W
                    warn = drift - n
                    if GraphEntropyMethod.is_real_drift(drift, dataset.drift_points):
                        if GraphEntropyMethod.is_not_duplicate(drift, dataset.drift_points, DRIFT):
                            DRIFT.append(drift)
                            WARN.append(warn)
                    else:
                        FA.append(drift)
                    c = 0
                    n = 0
                    start = i
                    print("Drift Points: ", DRIFT)
                    print("False Alarm: ", FA)
                    #print("Warn Points: ", WARN)

                C.append(c)
                N.append(n)
                #print("Entropy List: ", GraphEntropyMethod.E)
                #print("C List: ", GraphEntropyMethod.C)

                winCount += 1

                GraphEntropyMethod.flag = "w"
                i += 1 #get number of graph in stream
            graphCount += 1
        return DRIFT, FA, E
