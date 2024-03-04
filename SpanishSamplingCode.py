import pandas as pd 

#Load the Dataset 
df = pd.read_csv("Your_CSV_Here.csv")

#Initialize receiving lists and get subject list and entries per subject
random_titles = []
subject_list = df.Subject.unique()
random_subjects = []
value_counts = df['Subject'].value_counts()

#For each subject, if less than 20 entries, extract all. Else, extract 20 random entries
for x in range(len(subject_list)):
    if value_counts.get(subject_list[x], 0) < 21:
        random_titles.extend(df[df['Subject'] == subject_list[x]]['Title'].tolist())
        random_subjects.extend(df[df['Subject'] == subject_list[x]]['Subject'].tolist())
    else:
        random_titles.extend(df[df['Subject'] == subject_list[x]]['Title'].sample(n=20, replace = False))
        random_subjects.extend(df[df['Subject'] == subject_list[x]]['Subject'].sample(n=20, replace = False))

#Create the dataframe
Sampled_Set = pd.DataFrame({"Subject":random_subjects, "Title":random_titles})

#Send to csv
Sampled_Set.to_csv("SampledSpanishLibrary.csv")