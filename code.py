# ref: https://www.kaggle.com/code/subinium/awesome-visualization-with-titanic-dataset

#!/usr/bin/env python3

import os
import sys
import yaml
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# The function

def gender(source: str) -> str:
    try:
        if source == "EDA":
            data = pd.read_csv(f"train.csv")

        sns.barplot(x="Sex", y="Survived", data=data)
        plt.savefig(f"/data/gender_{source}.png")
        plt.close("all")
        return "Figure saved to \"/data/gender{source}.png\""
    except IOError as e:
        return f"ERROR: {e} ({e.errno})"

def pclass(source: str) -> str:
    try:
        data = pd.read_csv(f"train.csv")

        sns.color_palette(sns.color_palette("PuBu", 2))

        fig = plt.figure(figsize=(12, 8))
        gs = fig.add_gridspec(3, 1)
        gs.update(hspace=-0.55)

        axes = list()
        colors = ["#022133", "#5c693b", "#51371c"]

        for idx, cls, c in zip(range(3), sorted(data['Pclass'].unique()), colors):
            axes.append(fig.add_subplot(gs[idx, 0]))

            # you can also draw density plot with matplotlib + scipy.
            sns.kdeplot(x='Age', data=data[data['Pclass'] == cls],
                        fill=True, ax=axes[idx], cut=0, bw_method=0.25,
                        lw=1.4, edgecolor='lightgray', hue='Survived',
                        multiple="stack", palette='PuBu', alpha=0.7
                        )

            axes[idx].set_ylim(0, 0.04)
            axes[idx].set_xlim(0, 85)

            axes[idx].set_yticks([])
            if idx != 2: axes[idx].set_xticks([])
            axes[idx].set_ylabel('')
            axes[idx].set_xlabel('')

            spines = ["top", "right", "left", "bottom"]
            for s in spines:
                axes[idx].spines[s].set_visible(False)

            axes[idx].patch.set_alpha(0)
            axes[idx].text(-0.2, 0, f'Pclass {cls}', fontweight="light", fontfamily='serif', fontsize=11, ha="right")
            if idx != 1: axes[idx].get_legend().remove()

        fig.text(0.13, 0.81, "Surivial distribution by Pclass in Titanic", fontweight="bold", fontfamily='serif',
                 fontsize=16)

        plt.show()
        
        plt.savefig(f"/data/pclass_{source}.png")
        plt.close()
        return "Successful! Figure saved to \"/data/pclass{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"

def Ticket(source: str) -> str:
    try:
        data = pd.read_csv(f"train.csv")

        data['Ticket'].value_counts()

        Ticket_Count = dict(data['Ticket'].value_counts())
        data['Ticket_Class'] = data['Ticket'].apply(lambda x: Ticket_Count[x])
        sns.barplot(x='Ticket_Class', y='Survived', data=data)
        plt.savefig(f"/data/Ticket_{source}.png")
        plt.close()
        return "Successful! Figure saved to \"/data/Ticket{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"

def Title(source: str) -> str:
    try:
        data = pd.read_csv(f"train.csv")

        # Name processing
        # Title Feature(New)
        data['Title'] = data['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())
        data['Title'].replace(['Mr'], 'Mr', inplace=True)
        data['Title'].replace(['Mlle', 'Miss'], 'Miss', inplace=True)
        data['Title'].replace(['Mme', 'Ms', 'Mrs'], 'Mrs', inplace=True)
        data['Title'].replace(['Capt', 'Col', 'Major', 'Dr', 'Rev'], 'Officer', inplace=True)
        data['Title'].replace(['Don', 'Sir', 'the Countess', 'Dona', 'Lady'], 'Royalty', inplace=True)
        data['Title'].replace(['Master', 'Jonkheer'], 'Master', inplace=True)

        sns.barplot(x="Title", y="Survived", data=data)

        plt.savefig(f"/data/Title_{source}.png")
        plt.close()
        return "Successful! Figure saved to \"/data/Title{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"

def Correlation(source: str) -> str:
    try:
        data = pd.read_csv(f"train.csv")

        data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
        data['Embarked'] = data['Embarked'].fillna('S')
        data['Embarked'] = data['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
        data['Family'] = data['SibSp'] + data['Parch']
        data = data[[col for col in data.columns if col != 'Survived'] + ['Survived']]
        corr = data.corr()

        sns.color_palette(sns.diverging_palette(230, 20))

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))

        mask = np.zeros_like(corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        sns.heatmap(corr,
                    square=True,
                    mask=mask,
                    linewidth=2.5,
                    vmax=0.4, vmin=-0.4,
                    cmap=cmap,
                    cbar=False,
                    ax=ax)

        ax.set_yticklabels(ax.get_xticklabels(), fontfamily='serif', rotation=0, fontsize=11)
        ax.set_xticklabels(ax.get_xticklabels(), fontfamily='serif', rotation=90, fontsize=11)

        ax.spines['top'].set_visible(True)

        plt.tight_layout()
        plt.show()

        plt.savefig(f"/data/Correlation_{source}.png")
        plt.close()

        return "Successful! Figure saved to \"/data/Correlation{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"



# The entrypoint of the script
if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "gender":
        print(yaml.dump({ "contents": gender(os.environ["SOURCE"]) }))
    elif command == "pclass":
        print(yaml.dump({ "contents": pclass(os.environ["SOURCE"]) }))
    elif command == "Ticket":
        print(yaml.dump({ "contents": Ticket(os.environ["SOURCE"]) }))
    elif command == "Title":
        print(yaml.dump({ "contents": Title(os.environ["SOURCE"]) }))
    elif command == "Correlation":
        print(yaml.dump({ "contents": Correlation(os.environ["SOURCE"]) }))
    # Done!
