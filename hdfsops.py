import subprocess
from hdfs.ext.kerberos import KerberosClient
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import hdfs3
from hdfs3 import HDFileSystem
hdfs_client = KerberosClient('http://localhost:9870') 
#hdfs = pa.hdfs.connect('localhost', port=54310)

def readcsv():
	try:
		with hdfs_client.read('/test/files/trees.csv') as reader: 
			df = pd.read_csv(reader, sep = ';', error_bad_lines = False)
			print(df)
		print("-------------------------------------------------------------")
	except Exception as e:
		print(e)

def readtext():
	try:
		cat = subprocess.Popen(["hadoop", "fs", "-cat", "/test/files/a.txt"], stdout=subprocess.PIPE)
		for line in cat.stdout:
	    		print (line)
		print("-------------------------------------------")
	except Exception as e:
		print(e)

def readavro():
	try:
		cat = subprocess.Popen(["hadoop", "fs", "-text", "/test/files/data.avro"], stdout=subprocess.PIPE)
		for line in cat.stdout:
	    		print (line)
		print("-------------------------------------------")
	except Exception as e:
		print(e)
'''
def readparq():
	try:

		with hdfs.open('/test/files/data.parquet', 'rb') as f: 
			 df = pq.read_table(reader, filesystem = hdfs)
   			 print(df)
		print("-------------------------------------------")
	except Exception as e:
		print(e)
'''
readcsv()
readtext()
#readavro()
#readparq()

 #read a directory of parquet filesdataset = pq.ParquetDataset('path/to/directory', filesystem = hdfs) table = dataset.read() df = table.to_pandas()
'''

with hdfs.open('/test/files/data.parquet', 'rb') as f: 
			dataset = pq.read_table(f, filesystem = hdfs)
			table = dataset.read() 
			df = table.to_pandas()
			print(df)
		print("-------------------------------------------")
				
import pyarrow as pa
import hdfs3
import pandas as pd
from hdfs3 import HDFileSystem

hdfs = hdfs3.HDFileSystem('localhost', port=54310, user='hadoop',driver='libhdfs3')
#hdfs = HDFileSystem('localhost', 54310, 'hadoop')
with hdfs.open('/test/files/trees.csv', 'rb') as reader:
     df = pd.read_csv(reader, sep = ';', error_bad_lines = False)
     print(df)


import pyarrow as pa
import pyarrow.parquet as pq
hdfs = pa.hdfs.connect('localhost', port=54310)
with hdfs.open('/test/files/data.parquet', 'rb') as f:
    df = pq.read_table(f, filesystem=hdfs)
    print(df)
    '''
    
'''
import gc
import random
import time
import pyarrow as pa
import hdfs3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATA_SIZE = 200 * (1 << 20)
data = 'a' * DATA_SIZE

hdfs = pa.HdfsClient('localhost', 20500, 'wesm')
hdfscpp = pa.HdfsClient('localhost', 20500, 'wesm', driver='libhdfs3')
hdfs3_fs = hdfs3.HDFileSystem('localhost', port=20500, user='wesm')

hdfs.delete(path)
path = '/tmp/test-data-file-1'
with hdfs.open(path, 'wb') as f:
    f.write(data)

def read_chunk(f, size):
    # do a random seek
    f.seek(random.randint(0, size))
    return f.read(size)

def ensemble_average(runner, niter=10):
    start = time.clock()
    gc.disable()
    data_chunks = []
    for i in range(niter):
        data_chunks.append(runner())
    elapsed = (time.clock() - start) / niter
    gc.enable()
    return elapsed

def make_test_func(fh, chunksize):
    def runner():
        return read_chunk(fh, chunksize)
    return runner

KB = 1024
MB = 1024 * KB
chunksizes = [4 * KB, MB, 10 * MB, 100 * MB]
iterations = [100, 100, 100, 10]

handles = {
    ('pyarrow', 'libhdfs'): hdfs.open(path),
    ('pyarrow', 'libhdfs3'): hdfscpp.open(path),
    ('hdfs3', 'libhdfs3'): hdfs3_fs.open(path, 'rb')
}

timings = []
for (library, driver), handle in handles.items():
    for chunksize, niter in zip(chunksizes, iterations):
        tester = make_test_func(handle, chunksize)
        timing = ensemble_average(tester, niter=niter)
        throughput = chunksize / timing

        result = (library, driver, chunksize, timing, throughput)
        print(result)
        timings.append(result)

results = pd.DataFrame.from_records(timings, columns=['library', 'driver', 'read_size', 'timing', 'throughput'])
results['MB/s'] = results['throughput'] / MB
results
results['type'] = results['library'] + '+' + results['driver']

plt.figure(figsize=(12, 6))
g = sns.factorplot(y='read_size', x='MB/s', hue='type', data=results, kind='bar', orient='h', size=(10))
g.despine(left=True)
#g.fig.get_axes()[0].set_xscale('log', basex=2)
g.fig.set_size_inches(12, 4)

plt.savefig('results2.png')
'''
