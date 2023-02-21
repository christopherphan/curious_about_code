10 REM BASIC solution to David Amos's coding challenge "Adding it all up"
20 REM https://discourse.davidamos.dev/t/adding-it-all-up/139
30 PRINT "VALUE?"
40 INPUT X
50 IF X <> 0 THEN GOTO 80
60 PRINT "0"
70 END
80 A=0
90 M=1
100 IF X < 0 THEN M=-1
110 X = ABS(X)
120 FOR K=1 TO X
130 A = A + K
140 NEXT K
150 PRINT M*A

