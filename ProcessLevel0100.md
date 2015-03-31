# Level 0100/0250 #
Level 0100 and 0250 datasets are quality controled.

## Quality flag ##
The quality flags for all parameters are stored in a single column with 3 digits per parameter.

For example, if a file has records on air temperature and air humidity (i.e. 2 parameters), the quality flag consists of 6 digits. Left of the digits, the character "q" is included mainly for computing purposes. Hence, the quality flag for the file would look like "q000000".

## Range check ##
For the range check, fixed threshold values for each parameter are used which define a reasonable lower/upper bound of data values. The range check changes the third (i.e. rightmost) digit. The meaning of the digit value is as follows:
  * 0: No check has been performed (e.g. 000)
  * 1: Check has been performed but value is in range (e.g. 001)
  * 2: Check has been performed but value is out of range (e.g. 002)

## Step check ##
For the step check, fixed threshold values for each parameter are used which define a reasonable minimum/maximum value change per time step.. The step check changes the second digit. The meaning of the digit value is as follows:
  * 0: No check has been performed (e.g. 000)
  * 1: Check has been performed but value is in range (e.g. 010)
  * 2: Check has been performed but value is out of range (e.g. 020)