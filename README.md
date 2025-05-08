# Info
    This simple package provides an easy evaluation for the [User Experience Questionnaire](https://www.ueq-online.org/) for comparsion of products. It computes statistical comparison tests and formats the results nicely in a Latex Table. Please still refer the official Excel sheet for data investigation, but this might just save some time and effort in copying the necessary numbers.

# Usage Example
```py
    import pandas as pd

    # Data Reading
    data = pd.read_csv("mydata/data.csv", sep="\t", header=0)
    
    # Compute Output and Write to Data
    computeUEQScores(data, ["UEQ_01","UEQ_02","UEQ_03","UEQ_04","UEQ_05","UEQ_06","UEQ_07","UEQ_08","UEQ_09","UEQ_10","UEQ_11","UEQ_12","UEQ_13","UEQ_14","UEQ_15","UEQ_16","UEQ_17","UEQ_18","UEQ_19","UEQ_20","UEQ_21","UEQ_22","UEQ_23","UEQ_24","UEQ_25","UEQ_26"])
    
    # Print as Latex Compatible Table
    printArrowCommandDefinitions()
    printLatexUEQComparison(data.query("Condition == 'A'"), data.query("Condition == 'B'"), paired=True, data1Label="A", data2Label="B")
```
