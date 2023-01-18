
Causal broadcast algorithm

on initialisation do
  sendSeq := 0; delivered := ⟨0, 0, . . . , 0⟩; buffer := {}
end on

on request to broadcast m at node Ni do
  deps := delivered; deps[i] := sendSeq
  send (i, deps, m) via reliable broadcast
  sendSeq := sendSeq + 1
end on

on receiving msg from reliable broadcast at node Ni do
  buffer := buffer ∪ {msg}
  while ∃(sender , deps, m) ∈ buffer . deps ≤ delivered do
    deliver m to the application
    buffer := buffer \ {(sender , deps, m)}
    delivered[sender ] := delivered[sender ] + 1
  end while
end on

sendSeq = counts the number of messages broadcast by this node delivered = vector with one entry per node, counting the number of messages from each sender that this node has delivered buffer = for holding back messages until they are ready to be delivered deps = causal dependencies of the message

Node sends a message and it attaches the sending node i an deps. Deps is copy of delivered. All messages that have been delivered locally prior to this broadcast must appear before the broadcast message in the causal order. Receiving a message = first add in buffer, then check the buffer for new messages deps ≤ delivered - true if the node has delivered all messages prior this, in causal order.
