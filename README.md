# Optimizing Event Selection for the Swim Team at APAC
This problem falls under the category of linear integer programming. It is similar to the University Class Scheduling problem or the employee time-tabling problem. 
## Problem Formulation
There are several rules when selecting events for the team at APAC:

### Constraints
1. There can only be a maximum of **12 people** representing each team.
2. Each athlete can only participate in a total of **five events** including relays: three individual events two relays, two individuals and three realys, four individuals events 1 relay etc.
3. There can only be a maximum of **four athletes** representing each team for each event.
4. There can be a maximum of **two relay teams** representing each team for each relay event.
5. Each relay team must have **four members**.

### Cost Function
The table for scoring at APAC:

| Rank | Individual Points | Relay Points |
|:---:|:---:| :---:|
| 1    | 16     | 32 |
| 2    | 13     | 26 |
| 3    | 12     | 24 |
| 4    | 11     | 22 |
| 5    | 10     | 20 |
| 6    | 9      | 18 |
| 7    | 7      | 14 |
| 8    | 5      | 10 |
| 9    | 4      | 8 |
| 10   | 3      | 6 |
| 11   | 2      | 4 |
| 12   | 1      | 2 |

I will be using a custom made cost function.
