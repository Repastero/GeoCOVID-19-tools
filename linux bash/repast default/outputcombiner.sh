#!/bin/bash
rm -rf instance_*/data
java -Xmx512m -cp "lib/*" repast.simphony.batch.ClusterOutputCombiner . combined_data
# rm -r instance_*
