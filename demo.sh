#!/bin/bash
echo 'Drilling repository...'
cd src && python commit_extraction.py && cd ..
echo 'Running inference...'
cd src/models && python predict_model.py ../../data/processed/2020-10-27.json random_forest && cd ../..
