#!/bin/bash
start_time=$(date +%s.%N)

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


#Erreur pour certains cas :
#ERROR: The Python script 'particle_analyze.py' has exited with an error.
#Traceback (most recent call last):
#  File "particle_analyze.py", line 32, in <module>
#    data = node.compute()
#  File "/home/victor/Soft/ovito-2.9.0/bin/../lib/ovito/plugins/python/ovito/__init__.py", line 202, in _ObjectNode_compute
#    if not self.wait(time = time):
#  File "/home/victor/Soft/ovito-2.9.0/bin/../lib/ovito/plugins/python/ovito/__init__.py", line 173, in _ObjectNode_wait
#    raise RuntimeError("Data pipeline evaluation failed with the following error: %s" % state.status.text)
#RuntimeError: Data pipeline evaluation failed with the following error: Cannot generate Delaunay tessellation. Simulation cell is too small, or radius parameter is too large.