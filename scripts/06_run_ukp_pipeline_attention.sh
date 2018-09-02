# Script to run the training in all configurations. Must be run from the
# argument mining folder

DATE=$(date +%y-%m-%d-%H-%M)
RESULT_DIRECTORY="../results/ukpnets"
EXPERIMENT_DIRECTORY="ongoing-"$DATE
RELATIONS=""
SEPARATION_LEVEL="paragraph"
DATA_DIR="../data/echr/annotation/for_training"
echo "******** Starting experiment $DATE"
echo "******** Using relation suffix $RELATIONS"
ATTENTION_MODEL="time_pre"
ATTENTION_ACTIVATION="sigmoid"
echo "******** Using attention " $ATTENTION_MODEL " " $ATTENTION_ACTIVATION


mkdir $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/
mkdir $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/$EXPERIMENT_DIRECTORY
for PARTITION_DIR in $(compgen -f $DATA_DIR/partition)
do
    PARTITION=$(basename $PARTITION_DIR)
    echo "******** Training on $PARTITION"
    DATASET_NAME=$(compgen -f $PARTITION_DIR/${SEPARATION_LEVEL}${RELATIONS}/ukp*.p)
    # The model resulting from this command will be saved in --output_dirpath + --experiment_name _model.h5
    python -u experiments/train_BiLSTM_CNN_CRF.py \
        --dataset $DATASET_NAME \
        --attention_model $ATTENTION_MODEL \
        --attention_activation $ATTENTION_ACTIVATION \
        --output_dirpath $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/$EXPERIMENT_DIRECTORY \
        --experiment_name $PARTITION \
        --char_embedding lstm \
        --char_embedding_size 32 \
        --epochs 50 \
        --classifier CRF \
        --patience 10 \
        --dropout 0.3 0.3 \
        --batch_size 30 \
        --num_units 50 50
    # Now we need to evaluate the model
    MODEL_NAME=$(compgen -f $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/$EXPERIMENT_DIRECTORY/$PARTITION*h5)
    echo "********* Evaluating model $MODEL_NAME"
    python -u experiments/run_BiLSTM_CNN_CRF.py \
        --classifier $MODEL_NAME --dataset $DATASET_NAME \
        --attention_model $ATTENTION_MODEL \
        --output_dirname $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/$EXPERIMENT_DIRECTORY \
        --experiment_name $PARTITION
done

echo "********** All experiments completed"
mv $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/$EXPERIMENT_DIRECTORY $RESULT_DIRECTORY/${SEPARATION_LEVEL}${RELATIONS}/$DATE
