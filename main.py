import os
import json
import numpy as np
import matplotlib.pyplot as plt

from utils import draw_plot
from load import load_model
from query import read_queries

from exact import exact_inference
from prior import prior_sample
from rejection import rejection_sample
from likelihood import likelihood_sample
from gibbs import gibbs_sample

IN_PATH = ".\Data"
OUT_PATH = ".\Out"

# Main
cpts, graph, V = load_model(IN_PATH + "\model.txt")
queries, evidences = read_queries(IN_PATH + "\queries.txt")

prior_ae_vals = []
rejection_ae_vals = []
likelihood_ae_vals = []
gibbs_ae_vals = []

print("\n")

for i in range(len(queries)):
    exact_val = exact_inference(queries[i], evidences[i], cpts, graph)
    prior = prior_sample(queries[i], evidences[i], cpts, graph, V)
    rejection = rejection_sample(queries[i], evidences[i], cpts, graph, V)
    likelihood = likelihood_sample(queries[i], evidences[i], cpts, graph, V)
    gibbs = gibbs_sample(queries[i], evidences[i], cpts, graph, V)

    print(f"Query {i+1}:")
    print(f"exact_val: {exact_val}")
    print(f"prior: {prior}")
    print(f"rejection: {rejection}")
    print(f"likelihood: {likelihood}")
    print(f"gibbs: {gibbs}\n")

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

print("prior average error: ", round(prior_ae_avg, 5))
print("rejection average error: ", round(rejection_ae_avg, 5))
print("likelihood average error: ", round(likelihood_ae_avg, 5))
print("gibbs average error: ", round(gibbs_ae_avg, 5), "\n")

draw_plot(prior_ae_vals, rejection_ae_vals, likelihood_ae_vals, gibbs_ae_vals, "Chart")