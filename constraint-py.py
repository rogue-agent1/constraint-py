#!/usr/bin/env python3
"""Constraint propagation solver (arc consistency + backtracking)."""
import sys
from copy import deepcopy

class CSP:
    def __init__(self):self.vars={};self.constraints=[]
    def variable(self,name,domain):self.vars[name]=list(domain)
    def constraint(self,vars_,pred):self.constraints.append((vars_,pred))
    def ac3(self,domains):
        queue=[(c,v) for c in self.constraints for v in c[0]]
        while queue:
            (cvars,pred),xi=queue.pop(0)
            removed=False
            new_dom=[]
            for val in domains[xi]:
                # Check if any consistent assignment exists for other vars
                others=[v for v in cvars if v!=xi]
                if not others:
                    if pred({xi:val}):new_dom.append(val)
                    else:removed=True;continue
                # Try all combos of others
                found=False
                def try_assign(idx,assign):
                    nonlocal found
                    if found:return
                    if idx==len(others):
                        assign[xi]=val
                        if pred(assign):found=True
                        return
                    for v in domains[others[idx]]:
                        try_assign(idx+1,{**assign,others[idx]:v})
                try_assign(0,{})
                if found:new_dom.append(val)
                else:removed=True
            domains[xi]=new_dom
            if not new_dom:return False
            if removed:
                for c in self.constraints:
                    if xi in c[0]:
                        for v in c[0]:
                            if v!=xi:queue.append((c,v))
        return True
    def solve(self):
        domains=deepcopy(self.vars)
        if not self.ac3(domains):return None
        return self._bt(domains,{})
    def _bt(self,domains,assign):
        if len(assign)==len(self.vars):
            if all(pred({v:assign[v] for v in vs}) for vs,pred in self.constraints):return dict(assign)
            return None
        var=min((v for v in self.vars if v not in assign),key=lambda v:len(domains[v]))
        for val in domains[var]:
            assign[var]=val
            d2=deepcopy(domains);d2[var]=[val]
            if self.ac3(d2):
                r=self._bt(d2,assign)
                if r:return r
            del assign[var]
        return None

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        c=CSP()
        c.variable("x",range(1,10));c.variable("y",range(1,10));c.variable("z",range(1,10))
        c.constraint(["x","y"],lambda a:a["x"]!=a["y"])
        c.constraint(["y","z"],lambda a:a["y"]!=a["z"])
        c.constraint(["x","y","z"],lambda a:a["x"]+a["y"]+a["z"]==6)
        r=c.solve()
        assert r and r["x"]+r["y"]+r["z"]==6 and r["x"]!=r["y"] and r["y"]!=r["z"]
        print("All tests passed!")
    else:
        c=CSP();c.variable("a",[1,2,3]);c.variable("b",[1,2,3])
        c.constraint(["a","b"],lambda a:a["a"]<a["b"])
        print(f"Solution: {c.solve()}")
if __name__=="__main__":main()
