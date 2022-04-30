#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function, division
import time

from matplotlib import rcParams
import matplotlib.pyplot as plt

from nilmtk import DataSet, TimeFrame, MeterGroup, HDFDataStore
from grudisaggregator import GRUDisaggregator
import metrics


# In[2]:


print("========== OPEN DATASETS ============")
train = DataSet('/home/houpc16/dataset/ukdale_2.h5')
test = DataSet('/home/houpc16/dataset/ukdale_2.h5')

train.set_window(start="13-4-2013", end="1-1-2014")
test.set_window(start="1-1-2014", end="30-3-2014")


# In[3]:


train_building = 1
test_building = 1
sample_period = 60
meter_key = 'kettle'
train_elec = train.buildings[train_building].elec
test_elec = test.buildings[test_building].elec


# In[4]:


train_meter = train_elec.submeters()[meter_key]
train_mains = train_elec.mains()
test_mains = test_elec.mains()
disaggregator = GRUDisaggregator()


# In[5]:


start = time.time()
print("========== TRAIN ============")
epochs = 0
for i in range(5):
    print("CHECKPOINT {}".format(epochs))
    disaggregator.train(train_mains, train_meter, epochs=1, sample_period=sample_period)
    epochs += 1
    disaggregator.export_model("/home/houpc16/GRU/UKDALE-GRU-h{}-{}-{}epochs.h5".format(train_building,
                                                        meter_key,
                                                        epochs))
end = time.time()
print("Train =", end-start, "seconds.")


# In[6]:


print("========== DISAGGREGATE ============")
disag_filename = "/home/houpc16/GRU/disag_ukdale_kettle.h5"
output = HDFDataStore(disag_filename, 'w')
disaggregator.disaggregate(test_mains, output, train_meter, sample_period=sample_period)
output.close()


# In[7]:


result = DataSet(disag_filename)
res_elec = result.buildings[1].elec
predicted = res_elec[meter_key]
ground_truth = test_elec[meter_key]

import matplotlib.pyplot as plt
predicted.plot()
ground_truth.plot()
plt.savefig('/home/houpc16/djangoenv/nilmProject/static/analyze/GRU_ukdale_kettle.png', dpi=100)
plt.show()


# In[8]:


print("========== RESULTS ============")
result = DataSet(disag_filename)
res_elec = result.buildings[test_building].elec
rpaf = metrics.recall_precision_accuracy_f1(res_elec[meter_key], test_elec[meter_key])
print("============ Recall: {}".format(rpaf[0]))
print("============ Precision: {}".format(rpaf[1]))
print("============ Accuracy: {}".format(rpaf[2]))
print("============ F1 Score: {}".format(rpaf[2]))

print("============ Relative error in total energy: {}".format(metrics.relative_error_total_energy(res_elec[meter_key], test_elec[meter_key])))
print("============ Mean absolute error(in Watts): {}".format(metrics.mean_absolute_error(res_elec[meter_key], test_elec[meter_key])))


# In[ ]:




