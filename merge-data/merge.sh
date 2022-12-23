rm -r output/
python merge.py --dataset defacto --filepath data/df_flattened_2022-12-22_1.csv 
python merge.py --dataset science --filepath data/sf_flattened_2022-12-22_1.csv --merged-table output/misinformation_2022-12-22_1.csv 
python merge.py --dataset condor --filepath data/condor_cleaned_2022-12-22_1.csv --merged-table output/misinformation_2022-12-22_2.csv 
rm output/misinformation_2022-12-22_1.csv  output/misinformation_2022-12-22_2.csv 
mv output/misinformation_2022-12-22_3.csv output/misinformation_2022-12-22.csv