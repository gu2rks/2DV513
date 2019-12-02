- function dependency : prime attibute -> non-prime attibute

# 2NF
- **NO** partial dependency: part of primary key -> non-prime attibute
- if so -> create a new table
# 3NF
- **NO** transitive dependency: non-prime attibute -> non prime attibute
- if so -> create a new table

# BCNF
- **not** allow non-prime attibute -> prime attibute (how da fuq can it be like that anyway) 


# Interviews(manager, applicant, day, time, room).
## Find functional dependencies.

1. applicant, day -> manager
2. applicatn, day -> time
3. applicant, day -> room  
2. applicant -> day
which give us 

## Find the keys of the relation.
prime key: applicant and day

## Show that the relation is in 3NF but not in BCNF.
since applicant -> day is a FD. Applicant(left side) is not a supper key! which violated BCNF. On anoter hand, There is no transitive dependency which is why this relation is 3NF.

