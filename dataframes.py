## import libraries
import csv
import numpy as np
import pandas as pd
from urllib.request import urlopen

## Create country_list
country_list = []

with open('data/countries.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        country_list.append(row[0])

## Read data from csv files
df_expeditions = pd.read_csv('data/expeditions.csv')
df_peaks = pd.read_csv('data/peaks.csv')
df_members = pd.read_csv('data/members.csv')
df_citizenship_geodata = pd.read_csv('data/citizenship_geodata.csv')

## Filling missing peak name in index 2546.
df_expeditions['peak_name'][2546:2547].fillna("Sharphu I", inplace=True)

## Replacing all peak ids of expeditions having the peak name SPHU with SPH1 as it is an error noticed from looking at the peaks dataframe
df_expeditions['peak_id'] = df_expeditions['peak_id'].replace(['SPHU'], 'SPH1')

## Replace the expendition_id of expeditions with the same error as above
df_expeditions['expendition_id'] = df_expeditions['expedition_id'].replace(['SPHU63301'], 'SPH163301')

## Dropping the "basecamp_date", "highpoint_date", and "termination_date" columns as they have a lot of NaNs
df_expeditions = df_expeditions.drop(columns=["basecamp_date", "highpoint_date", "termination_date"])

## Filling missing trekking agency data. We're assuming they are independent trekkers and as such didn't use an agency
df_expeditions['trekking_agency'].fillna("Independent Trekkers", inplace=True)

## Drop rows with NaNs in the "highpoint_metres" column
df_expeditions = df_expeditions.dropna(subset=["highpoint_metres"])

## Repeat the replacement of all member_ids, peak_ids and expendition_ids with SPHU in them with SPH1
df_members['member_id'] = df_members['member_id'].str.replace('SPHU63301', 'SPH163301')
df_members['peak_id'] = df_members['peak_id'].replace(['SPHU'], 'SPH1')
df_members['expendition_id'] = df_members['expedition_id'].replace(['SPHU63301'], 'SPH163301')

## Fill missing peak names within the specified indexes with the new name.
df_members['peak_name'][21183:23692].fillna("Sharphu I", inplace=True)

## Drop NaN rows for sex and age columns.
df_members = df_members.dropna(subset=["sex", "age"])

## Create a dataframe for death cause
death_cause = ~df_members['death_cause'].isna()
df_members_death_cause = df_members[death_cause]
df_members_death_cause.reset_index(drop=True, inplace=True)

## Drop "injury_type", "injury_height_metres" columns as they have a lot of unusuable NaN values
df_members_death_cause = df_members_death_cause.drop(columns=["injury_type", "injury_height_metres"])

## Drop NaNs in the death cause data frame
df_members_death_cause = df_members_death_cause.dropna(subset=["death_height_metres"])
df_members_death_cause = df_members_death_cause.dropna(subset=["highpoint_metres"])

## Drop "death_cause", "death_height_metres", "injury_type", "injury_height_metres" columns after creating the death cause df
df_members = df_members.drop(columns=["death_cause", "death_height_metres", "injury_type", "injury_height_metres"])

## Remove NaNs from "highpoint_metres" column
df_members = df_members.dropna(subset=["expedition_role", "highpoint_metres"])

## Replace citizenship data with 'W Germany' to Germany and 'Kyrgyz Republic' to "Kyrgyzstan"
df_members['citizenship'] = df_members['citizenship'].str.replace('W Germany', 'Germany')
df_members['citizenship'] = df_members['citizenship'].str.replace('Kyrgyz Republic', 'Kyrgyzstan')

## Create a dataframe of member with dual citizenship
with_dual_citizenship_filter = df_members['citizenship'].str.contains('\w{1,}/')
df_members_dual_citizenship = df_members.loc[with_dual_citizenship_filter, :]
df_members_dual_citizenship.reset_index(drop=True, inplace=True)

## Create a dataframe of member without dual citizenship
wo_dual_citizenship_filter = ~df_members['citizenship'].str.contains('\w{1,}/')
df_members_wo_dual_citizenship = df_members.loc[wo_dual_citizenship_filter, :]
df_members_wo_dual_citizenship.reset_index(drop=True, inplace=True)

## Remove countries that no longer exist from the dataframe of members without dual citizenship and the members
df_members_wo_dual_citizenship = df_members_wo_dual_citizenship[df_members_wo_dual_citizenship['citizenship'].isin(country_list)]

## Add longitude and latitude infomation for citizenship countries for mapping.
df_members_wo_dual_citizenship = pd.merge(df_members_wo_dual_citizenship, df_citizenship_geodata, how='left', on=["citizenship"])
df_members_wo_dual_citizenship = df_members_wo_dual_citizenship.dropna(subset=["latitude", "longitude"])

## Add a column to indicate whether a member of an expedition in the members data frame
df_members['has_dual_citizenship'] = np.where(df_members['citizenship'].str.contains('\w{1,}/'), True, False)