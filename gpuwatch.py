import subprocess as sub

descriptors = list()

def getString():
    test_file = "nvidia-smi -q --gpu=0"
 
    try:
        p = sub.Popen(test_file, stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = p.communicate()
        return out
 
    except IOError:
        return "Error"

def readl(key):
    output=str(getString(), encoding='utf8')
    splittedoutput=output.split('\n')
    for line in splittedoutput:
        line=line.strip()
        if line.startswith(key):
            line=line.split(':')[1].strip()
            if key=='GPU Current Temp':
                return line.split('C')[0].strip()
            elif key=='Fan Speed':
                return line.split('%')[0].strip()
            else:
                return line[:-1]
    

def Gpu_Temp():
    return int(readl('GPU Current Temp'))

def Fan_Speed():
    return int(readl('Fan Speed'))

def Gpu_Util():
    return int(readl('GPU'))

def Mem_Util():
    return int(readl('Memory'))

def metric_init(params):
    global descriptors
    
    d1 = {'name': 'Gpu_Temperature',
        'call_back': Gpu_Temp,
        'time_max': 90,
        'value_type': 'uint',
        'units': 'C',
        'slope': 'both',
        'format': '%u',
        'description': 'GPU Temperature',
        'groups': 'gpu'}

    d2 = {'name': 'Fan_Speed',
        'call_back': Fan_Speed,
        'time_max': 90,
        'value_type': 'uint',
        'units': '%',
        'slope': 'both',
        'format': '%u',
        'description': 'Fan Speed',
        'groups': 'gpu'}

    d3 = {'name': 'Gpu_Utilization',
        'call_back': Gpu_Util,
        'time_max': 90,
        'value_type': 'uint',
        'units': '%',
        'slope': 'both',
        'format': '%u',
        'description': 'GPU GPU Utilization',
        'groups': 'gpu'}

    d4 = {'name': 'Memory_Utilization',
        'call_back': Mem_Util,
        'time_max': 90,
        'value_type': 'uint',
        'units': '%',
        'slope': 'both',
        'format': '%u',
        'description': 'GPU Memory Utilization',
        'groups': 'gpu'}

    descriptors = [d1,d2,d3,d4]
    return descriptors

def metric_cleanup():
    '''Clean up the metric module.'''
    pass

#Testing    
if __name__ == '__main__':
    metric_init({})
    for d in descriptors:
        v = d['call_back']('')
        print('value for {} is {}'.format(d['name'],  v))