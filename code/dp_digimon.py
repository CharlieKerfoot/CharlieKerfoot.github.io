import csv

def find_max_atk(file, max_digi, max_mem):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))
    
    dp = [[0] * (max_digi+1) for _ in range(max_mem+1)]
    
    for row in data:
        for j in range(max_mem, int(row["Memory"])-1, -1): 
            for k in range(max_digi, 0, -1): 
                dp[j][k] = max(dp[j][k], dp[j-int(row["Memory"])][k-1] + int(row["Atk"]))

    return max(dp[j][k] for j in range(max_mem+1) for k in range(1, max_digi+1))
