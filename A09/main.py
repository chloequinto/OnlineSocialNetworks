import pandas as pd 

def main():
    fb_data = pd.read_csv("FB_data.csv")
    print(fb_data.head())
    print("---")
    print(fb_data.columns)



if __name__ == "__main__":
    main()