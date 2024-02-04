import os
import json
import numpy as np
import matplotlib.pyplot as plt
import utils

IN_PATH = ".\Data"
OUT_PATH = ".\Out"

# Main
cpts, graph, V = load_model(IN_PATH + "\model.txt")
queries, evidences = read_queries(IN_PATH + "\queries.txt")

prior_ae_vals = []
rejection_ae_vals = []
likelihood_ae_vals = []
gibbs_ae_vals = []

for i in range(len(queries)):
    exact_val = exact_inference(queries[i], evidences[i], cpts, graph)
    prior = prior_sample(queries[i], evidences[i], cpts, graph, V)
    rejection = rejection_sample(queries[i], evidences[i], cpts, graph, V)
    likelihood = likelihood_sample(queries[i], evidences[i], cpts, graph, V)
    gibbs = gibbs_sample(queries[i], evidences[i], cpts, graph, V)

    print(f"exact_val: {exact_val}\tprior: {prior}\trejection: {rejection}\tlikelihood: {likelihood}\tgibbs: {gibbs}\n")

    # Add the desirable AE(Average Error) to the corresponding list for each method
    prior_ae_vals.append(abs(exact_val - prior))
    rejection_ae_vals.append(abs(exact_val - rejection))
    likelihood_ae_vals.append(abs(exact_val - likelihood))
    gibbs_ae_vals.append(abs(exact_val - gibbs))

# Illustrate the AE of each method with the draw_plot function and save the result in OUT_PATH directory
prior_ae_avg = sum(prior_ae_vals) / len(prior_ae_vals)
rejection_ae_avg = sum(rejection_ae_vals) / len(rejection_ae_vals)
likelihood_ae_avg = sum(likelihood_ae_vals) / len(likelihood_ae_vals)
gibbs_ae_avg = sum(gibbs_ae_vals) / len(gibbs_ae_vals)

print("prior average error: ", prior_ae_avg)
print("rejection average error: ", rejection_ae_avg)
print("likelihood average error: ", likelihood_ae_avg)
print("gibbs average error: ", gibbs_ae_avg)

draw_plot(prior_ae_vals, rejection_ae_vals, likelihood_ae_vals, gibbs_ae_vals, "Chart")