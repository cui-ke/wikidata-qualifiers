import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Lecture du fichier CSV
x = []
y = []
with open('rank-freq.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        # print(f'{row}')
        x.append(float(row[0]))
        y.append(float(row[1]))

# Création du scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, s=4)
plt.xlabel('Rank')
plt.ylabel('Frequency')
# plt.title('Rank - Frequency')
plt.yscale('log') 

# Sauvegarde du graphique en PDF
with PdfPages('graphique.pdf') as pdf:
    pdf.savefig()
    plt.close()
