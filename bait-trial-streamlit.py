# preliminary report for kakapo bait trial October 2023

import streamlit as st
import pandas as pd
import glob
#import os
from matplotlib import pyplot as plt
import plotly.express as px

st.title("Kākāpō bait trial preliminary findings")

### prep ###

### get data ###
#path = "dat/"
#all_files = glob.glob(os.path.join(path, "kakapo*.csv"))
all_files = glob.glob(os.path.join("kakapo*.csv"))

kdata = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# remove rows with KakapoID==NA
kdata = kdata[kdata['KakapoID'].notna()]

# RMS no. of interactions
no_interRMS = kdata['InteractionRMS'].isna().sum()
all_interRMS = kdata['InteractionRMS'].notna().sum()

# 20R no. of interactions
no_inter20R = kdata['Interaction20R'].isna().sum()
all_inter20R = kdata['Interaction20R'].notna().sum()

st.subheader("Number of birds and bait stations")
st.image("WH_bait_stations.png", caption="Whenua Hou map of bait stations")

st.write("Number of individual birds in trial: ", kdata['KakapoID'].nunique())
st.write("Number of bait stations in trial: ", kdata['RelativePath'].nunique())

st.subheader("Number of interactions by:")
st.markdown("- study design - Close and Away")
st.markdown("bait type - cereal (20R) and ready-made meat-based sausage (RMS)")

ABS = kdata[kdata['RelativePath'].str.contains("ABS")]
CBS = kdata[kdata['RelativePath'].str.contains("CBS")]

table_dict = {
    "Bait Type":['20R', 'RMS'],
    "Close": [CBS['Interaction20R'].notna().sum(), CBS['InteractionRMS'].notna().sum()],
    "Away": [ABS['Interaction20R'].notna().sum(), ABS['InteractionRMS'].notna().sum()],
    "Total": [all_inter20R, all_interRMS],
}

table = pd.DataFrame(data=table_dict)
st.write(table)
st.markdown(table.style.hide(axis="index"))

rms = pd.crosstab(kdata.KakapoID, kdata.InteractionRMS).rename_axis(None, axis=1)
r20 = pd.crosstab(kdata.KakapoID, kdata.Interaction20R).rename_axis(None, axis=1)

rms.drop('Touch accidental', axis=1, inplace=True)
r20.drop('Touch accidental', axis=1, inplace=True)

stacked_rms = rms.apply(lambda x: x*100/sum(x), axis=1)
stacked_20r = r20.apply(lambda x: x*100/sum(x), axis=1)

st.subheader("Proportion of interaction types per bird")

fig = px.bar(stacked_20r, x=stacked_20r.index,
                y=['Bite', 'Consumption', 'Encounter', 'Look', 'Touch'], 
                color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(
    xaxis_title="Kakapo Name", yaxis_title="Proportion of interactions",
    legend_title="Interaction type",
    title={
        'text': "20R proportion of interactions for each kakapo",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
)

#fig.show()
st.plotly_chart(fig)

fig = px.bar(stacked_rms, x=stacked_rms.index,
                y=['Bite', 'Encounter', 'Look', 'Touch'], 
                title="RMS proportion of interactions for each kakapo",
                color_discrete_sequence=px.colors.qualitative.Vivid)

fig.update_layout(
    xaxis_title="Kakapo Name", yaxis_title="Proportion of interactions",
    legend_title="Interaction type",
        title={
        'text': "RMS proportion of interactions for each kakapo",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
)

st.plotly_chart(fig)

st.subheader("Trial setup images")
st.caption("Bait station setup examples")
st.image(["GetImage(5).jpeg", "GetImage(3).jpeg"])  # width

st.caption(" Bait weathering cages")
st.image(["GetImage(7).jpeg", "GetImage(7).jpeg"])

st.caption("Example: RMS left intact, 20R fully consumed")
st.image(["GetImage.jpeg", "GetImage(1).jpeg"])
