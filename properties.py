class RabbitConnection:
    hostName = "127.0.0.1"
    queueName = "graph_stream"
    routingKey = "graph_stream"
    heartbeat = 0

class SubGen:
    s1PosSample = "subgenGEM/pos"
    s1NegSample = "subgenGEM/neg"
    s2PosSample = "subgenGEM/s2pos"
    s2NegSample = "subgenGEM/s2neg"
    subgenCommand = "subgenGEM/subgen"

class GBAD:
    gbadFolder ="/Users/rameshpaudel/Documents/gbad-tool-kit_3.3/gbad-mdl_3.3"
    graphFolder = "/Users/rameshpaudel/Documents/ClassMaterial/Research/GraphStream/DriftDetection/gbad/win"
    XPFolder = "/Users/rameshpaudel/Documents/ClassMaterial/Research/GraphStream/DriftDetection/gbad/xp"
    subgraph = "subgraph.g"
    graphFile = "G.g"
    posGraph = "pos_G.g"
    negGraph = "neg_G.g"
    minsize = 3
    maxsize = 10
    nsubs = 40
    gbadCommand = "bin/gbad "+ " -minsize "+ str(minsize) +" -maxsize " + str(maxsize) + " -nsubs "+ str(nsubs)
    algorithm = "mdl"

class SubDue:
    SubDueFolder ="subdue"
    graphFolder = "subdue/graphs"
    subgraph = "subgraph.g"
    graphFile = "G.g"
    minsize = 2
    maxsize = 15
    nsubs = 40
    beam = 4
    subdueCommand = "bin/subdue "+ " -minsize "+ str(minsize) +" -maxsize " + str(maxsize) + " -beam " + str(beam) +" -nsubs "+ str(nsubs)
    #subdueCommand = "bin/subdue "  + " -nsubs " + str(nsubs)


class Experiment:
    iterations = 1
    param_syn_n = [10, 15, 20]
    param_syn_w = [50, 150, 300]
    param_syn = [param_syn_n, param_syn_w]

    param_real_n = [10]
    param_real_w = [200]
    param_real = [param_real_n, param_real_w]

class DataList:
    # datasetname = (<dataset name>, <total graph>, <expected drift points>, <graph file name>, <isSyntetic (True or False)> , <param>(parameter array))
    SD1 = ('SD1', 2000, [1000], 'dataset/SD1.g', False, Experiment.param_syn)
    SD2 = ('SD2', 6000, [1001, 2001, 3001, 4001, 5001], 'dataset/SD2.g', False, Experiment.param_syn)
    DBLP = ('DBLP', 2000, [1000], 'dataset/DBLP.g', False, Experiment.param_real)
    AIDS = ('AIDS', 2000, [1600], 'dataset/aids.g', False, Experiment.param_real)

    #make a list of all datasets
    data_list = [DBLP]

class GraphEntropy:
    W = 300
