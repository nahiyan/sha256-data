dirs=("cadical" "cadical-p" "cadical-p-ib")
for dir in "${dirs[@]}"; do
  : >${dir}/collisions.md
  for order in {20..38}; do
    for file in ${dir}/logs/${order}-*; do
      echo $file
      python verify_from_log.py encodings/${order}-sfs.cnf <$file >>${dir}/collisions.md
    done
  done
done
