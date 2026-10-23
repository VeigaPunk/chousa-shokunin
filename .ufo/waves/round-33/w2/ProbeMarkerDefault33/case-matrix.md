| case | base gate f4731885 | landed gate 94a7be5a | oracle 930a2075 |
|---|---|---|---|
| a-flat-plain | rc0 id=a1=supported | rc0 id=a1=supported | rc0 id=a1=supported |
| aa-default-nonstring-id-dup-line | rc0 id=aa1=contradicted | rc0 id=aa1=contradicted | rc0 id=aa1=contradicted |
| b-flat-default-contradicted | rc0 id=b1=contradicted | rc0 id=b1=contradicted | rc0 id=b1=contradicted |
| c-nested-default-obj | rc0 id=c1=contradicted | rc1 id=line1=invalid; id=c1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=c1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| c2-nested-default-arr | rc0 id=c2=contradicted | rc1 id=line1=invalid; id=c2=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=c2=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| c3-nested-default-deep | rc0 id=c3=contradicted | rc1 id=line1=invalid; id=c3=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=c3=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| c4-default-in-string | rc1 id=line1=invalid; id=c4=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=c4=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=c4=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| c5-nested-id-array | rc1 id=nested=invalid; id=c5=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc0 id=c5=contradicted | rc0 id=c5=contradicted |
| d-dup-default-same | rc0 id=d1=contradicted | rc1 id=line1=invalid; id=d1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc0 id=d1=contradicted |
| e-dup-default-diff | rc1 id=e1=unproven [CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=e1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc0 id=e1=contradicted |
| f-both-id-and-default | rc1 id=f1=supported; id=f2=unproven [CONTRADICTION_MARKER_ABSENT] | rc1 id=f1=supported; id=f2=unproven [CONTRADICTION_MARKER_ABSENT] | rc1 id=f1=supported; id=f2=unproven [CONTRADICTION_MARKER_ABSENT] |
| g-default-own-marker | rc1 id=g1=contradicted; id=g2=unproven; id=g3=unproven [CONTRADICTION_MARKER_ABSENT,CONTRADICTION_MARKER_ABSENT] | rc1 id=g1=contradicted; id=g2=unproven; id=g3=unproven [CONTRADICTION_MARKER_ABSENT,CONTRADICTION_MARKER_ABSENT] | rc1 id=g1=contradicted; id=g2=unproven; id=g3=unproven [CONTRADICTION_MARKER_ABSENT,CONTRADICTION_MARKER_ABSENT] |
| h-nested-before-top | rc1 id=h1=unproven [CONTRADICTION_MARKER_ABSENT] | rc0 id=h1=contradicted | rc0 id=h1=contradicted |
| i-default-dup-line | rc0 id=i1=contradicted | rc0 id=i1=contradicted | rc0 id=i1=contradicted |
| j-default-dup-id | rc1 id=x=invalid; id=j1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=x=invalid; id=j1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=x=invalid; id=j1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| k-default-trailing-garbage | rc0 id=k1=contradicted | rc1 id=line1=invalid; id=k1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=k1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| l-default-bracket-marker | rc0 id=l1=contradicted | rc0 id=l1=contradicted | rc0 id=l1=contradicted |
| m-nested-id-default | rc1 id=nested=invalid; id=m1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc0 id=m1=contradicted | rc0 id=m1=contradicted |
| n-default-then-nested-override | rc1 id=n1=unproven [CONTRADICTION_MARKER_ABSENT] | rc1 id=line2=invalid; id=n1=contradicted [CLAIM_RECORD_INVALID] | rc1 id=line2=invalid; id=n1=contradicted [CLAIM_RECORD_INVALID] |
| o-default-dup-span | rc0 id=o1=contradicted | rc0 id=o1=contradicted | rc0 id=o1=contradicted |
| p-default-nonstring | rc1 id=line1=invalid; id=p1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=p1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=line1=invalid; id=p1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] |
| q-nested-after-top | rc0 id=q1=contradicted | rc0 id=q1=contradicted | rc0 id=q1=contradicted |
| r-default-dup-sha | rc0 id=r1=contradicted | rc0 id=r1=contradicted | rc0 id=r1=contradicted |
| s-default-dup-expect | rc0 id=s1=contradicted | rc0 id=s1=contradicted | rc0 id=s1=contradicted |
| t-default-dup-marker | rc0 id=t1=contradicted | rc0 id=t1=contradicted | rc0 id=t1=contradicted |
| u-claim-dup-default | rc0 id=u1=supported | rc0 id=u1=invalid [CLAIM_RECORD_INVALID] | rc0 id=u1=supported |
| v-default-dup-marker-key | rc0 id=v1=contradicted | rc0 id=line1=invalid; id=v1=unproven [CLAIM_RECORD_INVALID,CONTRADICTION_MARKER_ABSENT] | rc1 id=v1=unproven [CONTRADICTION_MARKER_ABSENT] |
| w-asymmetry | rc0 id=x1=contradicted | rc1 id=x1=invalid [CLAIM_RECORD_INVALID] | rc1 id=x1=invalid [CLAIM_RECORD_INVALID] |
| x-dup-id-diff | rc0 id=x2=supported | rc1 id=line1=invalid [CLAIM_RECORD_INVALID] | rc1 id=x3=invalid [CLAIM_RECORD_INVALID] |
| y-dup-marker-claim | rc0 id=y1=contradicted | rc1 id=y1=invalid [CLAIM_RECORD_INVALID] | rc1 id=y1=invalid [CLAIM_RECORD_INVALID] |
| z-default-after-claim | rc1 id=z1=unproven; id=z2=contradicted [CONTRADICTION_MARKER_ABSENT] | rc1 id=z1=unproven; id=z2=contradicted [CONTRADICTION_MARKER_ABSENT] | rc1 id=z1=unproven; id=z2=contradicted [CONTRADICTION_MARKER_ABSENT] |
