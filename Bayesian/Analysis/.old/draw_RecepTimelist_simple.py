#!/usr/bin/env python
# Authors:
#   Wenhan TANG - 06/2021
#   ...

import numpy as np
import pandas as pd
import datetime as dtm
import matplotlib.pyplot as plt
from Bench import BenchPlots, multicases_subplot_scheme
from REAL_Analyst import REAL_Analyst_Independent as Analyst
from pdb import set_trace

def draw_RecepTimelist(case, OutDir = "."):
    Receptors = case.ObsName_list
    timelist, Hx_orig = case.get_Hx(receptors_list = Receptors, HxType = "orig")
    _, Hx_pos = case.get_Hx(receptors_list = Receptors, HxType = "pos")
    _, Hx_final = case.get_Hx(receptors_list = Receptors, HxType = "final")
    _, obs = case.get_OBS(receptors_list = Receptors)
    _, bck_orig = case.get_BCK(receptors_list = Receptors, BCKType = "orig")
    _, bck_opt = case.get_BCK(receptors_list = Receptors, BCKType = "optimized")
    timelist_emiss, site_prior, prior_variance = case.get_SiteLoc_emiss(EmissType = "Prior", get_variance = True)
    _, site_posterior, posterior_variance = case.get_SiteLoc_emiss(EmissType = "Posterior", get_variance = True)

    #set_trace()
    bcp = BenchPlots(save_name = OutDir + "/Bench_BTH_d02_v5")
    vrange1 = (350, 600)
    #vrange2 = (-100, 250)
    vrange2 = (-10, 50)
    vrange3 = (350, 550)

    ax = bcp.subplot(1,1,1)
    for receptor in Receptors:
        ax.plot(timelist, obs[receptor], label = receptor)
    ax.set_ylim(vrange1)
    ax.grid()
    ax.legend()
    bcp.cfig.suptitle("Observation")
    bcp.next_page()
    
    for receptor in Receptors:
        axs = bcp.subplots(4,1,{"sharex": True})
        bcp.cfig.subplots_adjust(hspace = 0.1)
        #ax = bcp.subplot(4,1,1)
        ax = axs[0]
        ax.plot(timelist, obs[receptor], color = "red", marker = "o", label = "OBS")
        ax.plot(timelist, Hx_orig[receptor] + bck_orig[receptor], color = "black", label = "Prior")
        #ax.plot(timelist, Hx_pos[receptor] + bck_opt[receptor], color = "green", label = "Post_primary")
        ax.plot(timelist, Hx_final[receptor] + bck_opt[receptor], color = "blue", label = "Posterior")
        ax.set_ylim(vrange1)
        ax.grid(color = "grey", linestyle = "--", linewidth = 0.2)
        ax.legend()
        ax.set_ylabel("ppm")
        #ax = bcp.subplot(4,1,2)
        ax = axs[1]
        ax.plot(timelist, Hx_orig[receptor], label = "Hx_orig", color = "black")
        #ax.plot(timelist, Hx_pos[receptor], label = "Hx_pos")
        ax.plot(timelist, Hx_final[receptor], label = "Hx_pos", color = "blue")
        ax.plot(timelist, np.full((len(timelist)), 0), color = "black", linestyle = "--")
        ax.set_ylim(vrange2)
        ax.grid(color = "grey", linestyle = "--", linewidth = 0.2)
        ax.legend()
        ax.set_ylabel("ppm")
        #ax = bcp.subplot(4,1,3)
        ax = axs[2]
        #ax.plot(timelist, bck_orig[receptor], label = "BCK_orig")
        ax.plot(timelist, bck_opt[receptor], label = "BCK_optimized")
        ax.set_ylim(vrange3)
        ax.grid(color = "grey", linestyle = "--", linewidth = 0.2)
        ax.legend()
        ax.set_ylabel("ppm")
        #ax = bcp.subplot(4,1,4)
        ax = axs[3]
        ax.plot(timelist_emiss, site_prior[receptor], label = "prior emiss", color = "black")
        upper_line = site_prior[receptor] + prior_variance[receptor] ** 0.5
        lower_line = site_prior[receptor] - prior_variance[receptor] ** 0.5
        ax.fill_between(timelist_emiss, lower_line, upper_line, facecolor = "grey", alpha = 0.3)

        ax.plot(timelist_emiss, site_posterior[receptor], label = "posterior emiss", color = "blue")
        upper_line = site_posterior[receptor] + posterior_variance[receptor] ** 0.5
        lower_line = site_posterior[receptor] - posterior_variance[receptor] ** 0.5
        ax.fill_between(timelist_emiss, lower_line, upper_line, facecolor = "blue", alpha = 0.3)
        #print(receptor, ": prior_variance = ", prior_variance[receptor], "; posterior_variance = ", posterior_variance[receptor])
        #print(receptor, ": reduced = ", prior_variance[receptor]**0.5 - posterior_variance[receptor]**0.5)#, "; posterior_variance = ", posterior_variance[receptor])
        ax.grid(color = "grey", linestyle = "--", linewidth = 0.2)
        ax.legend()
        ax.set_ylabel("umol/m^2/s")
        bcp.cfig.autofmt_xdate()
        bcp.cfig.suptitle(receptor)
        bcp.next_page()
       
    bcp.close()

if __name__ == "__main__":
    case = Analyst(CaseName = "BTH_d02_test5", window = 24)
    draw_RecepTimelist(case)

    
