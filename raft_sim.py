#!/usr/bin/env python3
"""raft_sim - Simplified Raft consensus protocol."""
import sys, random, time
class Node:
    def __init__(self, id, peers):
        self.id=id; self.peers=peers; self.state="follower"
        self.term=0; self.voted_for=None; self.log=[]
        self.commit_index=0; self.timeout=random.uniform(1.5,3.0)
    def request_vote(self, candidate_term, candidate_id):
        if candidate_term>self.term:
            self.term=candidate_term; self.state="follower"; self.voted_for=candidate_id
            return True
        if candidate_term==self.term and (self.voted_for is None or self.voted_for==candidate_id):
            self.voted_for=candidate_id; return True
        return False
    def start_election(self, nodes):
        self.term+=1; self.state="candidate"; self.voted_for=self.id
        votes=1
        for peer in self.peers:
            if nodes[peer].request_vote(self.term, self.id): votes+=1
        if votes>len(self.peers)//2+1:
            self.state="leader"; return True
        return False
def simulate(n=5, rounds=5):
    nodes={i:Node(i,[j for j in range(n) if j!=i]) for i in range(n)}
    for r in range(rounds):
        leader=None
        for nid,node in nodes.items():
            if node.state=="leader": leader=nid; break
        if leader is None:
            candidate=random.choice(list(nodes.keys()))
            won=nodes[candidate].start_election(nodes)
            print(f"Round {r}: Node {candidate} election {'won' if won else 'lost'} (term {nodes[candidate].term})")
        else:
            entry=f"cmd_{r}"; nodes[leader].log.append(entry)
            print(f"Round {r}: Leader {leader} committed '{entry}' (term {nodes[leader].term})")
            if random.random()<0.2:
                nodes[leader].state="follower"; print(f"  Leader {leader} stepped down!")
    print(f"\nFinal states: {[(n.id,n.state,n.term) for n in nodes.values()]}")
if __name__=="__main__": simulate()
