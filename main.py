from graph.dataset import Dataset
from simulation.stream_generator import StreamGenerator
from results.measure_performance import MeasurePerformance
from properties import Experiment, DataList
from GEM.graph_entropy_method import GraphEntropyMethod

def main():
    sg = StreamGenerator()
    results = {}
    ds = Dataset()

    #prepare datasets
    available_dataset = ds.get_available_dataset()
    for dataset in available_dataset:
        print("\n\n*******----- Experimenting on [ %s ] Dataset Starts-------****"%(dataset.dataset_name))

        for i in range(1, Experiment.iterations+1):

            print("\n\n----- Iteration [ ", i," ] -------\n\n")
            g_list = sg.create_graph_stream(i, dataset)
            print("Total Graph: ", len(g_list))

            DRIFT, FA, E = GraphEntropyMethod.graph_entropy_method(g_list, dataset)

            #dd = DriftDetector()
            #PE, E, DRIFT, FA = dd.drift_detector(g_list, dataset)

            #print("\n\n PE Score: ", PE)
            print("\n\n Entropy: ", E)

            print("\n\n******---- Graph Stream [ ", i ," ] Ends ----****\n\n")

            mp = MeasurePerformance()
            results[i] = mp.calculate_metrics(DRIFT, FA, dataset)
            mp.print_results(results[i], DRIFT, FA)
        #summary = mp.aggregate_result(results)
        #mp.print_sumary(summary)



main()
