from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import ExactInference
from Bayesian_V1 import parameter_generation
from pgmpy.inference import VariableElimination
from Bayesian_V1 import define_variables as df
from Bayesian_V1 import define_CNF as df_CNF
from Bayesian_V1 import enc1_simplified_def_variables as df_simplify
from Bayesian_V1 import en1_simplified_def_CNF as df_CNF_simplify
from Bayesian_V1 import  write_cnf as writefile
from Bayesian_V1 import enc1_simplified_2 as enc1_sim2

from pgmpy.readwrite import BIFReader
# read a file?
reader = BIFReader('/Users/tianyangsun/Documents/Project/Github_repo/bifs/asia.bif')
earthquake_model = reader.get_model()


debug = False
# represent a simple bayesian network and store it as simple_example
# if A -> B, do ['A', 'B']
nodes = ['A', 'B', 'C'] # store the nodes in a list
simple_example = BayesianModel()
simple_example.add_nodes_from(nodes)

simple_example = BayesianModel([('A', 'B'),
                                ('B', 'C'),
                                ('A', 'C')])

# define individual
cpd_A = TabularCPD(variable = 'A', variable_card = 2, values = [[0.1, 0.9]])
# define the ones with evidence
# as explained in the pgmpy library, this matrix is transformed actually
cpd_B = TabularCPD(variable = 'B', variable_card = 2,
                   values = [[0.1, 0.2],
                             [0.9, 0.8]],
                   evidence = ['A'],
                   evidence_card = [2])

cpd_C = TabularCPD(variable = 'C', variable_card = 3,
                   values = [[0.1, 0.01, 0.05 , 0.5],
                             [0.2, 0.09, 0.5, 0],
                             [0.7, 0.9, 0.45, 0.5]],
                   evidence = ['A', 'B'],
                   evidence_card =[2, 2])

# associate the tables with the networks
simple_example.add_cpds(cpd_A, cpd_B, cpd_C)





cancer_model = BayesianModel([('Pollution', 'Cancer'),
                              ('Smoker', 'Cancer'),
                              ('Cancer', 'Xray'),
                              ('Cancer', 'Dyspnoea')])
cpd_poll = TabularCPD(variable='Pollution', variable_card=2,
                      values=[[0.9], [0.1]])
cpd_smoke = TabularCPD(variable='Smoker', variable_card=2,
                       values=[[0.3], [0.7]])
cpd_cancer = TabularCPD(variable='Cancer', variable_card=2,
                        values=[[0.03, 0.05, 0.001, 0.02],
                                [0.97, 0.95, 0.999, 0.98]],
                        evidence=['Smoker', 'Pollution'],
                        evidence_card=[2, 2])
cpd_xray = TabularCPD(variable='Xray', variable_card=2,
                      values=[[0.9, 0.2], [0.1, 0.8]],
                      evidence=['Cancer'], evidence_card=[2])
cpd_dysp = TabularCPD(variable='Dyspnoea', variable_card=2,
                      values=[[0.65, 0.3], [0.35, 0.7]],
                      evidence=['Cancer'], evidence_card=[2])
cancer_model.add_cpds(cpd_poll, cpd_smoke, cpd_cancer, cpd_xray, cpd_dysp)

#print (simple_example.check_model())
# check the models
def encode(bn):

    df.generate_variable(bn)
    df_CNF.enc1_indicator_clauses(bn)
    df_CNF.enc1_parameter_clauses()
    df_CNF.write_indicator_clause()

    writefile.write_no_weight(df_CNF.write_file)

    if (debug):
        print("These are parameter variables")
        print(df.parameter_variable_n)
        print(df.parameter_variable_v)
        print("parameter to value")
        print(df.parameter_to_value)

        print("These are indicator variables")
        print(df.indicator_variable_n)
        print(df.indicator_variable_v)



def enc1_simplified(bn):
    df_simplify.generate_variable(bn)
    df_CNF_simplify.enc1_indicator_clauses(bn)
    df_CNF_simplify.enc1_parameter_clauses()
    df_CNF_simplify.write_indicator_clause()

    writefile.enc1_write_no_weight_simplified(df_CNF_simplify.write_file)



def enc1_simplified_2(bn):
    enc1_sim2.generate_vars(bn)
    print(enc1_sim2.variable_dictionary)
    print(len(enc1_sim2.variable_dictionary))
    print(enc1_sim2.parameter_weights)
    print("encoding1 improved")

#encode(simple_example)
#enc1_simplified(earthquake_model)
enc1_simplified_2(earthquake_model)
#enc1_indicator_clauses()

# print the nodes in a Bayesian network
#print(simple_example.nodes)

# get a node's evidence
#print(simple_example.get_cpds('A').get_evidence())

# get a parameter value
#infer = VariableElimination(simple_example)

#result = infer.query(['B'], evidence={'A':1})['B']
#result = infer.query(['C'], evidence = {'A':1, 'B':0})['C']
#print(result.values[0])
#print(result)
