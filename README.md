# absynthe: A (branching) Behavior Synthesizer

## Motivation

You need `absynthe` if you wish to simulate the behavior of any well defined 
process -- whether it's a computer application or a business process flow. Each 
process is modelled as a _control flow graph_ (or _CFG_), which typically has 
one or more root (i.e. entry) nodes and multiple leaf (i.e. end) nodes. Each
_behavior_ is the sequence of nodes encountered while traversing this CFG from 
a root to a leaf. Of course, a CFG might contain loops which could be traversed
multiple times before arriving at the leaf.

Generation of behaviors can be an unending process. That is, after completing
one root-to-leaf traversal, `absynthe` could start all over again, ad infinitum.
Moreover, if there are multiple CFGs, then `absynthe` can synthesize 
_interleaved_ behaviors. This means that a single sequence of nodes might
contain nodes from multiple CFGs.

## Usage

You can use `absynthe` to synthesize both the CFGs and the corresponding 
behaviors. However, you could also hand-craft your CFGs and use `absynthe` to
synthesize only the behaviors.
