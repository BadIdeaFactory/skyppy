import json
import pandas as pd
import itertools

def segmentation_to_json(segmentation):
    data = pd.DataFrame(segmentation)
    data = data.round(2)
    output = data.values.tolist()
    return output

def segmentation_to_dict(segmentation):
    output = {}
    data = pd.DataFrame(segmentation)
    unique = data[0].unique()
    data = data.round(2) 
    for status in unique:
        output[status] = data[data[0] == status][[1,2]].values.tolist()
    return output
def segmentation_to_list_array(segmentation):
    output = {}
    output_v2 = {}
    data = pd.DataFrame(segmentation)
    unique = data[0].unique()
    data = data.round(2) 
    for status in unique:
        output[status] = data[data[0] == status][[1,2]].values.tolist()
        
    for status in unique:
        output_v2[status] = list(itertools.chain(*output[status]))
    return output_v2
# unit test

# unit testS

test = eval("[('noEnergy', 0.0, 0.36), ('music', 0.36, 12.66), ('male', 12.66, 100.86), ('noEnergy', 100.86, 102.28), ('male', 102.28, 184.70000000000002), ('music', 184.70000000000002, 208.70000000000002), ('noEnergy', 208.70000000000002, 209.08)]"
)

if __name__ == "__main__":
    #print(segmentation_to_list(test))
    #print(json.dumps(segmentation_to_list(test)))
    print(segmentation_to_list_array(test))
    print(segmentation_to_json(test))
