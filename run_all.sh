#!/bin/bash
start_time=$(date +%s.%N)

rm -f all_data.dat
rm -rf hrtem_images

mkdir -p hrtem_images

for i in {1..99}
do
    process_id=$(printf "%02d" $i)
    mkdir -p tmp_$process_id
    nohup ./run.sh $process_id &
done

wait
cat tmp_*/data.dat > all_data.dat
rm -rf tmp_*
end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "Total elapsed time: $elapsed_time seconds"
