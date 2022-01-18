import pandas as pd
import pyarrow 
hdfs_config = {
     "host" :"localshost",
     "port" : 9870,
     "user" : "user"
}
fs=pyarrow.HadoopFileSystem.connect(hdfs_config['host'], hdfs_config['port'], 
user=hdfs_config['user'])
df=pd.read_csv(fs.open("Files/input/file.csv"))
