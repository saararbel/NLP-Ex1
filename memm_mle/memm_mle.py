import sys

from memm_mle.liblin import LiblinearLogregPredictor

if __name__ == '__main__':
    input_file_name = sys.argv[1]
    modelname = sys.argv[2]
    out_file_name = sys.argv[3]
    tags_file_name = sys.argv[4]
    llp = LiblinearLogregPredictor(modelname)
    