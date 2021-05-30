#!/bin/bash
SECONDS=0
for i in {1..100}; do
  echo -e "\nROUND $i\n"
  for j in {1..25}; do
    python3 scalability.py &
  done
  wait
echo $SECONDS
done 2>/dev/null

