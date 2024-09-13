

merged = rt_df.merge(mojo_df, left_on = 'movie_title', right_on = 'Release Group', how = 'inner')
merged[['movie_title', 'Release Group', 'Worldwide', 'Domestic', 'tomatometer', 'audience_score', 'weighted_score']]
merged = merged[merged['Domestic'].notnull()]
merged = merged[merged['Domestic'] < 2*10**8]

import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Define the function for regression and plotting
def regress_and_plot(df, x_var, y_var):
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(df[x_var], df[y_var])

    correlation = df[x_var].corr(df[y_var])
    
    # Display regression statistics
    print(f'Regression statistics:')
    print(f'Intercept: {intercept:.4f}')
    print(f'Slope: {slope:.4f}')
    print(f'R-squared: {r_value**2:.4f}')
    print(f'Correlation (Pearson\'s r): {correlation:.4f}')
    print(f'P-value: {p_value:.4f}')
    print(f'Standard error: {std_err:.4f}')

    # Plotting the scatter plot with regression line
    plt.figure(figsize=(8, 6))
    sns.regplot(x=x_var, y=y_var, data=df, ci=None, scatter_kws={'color':'blue'}, line_kws={'color':'red'})
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title(f'Scatter Plot with Regression Line: {y_var} vs {x_var}')

    # Annotate the correlation coefficient on the plot
    plt.text(0.05, 0.95, f'Correlation (r): {correlation:.4f}', transform=plt.gca().transAxes,
             fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    plt.grid(True)
    plt.show()

regress_and_plot(merged, 'audience_score', 'Domestic')
regress_and_plot(merged, 'tomatometer', 'Domestic')
regress_and_plot(merged, 'weighted_score', 'Domestic')