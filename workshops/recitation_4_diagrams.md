# Recitation 4 
## Diagrams


### Q5. Library System

A New York City library system wants to better understand its vulnerability to book loss. They randomly sampled 5 residents from Neighborhood A, B, C, and D, for a total of 20 residents.

-  Residents from neighborhood A use Library A
-  Residents from neighborhood B use Library B
-  Library A tends to lose track of books on the shelf at a rate of 1 book per 200 days.
-  Library B tends to lose track of books on the shelf at a rate of 1 book per 300 days.
-  Residents tend to lose loaned books at a rate of 1 book per 100 days.
-  The library system's supplier loses books at a rate of 1 book per 1000 days.

1.  What is the overall probability that the library system does NOT lose any books? 
2.  How does that probability change over 3 years? 
3.  What is the average failure rate over the first year? Second year? Third year?

```mermaid
graph TD

s["Supplier<hr>&lambda; = 1/1000"]
la["Library A<hr>&lambda; = 1/200"]
lb["Library B<hr>&lambda; = 1/300"]

s---la
s---lb
la---naa
lb---nba

subgraph nb["Neighborhood B"]
    nba((" "))
    nbz((" "))
    r6["P6<hr>&lambda; = 1/100"]; r7["P7<hr>&lambda; = 1/100"];
    r8["P8<hr>&lambda; = 1/100"]; r9["P9<hr>&lambda; = 1/100"]; r10["P10<hr>&lambda; = 1/100"];
    nba --- r6
    nba --- r7
    nba --- r8
    nba --- r9
    nba --- r10
    r6 --- nbz
    r7 --- nbz
    r8 --- nbz
    r9 --- nbz
    r10 --- nbz
end

subgraph na["Neighborhood A"]
    naa((" "))
    naz((" "))
    r1["P1<hr>&lambda; = 1/100"]; r2["P2<hr>&lambda; = 1/100"]; r3["P3<hr>&lambda; = 1/100"]; 
    r4["P4<hr>&lambda; = 1/100"]; r5["P5<hr>&lambda; = 1/100"];
    naa --- r1
    naa --- r2
    naa --- r3
    naa --- r4
    naa --- r5
    r1 --- naz
    r2 --- naz
    r3 --- naz
    r4 --- naz
    r5 --- naz
end
```


