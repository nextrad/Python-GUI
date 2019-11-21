import numpy as np
import matplotlib.pyplot as plt
import configparser

#def phase_filer():
config = configparser.ConfigParser()
config.read('snip-config.ini')
next_config = configparser.ConfigParser()
next_config.read('NeXtRAD.ini')

data_file = config.get('Config','data_file')
update_rate = config.get('Config','update_rate')
outfile = config.get('Config','outfile')

num_pulses = next_config.get('PulseParameters','NUM_PRIS')
num_range_bins = next_config.get('PulseParameters','SAMPLES_PER_PRI')
pri = float(next_config.get('PulseParameters','PULSES').split(',')[1])
print(pri)

    # for i in range()
    #     data = np.fromfile(data_file, dtype=np.int16, count=2*num_pulses*num_range_bins)

# IQ = data[0::2] + 1j*data[1::2]       #Create complex IQ samples
# IQ_ref = ref_data[0::2] + 1j*ref_data[1::2] #Complex reference and trim away noise samples
# ref = np.pad(IQ_ref,(0, num_range_bins-len(IQ_ref)),'constant')

# pulse_matrix = np.reshape(IQ,(num_pulses,num_range_bins)) # Form a num_pulses x num_range_bin matrix

# temp_matrix = np.zeros((num_pulses,2*num_range_bins-1),dtype=complex)

# for pulse in range(num_pulses):
#     temp_matrix[pulse,:] = np.correlate(pulse_matrix[pulse,:], ref, mode='full')
#     pulse_matrix[pulse,:] = temp_matrix[pulse,num_range_bins-1::]
# if __name__ == '__main__':
#     pri = phase_filer
#     print(pri)