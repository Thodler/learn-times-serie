def execute(feature):
    from statsmodels.tsa.stattools import adfuller
    
    # Test ADF
    result = adfuller(feature)
    print("Statistique ADF :", result[0])
    print("p-value :", result[1])

    # Interprétation
    if result[1] < 0.05:
        print("La série est stationnaire (p-value < 0.05).")
    else:
        print("La série n'est pas stationnaire (p-value >= 0.05).")