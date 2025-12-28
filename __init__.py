from scipy import stats
import numpy as np
import statistics

UEQ_Questions = {
    "Attractiveness" : [1,12,14,16,24,25],
    "Perspicuity" : [2,4,13,21],
    "Efficiency" : [9,20,22,23],
    "Dependability" : [8,11,17,19],
    "Stimulation" : [5,6,7,18],
    "Novelty" : [3,10,15,26]
}

# Function below from https://machinelearningmastery.com/effect-size-measures-in-python/
def cohend(d1, d2):
	# calculate the size of samples
	n1, n2 = len(d1), len(d2)
	# calculate the variance of the samples
	s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
	# calculate the pooled standard deviation
	s = statistics.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
	# calculate the means of the samples
	u1, u2 = np.mean(d1), np.mean(d2)
	# calculate the effect size
	return (u1 - u2) / s

def printPValue(pValue, printZero=True):
	if(pValue < 0.001): return "< 0.001" if printZero else "< .001"
	if(pValue < 0.01): return "< 0.01" if printZero else "< .01"
	if(pValue < 0.05): return "< 0.05" if printZero else "< .05"
	return f"{pValue:.3f}" if printZero else f"{pValue:.3f}".lstrip('0')

def computeUEQScores(data, columnNames):
    Inverted = [1,1,-1,-1,-1,1,1,1,-1,-1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,-1,-1,-1,1]

    data[columnNames] -= 4
    data[columnNames] *= Inverted

    for key in UEQ_Questions:
       data[key] = data[[columnNames[i-1] for i in UEQ_Questions[key]]].mean(axis=1)

def getArrowColor(value):
    if(value > 0.8): return "\\arrowGreen"
    if(value > -0.8): return "\\arrowYellow"
    return "\\arrowRed"

def printArrowCommandDefinitions():
    print("\\usetikzlibrary{shapes.arrows}")
    print("\\definecolor{ArrowGreenOuter}{HTML}{3b6758}")
    print("\\definecolor{ArrowGreenInner}{HTML}{69a790}")
    print("\\definecolor{ArrowRedInner}{HTML}{d85738}")
    print("\\definecolor{ArrowRedOuter}{HTML}{93371e}")
    print("\\definecolor{ArrowYellowInner}{HTML}{edc484}")
    print("\\definecolor{ArrowYellowOuter}{HTML}{987637}")
    print("\\newcommand{\\colorArrow}[3]{\\tikz{\\node[single arrow, draw=#1, fill=#2, minimum width=10pt, single arrow head extend=3pt, minimum height=5mm, scale=0.4, rotate=#3] {};}\\hspace{10mm}}")
    print("\\newcommand{\\arrowRed}[0]{\\colorArrow{ArrowRedOuter}{ArrowRedInner}{-90}}")
    print("\\newcommand{\\arrowYellow}[0]{\\colorArrow{ArrowYellowOuter}{ArrowYellowInner}{0}}")
    print("\\newcommand{\\arrowGreen}[0]{\\colorArrow{ArrowGreenOuter}{ArrowGreenInner}{90}}")

def printLatexUEQComparison(data1, data2, paired=False, data1Label="Data1", data2Label="Data2"):
    output  = "\\begin{table}"
    output += "\n\t\\footnotesize"
    output += "\n\t\\centering"
    output += "\n\t\\begin{tabular}{c|p{0.1cm}c|c|p{0.1cm}c|c|r|r|r|}"
    output += "\n\t\t\\cline{2-10}"
    output += f"\n\t\t& \\multicolumn{{3}}{{c|}}{{{data1Label}\\rule{{0pt}}{{3mm}}}} & \\multicolumn{{3}}{{c|}}{{{data2Label}}} & \\multicolumn{{3}}{{c|}}{{Significance}} \\\\ "
    output += "\n\t\t& \\multicolumn{2}{c|}{Mean} & SD & \\multicolumn{2}{c|}{Mean} & SD & Test stat. & p-value & Cohen's d\\\\" 
    output += "\n\t\t\\cline{1-10}"
    
    for key in UEQ_Questions:
        d1 = data1[key].dropna()
        d2 = data2[key].dropna()

        stat1, pVal1 = stats.shapiro(d1)
        stat2, pVal2 = stats.shapiro(d2)
        
        cd = cohend(d1, d2)

        if paired:
            if(pVal1 < 0.05 or pVal2 < 0.05):
                res = stats.wilcoxon(d1,d2)
                testStat = f"$W={res.statistic:.2f}$ & ${printPValue(res.pvalue, printZero=False)}$"
            else:
                res = stats.ttest_rel(d1,d2)
                testStat = f"$t_{{rel}}({res.df})={res.statistic:.2f}$ & ${printPValue(res.pvalue, printZero=False)}$"
        else:
            stat3, pVal3 = stats.levene(d1,d2)
            if(pVal1 > 0.05 and pVal2 > 0.05 and pVal3 > 0.05):
                res = stats.ttest_ind(d1,d2, equal_var=True)
                testStat = f"$t_{{ind}}({res.df})={res.statistic:.2f}$ & ${printPValue(res.pvalue, printZero=False)}$"
            elif(pVal1 > 0.05 and pVal2 > 0.05):
                res = stats.ttest_ind(d1,d2, equal_var=False)
                testStat = f"$t_{{w}}({res.df:.2f})={res.statistic:.2f}$ & ${printPValue(res.pvalue, printZero=False)}$"
            else:
                res = stats.mannwhitneyu(d1,d2)
                testStat = f"$U={res.statistic:.2f}$ & ${printPValue(res.pvalue, printZero=False)}$"

        output += f"\n\t\t\t\\multicolumn{{1}}{{|c|}}{{{key}\\rule{{0pt}}{{3mm}}}} & {getArrowColor(data1[key].mean())} & {data1[key].mean():.2f} & {data1[key].std():.2f} & {getArrowColor(data2[key].mean())} &	{data2[key].mean():.2f}	& {data2[key].std():.2f} & {testStat} & ${"\\phantom{{-}}" if cd > 0 else ""}{cd:.2f}$\\\\"
    
    output += "\n\t\t\\cline{1-10}"
    output += "\n\t\\end{tabular}"
    if paired:
        output += "\n\t\\caption{Single scales of the User Experience Questionnaire \\cite{laugwitz2008}, where each value is within [-3,3] and marked with a green ($ \\ge0.8$), red ($\\le -0.8$) or yellow arrow for all values in between as done in the evaluation sheet of the questionnaire. In the right-most column, tests for significant differences between both conditions are depicted. Depending on normality (Shapiro-Wilk) a t-test ($t$) or a Wilcoxen ($W$) signed rank test was computed. Additionally, the effect sizes as defined by Cohen are shown.}"
    else:
        output += "\n\t\\caption{Single scales of the User Experience Questionnaire \\cite{laugwitz2008}, where each value is within [-3,3] and marked with a green ($ \\ge0.8$), red ($\\le -0.8$) or yellow arrow for all values in between as done in the evaluation sheet of the questionnaire. In the right-most column, tests for significant differences between both conditions are depicted. Depending on normality (Shapiro-Wilk) and equal variances (Levene), a t-test ($t$), a Welch test ($t_w$) or a Mann-Whitney-U-test ($U$) was computed. Additionally, the effect sizes as defined by Cohen are shown.}"

    output += "\n\t\\label{}"
    output += "\n\\end{table}"
    print(output)

def printLatexUEQTable(data):
    output  = "\\begin{table}"
    output += "\n\t\\footnotesize"
    output += "\n\t\\centering"
    output += "\n\t\\begin{tabular}{c|p{0.1cm}c|c|}"
    output += "\n\t\t\\cline{2-4}"
    output += "\n\t\t& \\multicolumn{2}{c|}{Mean} & SD\\\\"
    output += "\n\t\t\\cline{1-4}"
    for key in UEQ_Questions:
        output += f"\n\t\t\t\\multicolumn{{1}}{{|c|}}{{{key}\\rule{{0pt}}{{3mm}}}} & {getArrowColor(data[key].mean())} & {data[key].mean():.2f} & {data[key].std():.2f} \\\\"
    output += "\n\t\t\\cline{1-4}"
    output += "\n\t\\end{tabular}"
    output += "\n\t\\caption{Single scales of the User Experience Questionnaire \\cite{laugwitz2008}, where each value is within [-3,3] and marked with a green ($ \\ge0.8$), red ($\\le -0.8$) or yellow arrow for all values in between as done in the evaluation sheet of the questionnaire. }"
    output += "\n\t\\label{}"
    output += "\n\\end{table}"
    print(output)