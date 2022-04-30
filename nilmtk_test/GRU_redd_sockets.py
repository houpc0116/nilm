#!/usr/bin/env python
# coding: utf-8

# # How to use the RNN Autoencoder with NILMTK
# 
# This is an example on how to train and use the Recurrent Network (RNN) disaggregator on the [REDD](http://redd.csail.mit.edu/) dataset using [NILMTK](https://github.com/nilmtk/NILMTK/).
# 
# This network was described in the [Neural NILM](https://arxiv.org/pdf/1507.06594.pdf) paper.

# First of all, we need to train the RNNDisaggregator using the train data. For this example, both train and test data are consumption data of the microwave of the first REDD building.

# In[1]:


buildings=1
appliance='sockets'


# In[2]:


import warnings; warnings.simplefilter('ignore')

from nilmtk import DataSet
train = DataSet('/home/houpc16/dataset/redd.h5')
train.set_window(end="30-4-2011") #Use data only until 4/30/2011
train_elec = train.buildings[1].elec


# Next, we need to define the disaggregator model.

# In[3]:


from grudisaggregator import GRUDisaggregator
gru = GRUDisaggregator()


# Then train the model. We need to input the train data as well as their sample period. Also, we need to pass the desired number of training epochs. Finally, save the model for later use.

# In[4]:


train_mains = train_elec.mains() # The aggregated meter that provides the input
train_meter = train_elec.submeters()[appliance] # The microwave meter that is used as a training target

gru.train(train_mains, train_meter, epochs=10, sample_period=1)
gru.export_model("/home/houpc16/GRU/model-redd.h5")


# Now that the model is trained, we can use it to disaggregate energy data. Let's test it on the rest of the data from building 1.
# 
# First we use the model to predict the microwave consumption. The results are saved automatically in a .h5 datastore.

# In[5]:


test = DataSet('/home/houpc16/dataset/redd.h5')
test.set_window(start="01-05-2011")
test.set_window(end="20-05-2011")
test_elec = test.buildings[1].elec
test_mains = test_elec.mains().all_meters()[1]

disag_filename = '/home/houpc16/GRU/disag_redd_sockets.h5' # The filename of the resulting datastore
from nilmtk.datastore import HDFDataStore
output = HDFDataStore(disag_filename, 'w')

# test_mains: The aggregated signal meter
# output: The output datastore
# train_meter: This is used in order to copy the metadata of the train meter into the datastore
gru.disaggregate(test_mains, output, train_meter, sample_period=60)
output.close()

# Let's plot the results and compare them to the ground truth signal.
# 
# **Note:** Calling plot this way, downsamples the signal to reduce computing time. To plot the entire signal call
# ```
# predicted.power_series_all_data().plot()
# ground_truth.power_series_all_data().plot()
# ```

# In[6]:


import matplotlib.pyplot as plt


# In[7]:


result = DataSet(disag_filename)
res_elec = result.buildings[buildings].elec


# In[8]:


meter = res_elec[appliance].load(sample_period=60)
meter_df = next(meter)
mains = res_elec.mains().load(sample_period=60) #訓練的aggre
mains_df = next(mains)
gf=test_elec[appliance].load(sample_period=60)
gf_df=next(gf)


# In[9]:


zz=train_elec.mains().load(sample_period=60)
zz=next(zz)


# In[10]:


plt.figure(figsize=(20,10))
plt.plot(zz)
plt.show()


# In[11]:


pre=meter_df[18900:]
xx=mains_df[18900:]
yy=gf_df[18900:]


# In[12]:


import pandas as pd
merge1=pd.merge(pre,xx, how='inner', left_index=True, right_index=True) #結合再一起根據時間。(因為聚合資料比較多)
merge2=pd.merge(merge1,yy, how='inner', left_index=True, right_index=True) #結合再一起根據時間。(因為聚合資料比較多)


# In[13]:


plt.figure(figsize=(20,10))
plt.plot(merge2[('power_x', 'apparent')]['2011-05-11 04:58:00-04:00':'2011-05-13 05:16:00-04:00']) #pre
plt.plot(merge2[('power_y', 'apparent')]['2011-05-11 04:58:00-04:00':'2011-05-13 05:16:00-04:00']) #aggre
plt.plot(merge2[('power', 'active')]['2011-05-11 04:58:00-04:00':'2011-05-13 05:16:00-04:00'])     #gt
plt.figure()


# In[14]:


import numpy as np
aggre=np.array(merge2[('power_y', 'apparent')]['2011-05-11 04:58:00-04:00':'2011-05-13 05:16:00-04:00'])
target=np.array(merge2[('power', 'active')]['2011-05-11 04:58:00-04:00':'2011-05-13 05:16:00-04:00'])
pred=np.array(merge2[('power_x', 'apparent')]['2011-05-11 04:58:00-04:00':'2011-05-13 05:16:00-04:00'])


# In[15]:


zz=aggre
yy=target
decoded=pred
total_aggre=2*np.sum(zz) #根據REDD的計算
appliance_error=np.sum(abs(yy-decoded))
print(1-(appliance_error/total_aggre)) #計算準確率


# In[16]:


#計算mae
error=abs(decoded-yy)
sumerror=np.sum(error)
temp=1/len(error)
mm=sumerror*temp #mae
mm


# In[17]:


rmse=np.sqrt(np.mean((decoded-yy)**2))
rmse


# Finally let's see the metric results.

# In[18]:


result = DataSet(disag_filename)
res_elec = result.buildings[1].elec
predicted = res_elec[appliance]
ground_truth = test_elec[appliance]

import matplotlib.pyplot as plt
predicted.plot()
ground_truth.plot()
plt.savefig('/home/houpc16/djangoenv/nilmProject/static/analyze/GRU_redd_sockets.png', dpi=100)
plt.show()


# In[19]:


import metrics
rpaf = metrics.recall_precision_accuracy_f1(predicted, ground_truth)
print("============ Recall: {}".format(rpaf[0]))
print("============ Precision: {}".format(rpaf[1]))
print("============ Accuracy: {}".format(rpaf[2]))
print("============ F1 Score: {}".format(rpaf[3]))

print("============ Relative error in total energy: {}".format(metrics.relative_error_total_energy(predicted, ground_truth)))
print("============ Mean absolute error(in Watts): {}".format(metrics.mean_absolute_error(predicted, ground_truth)))


# In[ ]:




