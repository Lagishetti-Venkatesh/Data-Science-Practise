from sklearn.utils import resample
from matplotlib import pyplot
import numpy as np

#Here df_analysis is the dataframe of the data that your working.
def boostrap_ci(alpha, features, pe, sample_size):
  for i in features:
    x = df_analysis[i]
    a_string ="In " + str(i)+': '
    bolded_string = "\033[1m" + a_string + "\033[0m"
    print(bolded_string)
    # configure bootstrap
    n_iterations = 1000
    n_size = sample_size 
    # run bootstrap for median statistic . you can replace with the statistic you want. 
    stc = [] #stc is the statistic like mean or median or mode or standard deviation
    if(pe == 'median'):
      for i in range(n_iterations):
          # prepare train and test sets
          s = resample(x, n_samples= sample_size);# sample_size is the size of each boostrap sample
          m = np.median(s);
          #print(m)
          stc.append(m)
    if(pe == 'mean'):
      for i in range(n_iterations):
          # prepare train and test sets
          s = resample(x, n_samples= sample_size);# sample_size is the size of each boostrap sample
          m = np.mean(s);
          #print(m)
          stc.append(m)
    if(pe == 'std'):
      for i in range(n_iterations):
          # prepare train and test sets
          s = resample(x, n_samples= sample_size);# sample_size is the size of each boostrap sample
          m = np.std(s);
          #print(m)
          stc.append(m)
    if(pe == 'average'):
      for i in range(n_iterations):
          # prepare train and test sets
          s = resample(x, n_samples= sample_size);# sample_size is the size of each boostrap sample
          m = np.average(s);
          #print(m)
          stc.append(m)



    # plot scores
    pyplot.hist(stc)
    pyplot.show()

    # confidence intervals
    alpha = 0.95
    p = ((1.0-alpha)/2.0) * 100
    lower =  np.percentile(stc, p)

    p = (alpha+((1.0-alpha)/2.0)) * 100
    upper =  np.percentile(stc, p)
    
    print('for '+str(alpha*100) +" " + pe +' confidence interval is in range '+str(lower)+" "+str(upper))
    print('\n\n')

# SET THE PARAMETERES FOR ABOVE BOOSTRAP FUNCTION.
 
# for the statistic meadian
alpha = 0.95
features= list(df.columns[:-1])
#removing the text column
features.remove('review_by_patient')
print(features)

sample_size = 500
#list of point estimators
pe = ['mean', 'median', 'std']
for i in pe:
  print(i,": ")
  boostrap_ci(alpha, features, i, sample_size)
  print('='*150)
  
  
