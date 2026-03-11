#!/usr/bin/env python3
"""Raft consensus algorithm simulator."""
import sys, random
class Node:
    def __init__(self,id,n):
        self.id,self.n=id,n; self.state='follower'; self.term=0
        self.voted_for=None; self.votes=0; self.log=[]; self.leader=None
        self.timeout=random.randint(150,300)
    def request_vote(self,nodes):
        self.state='candidate'; self.term+=1; self.votes=1; self.voted_for=self.id
        for n in nodes:
            if n.id!=self.id and n.term<=self.term and n.voted_for is None:
                n.voted_for=self.id; self.votes+=1; n.term=self.term
        if self.votes>self.n//2:
            self.state='leader'; self.leader=self.id
            for n in nodes: n.leader=self.id; n.state='follower' if n.id!=self.id else 'leader'
            return True
        return False
    def append_entry(self,entry,nodes):
        if self.state!='leader': return False
        self.log.append((self.term,entry)); acks=1
        for n in nodes:
            if n.id!=self.id: n.log.append((self.term,entry)); acks+=1
        return acks>self.n//2
n=int(sys.argv[1]) if len(sys.argv)>1 else 5
nodes=[Node(i,n) for i in range(n)]
print(f"Raft cluster: {n} nodes")
# Simulate election
random.seed(42)
winner=min(nodes,key=lambda n:n.timeout)
print(f"\nNode {winner.id} times out first (timeout={winner.timeout}ms)")
if winner.request_vote(nodes):
    print(f"Node {winner.id} elected leader (term {winner.term}, {winner.votes}/{n} votes)")
# Simulate log replication
for entry in ["SET x=1","SET y=2","DEL x"]:
    ok=winner.append_entry(entry,nodes)
    print(f"  Replicate '{entry}': {'committed' if ok else 'failed'} ({len(winner.log)} entries)")
print(f"\nAll logs consistent: {all(n.log==nodes[0].log for n in nodes)}")
