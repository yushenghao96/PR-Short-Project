
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pylab as plt
from sklearn.metrics import classification_report

class confusionMatrixException(Exception):
    "Error when creating confusion matrix"
    pass

def generate_evaluation(v_predictedOutput,v_groundingTruth,tuple_languages):

    cm = confusion_matrix(v_predictedOutput, v_groundingTruth)

    fig = plt.figure(figsize=(10, 10))

    sns.heatmap(cm,annot = True,fmt = ".0f")
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    plt.title('KNN pca features classification')
    print(classification_report(v_predictedOutput, v_groundingTruth, target_names=tuple_languages))
    return 0
