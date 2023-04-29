import matplotlib.pyplot as plt
import json
import pandas as pd

data = json.load(open("hist.json"))

def data_clean(keyword):
    d = data[keyword]
    out = [[] for i in range(len(d[0]))]

    for i in range(len(d[0])):
        for j in range(len(d)):
            out[i].append(d[j][i])
    return out




def plotter(keyword):
    while True:
        try:
            cleaned_data = data_clean(keyword)
            break
        except:
            print("Invalid input")
            continue
    for i in range(len(cleaned_data)):
        plt.plot(data["turns"], cleaned_data[i], label=f"player {i}")
        plt.xlabel("turns")
        plt.ylabel(keyword)

    plt.legend()
    plt.show()

def main():
    while True:
        print("1. Health")
        print("2. Attack")
        print("3. Defense")
        print("4. Luck")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            plotter("health")
        elif choice == "2":
            plotter("attack")
        elif choice == "3":
            plotter("defense")
        elif choice == "4":
            plotter("luck")
        elif choice == "5":
            break
        else:
            print("Invalid input")

if __name__ == '__main__':
    main()