nlp2017 ass1 submit
======

Submitting:
------
* Boaz Berman, 311504401
* Saar Arbel, 315681775

HMM task 1:
------
For handling unknown words we created a special tag representing an unknown word.
For it to not actually be in the text we used an highly unlikeable word:
> very_very_rare_word_5_5_5

In order to allow a probability for an unknown word (since all probabilities must sum to 1) we replaced all the words
that appeared only once in the text with the unknown word.
Now if we came across an unknown word we handled it like it was our representation of an unknown word.

HMM task 2:
------
For pruning the tags our strategy was to take the last two tags (represented as t and t' in the presentation) from the
tags available in the viterbi of the last step. This pruning was enabled due to the fact that any pair of the last tags
that does not exist in the last viterbi step has a viterbi of zero. There for it will be zeroed as well, so we can
ignore it. Also we ignored any pair of tag and a word that its e mle was zero, because it zeroed the viterbi equasion
as well.

MEMM task 1:
------
### Steps
1. To create a output, you should run:
    ```shell
    MEMMFeaturesExtractor.py ass1-tagger-train memm_train
    ```
    Where `ass1-tagger-train` should be the name of the training file, and `memm_train` should be the name of the output
    file to be passed to the tagger. 

    #### Output:
    * `other_file` - a file to be used in the memm2 as the other file.
    * `memm_train` - a file to be passed to the tagger.
2. Next you need to take the `memm_train` file that the program created and pass it to liblinear (which is the tagger
we used) in the following way:
    ```shell
    java -cp liblinear.jar de.bwaldvogel.liblinear.Train memm_train MODEL_FILE
    ```
    while `MODEL_FILE` is representing the name of the output file the liblinear will provide.
    We chose `memm_model`.

MEMM task 2:
------
Make sure to provide the extra file to `MEMMTag`, which is created by `MEMMFeaturesExtractor`. It's name will be:
 > other_file