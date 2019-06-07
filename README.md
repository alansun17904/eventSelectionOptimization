# Optimizing Event Selection for the Swim Team at APAC
This problem falls under the category of linear integer programming. It is similar to the University Class Scheduling problem or the employee time-tabling problem. 

## Project Structure
- `optimize.py` The linear programming model, original script that isnt a class structure.
- `organize.py` Converts data from `ilikeswim.xlsx` to formatted `processed.xlsx`
- `wrangle.py`  Creates the scoreSchema and contains the class `ScoreSchema`
- `swimmer.py`  Contains the Enum `SwimmingRace`, has the `Filter` class which is the backbone of the score builder.
- `swimmingmodel.py` The optimization model `Model`
- `apac.py` Filters the APAC data for final comparison and ranking.


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

| Rank | Points |
|------|--------|
| 1    | 16     |
| 2    | 13     |
| 3    | 12     |
| 4    | 11     |
| 5    | 10     |
| 6    | 9      |
| 7    | 7      |
| 8    | 5      |
| 9    | 4      |
| 10   | 3      |
| 11   | 2      |
| 12   | 1      |

I will be using a custom made cost function.
