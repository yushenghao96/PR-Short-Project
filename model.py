import seaborn as sns
import numpy as np
import pandas as pd
import os
import csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn import decomposition
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

languages = [
    'Spanish',
    'English',
    'German',
    'French'
]

file_directory = os.getcwd()
extractedFeatures_folder = 'ExtractedFeatures/'

df_full = pd.DataFrame()
for language in languages:
    df_language = pd.read_csv(file_directory + '/' + extractedFeatures_folder + '/' + language + '.csv', delimiter=";", encoding='utf-8')
    df_language['Class'] = language
    df_full = pd.concat([df_full, df_language], ignore_index=True)
    df_full = df_full.reindex(range(df_full.shape[0]))


print(df_full.head())
y = df_full['Class'] # class labels

color_map = {
    "Spanish": "blue",
    "English": "green",
    "German": "red",
    "French": "purple"
}

#Mapping languages into colors for representation
colors = [color_map[label] for label in y]



df_dropped = df_full.drop(['phrase','Class'], axis=1) #Drop non-numeric columns


X = df_dropped.values  # Extracting numpy array from pandas dataframe

print(X.shape)  # Print the shape of the array


XS = StandardScaler().fit_transform(X)
pca = decomposition.PCA(n_components=25).fit(XS)
print('Explained variance = {} {} {} {}'.format(*pca.explained_variance_ratio_))
print(100*pca.explained_variance_ratio_.cumsum())

Xproj = pca.transform(XS) #project data to PCA space
Xreduced = Xproj[:,0:10] #keep first PC components
print(Xreduced)

kmeans_labels = KMeans(n_clusters=4).fit_predict(Xproj[:,0:3]) 


dfpca_3d = pd.DataFrame(Xproj[:, 0:3], columns=['PCA1', 'PCA2', 'PCA3'])

# Initialize a 3D figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for label, color in color_map.items():
    ax.scatter(dfpca_3d.loc[y == label, 'PCA1'], 
               dfpca_3d.loc[y == label, 'PCA2'], 
               dfpca_3d.loc[y == label, 'PCA3'], 
               c=color, label=label)

# Set labels and title
ax.set_xlabel('PCA1')
ax.set_ylabel('PCA2')
ax.set_zlabel('PCA3')
ax.set_title('3D PCA')

# Add legend
ax.legend()

plt.show()


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(Xproj[:, 0], Xproj[:, 1], Xproj[:, 2], c=kmeans_labels)  # Plotting in 3D
ax.set_title("k-means clustering (k=4) in 3D")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()