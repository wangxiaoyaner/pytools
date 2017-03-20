#coding=utf-8
#input S = [1,2,3,4]
#output S的幂集
#16:08
#DFS需要记录深度信息，但要耗费一定的时间复杂度
ans = []
def dfs(s,level):
    if level >= len(s):
        print ans
        return 
    ans.append(s[level])
    dfs(s,level+1)
    ans.pop()
    dfs(s, level+1)
    return

s = [1,2,3,4]
dfs(s,0)
        
