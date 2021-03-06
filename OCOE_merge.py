
import os
import pickle
import numpy as np
import pandas as pd
from sklearn import preprocessing
from src.IPC_plot import IPCPLOT

class OCOE(object):
    def __init__(self):
        self.a = None
        self.EventName = ['SW_INCR', 'L1I_CACHE_REFILL', 'L1I_TLB_REFILL', 'L1D_CACHE_REFILL', 'L1D_CACHE',
         'L1D_TLB_REFILL', 'LD_RETIRED', 'ST_RETIRED', 'ST_RETIRED', 'EXC_TAKEN', 'EXC_RETURN', 'CID_WRITE_RETIRED',
         'PC_WRITE_RETIRED', 'BR_IMMED_RETIRED', 'PRD_FN_RET', 'UNALIGNED_LDST_RETIRED',
         'BR_MIS_PRED', 'BR_PRED', 'JAVA_BC_EXEC', 'JAVA_SFTBC_EXEC', 'JAVA_BB_EXEC',
         'CO_LF_MISS', 'CO_LF_HIT', 'IC_DEP_STALL', 'DC_DEP_STALL', 'STALL_MAIN_TLB', 'STREX_PASS',
         'STREX_FAILS', 'DATA_EVICT', 'ISS_NO_DISP', 'ISS_EMPTY', 'NUMBER_OF_DATA_LINEFILLS',
         'NUMBER_OF_PERFETCHER_LINEFILLS', 'NUMBER_OF_HITS_IN_PERFETECHED_CACHE_LINES',
         'INS_MAIN_EXEC', 'INS_SND_EXEC', 'INS_LSU', 'INS_FP_RR', 'INS_NEON_RR', 'STALL_PLD','STALL_WRITE',
         'STALL_INS_TLB', 'STALL_DATA_TLB', 'STALL_INS_UTLB', 'STALL_DATA_ULTB', 'STALL_DMB', 'CLK_INT_EN',
         'CLK_DE_EN', 'NEON_SIMD_CLOCK_ENABLED', 'INSTRUCTION_TLB_ALLOCATION', 'DATA_TLB_ALLOCATION', 'INS_ISB',
         'INS_DSB', 'INS_DMB', 'EXT_IRQ', 'PLE_CL_REQ_CMP','PLE_CL_REQ_SKP', 'PLE_FIFO_FLSH', 'PLE_REQ_COMP',
         'PLE_FIFO_OF', 'PLE_REQ_PRG', 'IPC']

    def get_eventname(self, rootdir=None):
        """ 根据根目录，返回事件名称
        :param rootdir:
        :return:
        """
        if rootdir == None:
            return None
        else:
            event_name = []
            for parent, dirnames, filenames in os.walk(rootdir):
                for filename in filenames:
                    if filename == 'slaver2.xls':
                        filename = os.path.join(parent, filename)
                        df = pd.read_excel(filename)
                        event_name.append(list(df)[3:])
            event_names = []
            for index, val in enumerate(event_name):
                for va in val:
                    event_names.append(va)
            return event_names


    def dir_sorted(self, rootdir=None):
        """ 根据当前目录，对目录下来的文件夹按照 archi_1, archi_2, 3,..., archi_15 的方式重新排列文件夹
        :param rootdir:
        :return: 返回排序好之后的文件夹list
        """
        current_dirs = os.listdir(rootdir)
        dir_index = []
        new_dirs = []
        for index,val in enumerate(current_dirs):
            dir_index.append(int(val.strip().split('_')[1].split('events')[0]))
        dir_index.sort()
        for i in dir_index:
            for index,val in enumerate(current_dirs):
                tmp_index = int(val.strip().split('_')[1].split('events')[0])
                if tmp_index == i:
                    new_dirs.append(val)
        return new_dirs



    def ocoe_mergedata(self, being_merged_data=None):
        df = pd.read_excel(being_merged_data)
        col_names = df.columns[3:]
        df = df.fillna(0)
        ipc = 1.0 * df[df.columns[1]] / df[df.columns[2]]
        df = df[df.columns[[3, 4, 5, 6]]]
        df = pd.DataFrame(preprocessing.scale(df))
        df.columns = col_names
        df['IPC'] = ipc
        return df

    def ocoe_mergedata_noscale(self, being_merged_data=None):
        """ 未对数据做规范化，直接原始数据合并
        :param being_merged_data:
        :return:
        """
        df = pd.read_excel(being_merged_data)
        col_names = df.columns[3:]
        df = df.fillna(0)
        ipc = 1.0 * df[df.columns[1]] / df[df.columns[2]]
        df = df[df.columns[[3, 4, 5, 6]]]
        df.columns = col_names
        df['IPC'] = ipc
        return df


    def fill_random(self, data):
        """ 用随机值填充 NaN
        :param data:
        :return:
        """
        for index, row in data.iterrows():  # 获取每行的index、row
            for col_name in data.columns:
                if row[col_name] == -7:
                    row[col_name] = np.random.random()  # 把结果返回给data
        return data


    def dir_sorted_merge(self, rootdir=None,new_dirs=None, slaver=None):
        """  根据根目录，排序好的文件夹list,以及需要处理的slaver名称进行数据合并
        :param rootdir:
        :param new_dirs:
        :param slaver:
        :return: 返回大 DataFrame 表
        """
        if rootdir == None or new_dirs == None or slaver == None:
            return None
        else:
            df_aa = []
            mean = []
            Min = []
            Max = []
            for index,val in enumerate(new_dirs):
                dirname = os.path.join(rootdir, val)
                for filename in os.listdir(dirname):
                    if filename == slaver:
                        filename = os.path.join(dirname, filename)
                        """ scale by Standardization"""
                        df_tmp = self.ocoe_mergedata(filename)
                        """ No-scale"""
                        #df_tmp = self.ocoe_mergedata_noscale(filename)
                        # mean.append(np.mean(df_tmp['IPC']))
                        # Min.append(min(df_tmp['IPC']))
                        # Max.append(max(df_tmp['IPC']))
                        df_aa.append(df_tmp)
            df = pd.concat(df_aa, ignore_index=True)
            """NaN filled by zero(0) or random value(-7) """
            #df = df.fillna(0)
            df = df.fillna(-7)
            df = self.fill_random(df)
            df = df.ix[:, self.EventName]

            '''打印列名, 行数'''
            #print(df.columns.values.tolist())
            #print([column for column in df])
            print(len(df['IPC']))
            df.to_csv('random_'+str(rootdir.strip().split('/')[-1].split('-')[0])+'.csv')
            #df.to_csv(str(rootdir.strip().split('/')[-1].split('-')[0]) + '_noscale' + '.csv')
            #IPCPLOT.ipc_plot(mean, Min, Max)

            return df


    def ocoe_merge(self):
        slaver = "slaver2.xls"
        rootdir = "../data/LogisticRegression-128MB_xls"
        rootdir = 'F:/linlingfeng/codes/python/perf_DATA/IPC/800ms/PCA-64MB-18slavers-800ms_xls'
        new_dirs = self.dir_sorted(rootdir=rootdir)
        df = self.dir_sorted_merge(rootdir=rootdir, new_dirs=new_dirs, slaver=slaver)
        return df



    def build(self):
        #df = self.ocoe_mergedata()
        df = self.ocoe_merge()
        return self.a

if __name__ == '__main__':
    ocoe = OCOE()
    ocoe.__init__()
    a = None
    a = ocoe.build()