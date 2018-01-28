# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

N_FLIPS=300
SIZE=25000

S_RANGE=range(SIZE+1)

P_WIN=0.6

"""
for i in range(31):
    print(max_ev(10*i+1, int(SIZE/2)))
    
print("EV of optimal solution at 300,2500: {}".format(max_ev(300,2500)))
print("optimal first bet: {}".format(argmax_ev(300,2500)))

plt.plot(plot_fn_max_ev(300)(S_RANGE))

plt.plot(plot_fn_ev(300,2500)(bet_range(2500)))

plt.plot(plot_fn_argmax(300)(S_RANGE))
    
"""

def memoize(f):
    memo={}
    def helper(*args):
        if args not in memo:
            memo[args]=f(*args)
        return memo[args]
    return helper

def bind(f, x):
    def helper(*args):
        return f(x, *args)
    return helper

def functionalize(f):
    def helper(x):
        if hasattr(x, "__getitem__"):
            return [f(i) for i in x]
        else:
            return f(x)
    return helper

def argmax_bimodal(f, range_):
    eps = 1e-7
    if len(range_) == 0:
        raise
    if len(range_) == 1:
        return range_[0]
    
    def g(i):
        return f(range_[i])
    
    def del_(g, i):
        return g(i+1)-g(i)
    
    del_g = bind(del_, g)
    
    start = 0; end = len(range_)-2
    assert del_g(start) >= del_g(end) - eps
    if del_g(end)>0:
        return range_[-1]
    
    while end>start:
        mid = int((start+end)/2)
        if del_g(mid)<=eps:
            end=mid
        else:
            start=mid+1
    
    return range_[start]

def ev(k,s,bet):
    if k==0:
        return s
    return P_WIN * max_ev(k-1,s+bet) + (1-P_WIN) * max_ev(k-1,s-bet)

@memoize
def argmax_ev(k,s):
    ev_k_s=bind(bind(ev,k),s)
    range_=range(min(s,SIZE-s)+1)
    return argmax_bimodal(ev_k_s,range_)

@memoize
def max_ev(k,s):
    return ev(k,s,argmax_ev(k,s))

def plot_fn_ev(k, s):
    return functionalize(bind(bind(ev,k),s))

def plot_fn_max_ev(k):
    return functionalize(bind(max_ev,k))

def plot_fn_argmax(k):
    return functionalize(bind(argmax_ev,k))

def bet_range(s):
    return range(min(s,SIZE-s)+1)

    