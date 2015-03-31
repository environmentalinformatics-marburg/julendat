# Level 0300/0310 #
Level 0300 and 0310 datasets have an hourly resolution and are gap filled.

## Data gap definition ##
Data gaps are either time periods for which no data is available or time steps whre the data values show a bad quality (based on the 0250 quality check).

## Data gap filling ##
Gaps are filled using a multiple linear interpolation based on values recorded by the 15 spatially closest station to the station dataset in question. The interpolation is trained using the 4 weeks prior to the data gap.

If one of the 15 closest stations shows a data gap during the same time period, the next closest station is selected.

If a project has considerable spatial extend like the DFG biodiversity exploratories, the selection of neighbouring stations is restricted to the same region and principal land cover type (e. g. if a station in the Hainich forest must be gap filled, only forest stations in the Hainich are considered).

## Limits ##
So far, only spatially quasi-continous parameters like temperature, air humidity etc. are gap filled.