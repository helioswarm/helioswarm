#!/usr/bin/env python3

import glob

import numpy
import spacepy.pycdf


cdfs = [spacepy.pycdf.CDF(f) for f in sorted(glob.glob("./hsconcept_l2-summary_20*.cdf"))]
data = spacepy.pycdf.concatCDF(cdfs)
# vb = spacepy.pycdf.istp.VarBundle(data, 'Position')
# vb.slice(1, 0, single=True).toSpaceData().plot()
# vb.slice(1, 5, single=True).toSpaceData().plot()
del cdfs
dates = numpy.vectorize(lambda x: f"{x.day:2d}" + x.strftime(" %b %Y %H:%M:%S.%f")[:-3])(
    data["Epoch"]
)
r = numpy.sqrt((data["Position"] ** 2).sum(axis=-1))
sc = 0
with open("comparison.txt", "wt") as f:
    f.write(
        """                                                                                                                                16 Jul 2024 14:55:08
Satellite-Chief


       Time (UTCG)              x (km)            y (km)            z (km)       Magnitude (km)    True_Anomaly (deg)    Total_Mass_Flow_Rate (g/hr)
------------------------    --------------    --------------    -------------    --------------    ------------------    ---------------------------\n"""
    )
    for i in range(len(data["Epoch"])):
        f.write(
            f"{dates[i]}"
            f"{data['Position'][i, sc, 0]:18.6f}"
            f"{data['Position'][i, sc, 1]:18.6f}"
            f"{data['Position'][i, sc, 2]:17.6f}"
            f"{r[i, sc]:18.6f}"
            f"{data['True_Anomaly'][i, sc]:22.3f}"
            "                    0.000000000\n"
        )
