#!/bin/bash
## (c) Pourya Gohari 2023
#Colors
RED='\033[0;31m' #RED
NC='\033[0m'     # No Color
GR='\033[0;32m'  # GREEN
BL='\033[0;34m'  # BLUE

parts=(Part1 Part2 Part3)

level=(0-Easy 1-Medium 2-Hard)

length=(4 6 8 10 12 14)
# For Part2
length_extended=(8 10 12 14 16 18)

for i in "${!parts[@]}"; do
  echo "${parts[$i]} Started..."
  if [[ "${parts[$i]}" == "Part2" ]]; then
    for j in "${!level[@]}"; do
      echo "level: ${level[$j]}"
      for k in "${!length_extended[@]}"; do
        echo "Mission length=${length_extended[$k]}"
        for l in {1..5}; do
          cp -rf ./inputs/"${parts[$i]}"/"${level[$j]}"/"${length_extended[$k]}"/"${l}"_config.txt ./config.txt
          cp -rf ./inputs/"${parts[$i]}"/"${level[$j]}"/"${length_extended[$k]}"/"${l}"_mission.txt ./mission.txt
          ## run your code
          python ./main.py
          mkdir -p ./results/"${parts[$i]}"/"${level[$j]}"/"${length_extended[$k]}"/
          cp -rf ./output.txt ./results/"${parts[$i]}"/"${level[$j]}"/"${length_extended[$k]}"/"${l}"_output.txt
          rm -rf ./output.txt
          rm -rf ./config.txt
          rm -rf ./mission.txt
        done
      done
    done
  else
    for j in "${!level[@]}"; do
      echo "level: ${level[$j]}"
      for k in "${!length[@]}"; do
        echo "Mission length=${length[$k]}"
        for l in {1..5}; do
          cp -rf ./inputs/"${parts[$i]}"/"${level[$j]}"/"${length[$k]}"/"${l}"_config.txt ./config.txt
          cp -rf ./inputs/"${parts[$i]}"/"${level[$j]}"/"${length[$k]}"/"${l}"_mission.txt ./mission.txt
          ## run your code
          python ./main.py
          mkdir -p ./results/"${parts[$i]}"/"${level[$j]}"/"${length[$k]}"/
          cp -rf ./output.txt ./results/"${parts[$i]}"/"${level[$j]}"/"${length[$k]}"/"${l}"_output.txt
          rm -rf ./output.txt
          rm -rf ./config.txt
          rm -rf ./mission.txt
        done
      done
    done
  fi
done
echo DONE!
